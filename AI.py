# DQN AI

import os
import random

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.autograd import Variable


# Creating the architecture of the Neural Network
class Network(nn.Module):
    def __init__(self, input_size, nb_action):
        super(Network, self).__init__()
        self.input_size = input_size
        self.nb_action = nb_action
        self.fc1 = nn.Linear(input_size, 30)
        self.fc2 = nn.Linear(30, nb_action)

    def forward(self, state):
        x = F.relu(self.fc1(state))
        q_values = self.fc2(x)
        return q_values


# Implementing Experience Replay
class ReplayMemory(object):
    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = []

    def push(self, event):
        self.memory.append(event)
        if len(self.memory) > self.capacity:
            del self.memory[0]

    def sample(self, batch_size):
        samples = zip(*random.sample(self.memory, batch_size))
        return map(lambda x: Variable(torch.cat(x, 0)), samples)


# Main Deep Q Network Class
class Dqn(object):
    def __init__(self, input_size, nb_action, gamma):
        self.gamma = gamma
        self.sliding_reward_window = []
        self.model = Network(input_size, nb_action)
        self.memory = ReplayMemory(100000)
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.001)
        self.last_state = torch.Tensor(input_size).unsqueeze(0)
        self.last_action = 0
        self.last_reward = 0

    def select_action(self, state):
        probs = F.softmax(self.model(Variable(state)) * 100, dim=1)  # T = 100
        action = probs.multinomial(100, replacement=True)
        return action.data[0, 0]

    def learn(self, batch_state, batch_next_state, batch_reward, batch_action):
        outputs = self.model(batch_state).gather(1, batch_action.unsqueeze(1)).squeeze(1)
        next_outputs = self.model(batch_next_state).detach().max(1)[0]
        target = self.gamma * next_outputs + batch_reward
        td_loss = F.smooth_l1_loss(outputs, target)
        self.optimizer.zero_grad()
        td_loss.backward()
        self.optimizer.step()

    def update(self, reward, new_signal):
        new_state = torch.Tensor(new_signal).float().unsqueeze(0)
        self.memory.push(
            (self.last_state, new_state, torch.LongTensor([int(self.last_action)]), torch.Tensor([self.last_reward])))
        action = self.select_action(new_state)
        if len(self.memory.memory) > 100:
            batch_state, batch_next_state, batch_action, batch_reward = self.memory.sample(100)
            self.learn(batch_state, batch_next_state, batch_reward, batch_action)
        self.last_action = action
        self.last_state = new_state
        self.last_reward = reward
        self.sliding_reward_window.append(reward)
        if len(self.sliding_reward_window) > 1000:  # This self.reward_window will have a list of item that is less than 1000.
            del self.sliding_reward_window[0]  # Whenever the list goes beyond 1000, the first item in the list is terminated.
        return action

    def overall_score(self):
        return sum(self.sliding_reward_window) / (len(self.sliding_reward_window) + 1.)

    def save(self):
        torch.save({'state_dict': self.model.state_dict(),
                    'optimizer': self.optimizer.state_dict(),
                    }, './Brain/last_brain.pth')
        print("Current DQN is Saved!")

    def load(self):
        if os.path.isfile('./Brain/last_brain.pth'):
            print("Loading Previously Saved DQN!")
            checkpoint = torch.load('./Brain/last_brain.pth')
            self.model.load_state_dict(checkpoint['state_dict'])
            self.optimizer.load_state_dict(checkpoint['optimizer'])
        # If there is no file found then this is executed.
        else:
            print("No Saved DQN found!")
