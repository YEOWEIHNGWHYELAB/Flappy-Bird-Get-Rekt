import queue
import pygame
import math
import FlappyEngine
import matplotlib.pyplot as plt

import AI

def saveDQN(dqnForFlappy, sliding_window_scores): # save button
    dqnForFlappy.save()
    plt.plot(sliding_window_scores)
    plt.show()

def loadDQN(dqnForFlappy):  # load button
    dqnForFlappy.load()

def circularArray(i):
    if i >= 3:
        return 0
    else:
        return i + 1

def display_max_score(win, x, y, font):
    score = font.render("Current Score: " + str(current_Score), True, (255, 255, 255))
    win.blit(score, (x, y))


def display_current_score(win, x, y, font):
    score = font.render("High Score: " + str(max_Score), True, (255, 255, 255))
    win.blit(score, (x, y))

def display_avg_reward(win, x, y, font):
    float = avg_score
    format_float = "{:.2f}".format(float)
    score = font.render("AVG Reward: " + str(format_float), True, (255, 255, 255))
    win.blit(score, (x, y))


def reward_management(hit_Status, clear_Hit):
    if (hit_Status):
        return -1
    elif (clear_Hit):
        return 0.3
    else:
        return -0.2


def main():
    global is_mainloop_running
    global bird_Y
    global obstaclePos
    global obstacleHeight
    global currClosestPos
    global slitCenter
    global hit_Status
    global max_Score
    global current_Score
    global last_reward
    global avg_score
    global hit_reset
    global denominator

    # DQN Network Initialization
    sliding_window_scores = []
    dqnForFlappy = AI.Dqn(3, 2, 0.7)

    # Set up Screen & PyGame
    is_mainloop_running = True
    pygame.init()
    width = 1280
    height = 720
    win = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Flappy Bird Get Rekt!")

    # Image Setup
    background = pygame.image.load('./Images/background.png')

    # Bird & Obstacles
    flappyBird = FlappyEngine.BirdFly()
    obstaclePipe = FlappyEngine.ObstaclesPipe(1220)
    obstaclePos = obstaclePipe.getPosList()
    obstacleHeight = obstaclePipe.getHeightList()
    crash_Index = 0
    max_Score = 0
    current_Score = 0
    last_reward = 0
    denominator = 1220
    ai_ctrl = True
    score_status = False
    hit_reset = False
    old_slit = 0
    highScoreFont = pygame.font.Font('freesansbold.ttf', 32, )
    currentScoreFont = pygame.font.Font('freesansbold.ttf', 32, )
    avfScoreFont = pygame.font.Font('freesansbold.ttf', 32, )
    currClosestPos = obstaclePos[crash_Index]

    # Main Loop
    while is_mainloop_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_mainloop_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    saveDQN(dqnForFlappy, sliding_window_scores)
                elif event.key == pygame.K_DOWN:
                    loadDQN(dqnForFlappy)

        # PyGame Draw
        win.fill((0, 0, 0))
        win.blit(background, (0, 0))
        flappyBird.aiMove(win)
        obstaclePipe.move(win)

        # Collision Handling (pipe width = 60 and slit size is 200 allowable, bird is at 60 + 64 and height - 64)
        clear_Hit = False
        if currClosestPos < obstaclePos[crash_Index]:
            crash_Index = circularArray(crash_Index)
            denominator = 380
            if (hit_Status is False):
                current_Score += 1
                clear_Hit = True
            if (hit_reset is True):
                hit_reset = False

        slitCenter = obstacleHeight[crash_Index] - 100
        currClosestPos = obstaclePos[crash_Index]
        bird_Y = flappyBird.birdHeight()

        if 30 <= currClosestPos <= 124 and abs((bird_Y + 32) - slitCenter) >= 70:
            hit_Status = True
            current_Score = 0
            hit_reset = True
        else:
            hit_Status = False

        bonus = 0.0
        # near_Slit = abs(bird_Y - slitCenter)
        # if (abs(near_Slit) <= 60):
        #     bonus = 0.1
        near_Slit = abs(bird_Y - slitCenter)
        if (near_Slit < old_slit and (not hit_Status)):
            bonus = 0.1
        elif(abs(near_Slit) <= 80 and (not hit_Status)):
            bonus = 0.3
        else:
            bonus = -0.5
        old_slit = near_Slit

        last_reward = reward_management(hit_Status, clear_Hit) + bonus

        # Test Collision
        # pygame.draw.rect(win, (255, 0, 255), pygame.Rect(30, slitCenter, 30, 10))
        # pygame.draw.rect(win, (255, 0, 0), pygame.Rect(30, (bird_Y + 32), 30, 10))
        # pygame.draw.rect(win, (255, 0, 255), pygame.Rect(124, 300, 30, 10))
        # pygame.draw.rect(win, (255, 0, 255), pygame.Rect(60, 300, 30, 10))
        # print(abs((bird_Y + 32) - slitCenter))
        pygame.draw.rect(win, (255, 0, 255), pygame.Rect(60, slitCenter, 30, 5))
        pygame.draw.rect(win, (255, 0, 0), pygame.Rect(60, bird_Y + 32, 30, 5))

        # Scoring Display
        avg_score = dqnForFlappy.overall_score()
        display_current_score(win, 10, 10, currentScoreFont)
        if current_Score > max_Score:
            max_Score = current_Score
        display_max_score(win, 10, 50, highScoreFont)
        display_avg_reward(win, 10, 90, avfScoreFont)

        # AI Handling
        last_state = [(float(currClosestPos) / denominator), (float(slitCenter) / 660), (float(bird_Y + 32) / (660 + 32))]
        # last_state = [hit_Status, currClosestPos, slitCenter, bird_Y]
        # last_state = [(float(currClosestPos) / width), near_Slit]
        next_action = dqnForFlappy.update(last_reward, last_state)
        sliding_window_scores.append(dqnForFlappy.overall_score())
        flappyBird.dqn_choice = bool(next_action)
        # print(last_state)

        # PyGame Update
        pygame.time.delay(50)
        clock.tick(500)
        pygame.display.update()


if __name__ == '__main__':
    main()
