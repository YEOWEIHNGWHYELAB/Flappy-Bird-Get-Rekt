# Flappy-Bird-Get-Rekt

## Introduction
This is a test which I will apply the things learnt from my 2D-Self-Driving-Car-Python-3 project to flappy bird. 
This will be my own version of using reinforcement learning to defeat flappy bird without computer vision. I will
just be feeding in data like height of slit, distance to slit, height of bird. 


I will not be using Flappy Bird's kind of "tap to flap" kind of mechanics (where you need to release the jump button
before you can flap again). I will be implementing it such that the bird will move upwards as long as you hold down 
the jump button. 


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
  

# Overall Results
Duration of training: 7 Hours
Recorded High Score: 10452


## References
Bird Icon: https://www.flaticon.com/free-icon/bird_616438
Background: https://www.desktopbackground.org/wallpaper/flappy-generator-plus-create-your-own-flappy-bird-game-799254
