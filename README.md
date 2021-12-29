# Flappy-Bird-Get-Rekt

## Introduction

This is a test which I will apply the things learnt from my 2D-Self-Driving-Car-Python-3 project to flappy bird. 
This will be my own version of using reinforcement learning to defeat flappy bird without computer vision.

I will not be using Flappy Bird's kind of "tap to flap" kind of mechanics (where you need to release the jump button
before you can flap again). I will be implementing it such that the bird will move upwards as long as you hold down 
the jump button. 

Key Parameters (Normalized to value between 0 and 1) to feed into the DQN network:

1) Current height of bird with respect to ground

2) Slit height of nearest pipe with respect to ground

3) Distance to nearest pipe with respect to the agent

## Issues

There were several problem at the start:

1) The collision box range of the pipe is incorrectly placed leading to the AI not being able to learn the way it 
  should. 
  
2) The punishment of hitting pipe is not severe enough for the AI to want to avoid hitting the pipe. The AI simply 
  just get near to the center of the pipe slit since the reward system is made such that a positive reward will be
  given if the agent gets nearer to the pipe slit or that it simply stay within a certain distance from the pipe slit
  center. 
  
3) I also feed in the hit_status which is unneccesary since the negative reward itself should indicate to the agent that
  it is not doing well...
  
4) The max height of the slit of the pipe is such that the agent can just depressed the jump button continously without
  crashing into the pipe because there is a maximum limit to how high the agent can flap and thus if the pipe slit is at
  the max height, then it will just need to depressed the jump button non-stop. But that of course is a edge case and will
  be a problem if the learning rate of the agent is set too high leading to it over fitting and learnt incorrectly. 
  
5) AI agent still get positive reward even after collision if the collision is momentary due to the hit status not staying
  continously "on" after colliding. So it thinks its doing well when it really isn't...
  
6) Collision box has incorrect values leading to the bird hitting pipe and not getting detected.


## Overall Results [High Score: 5117]

### Initial

Start Time: 7:00 PM

Ram Usage: 120.5 MB

### Termination

End Time: 9:12 PM

Ram Usage: 417.8 MB

Average Reward: 0.03

Number of Iteration: > 350000

Link: 

## References

Bird Icon: https://www.flaticon.com/free-icon/bird_616438

Background: https://www.desktopbackground.org/wallpaper/flappy-generator-plus-create-your-own-flappy-bird-game-799254
