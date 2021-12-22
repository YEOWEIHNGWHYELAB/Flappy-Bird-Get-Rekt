import queue
import pygame

import FlappyEngine

def circularArray(i):
    if i >= 3:
        return 0
    else:
        return i + 1

def main():
    global is_mainloop_running
    global bird_Y
    global obstaclePos
    global obstacleHeight
    global currClosestPos
    global slitCenter
    global sliding_window_hit

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
    currClosestPos = obstaclePos[crash_Index]

    # Main Loop
    while is_mainloop_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_mainloop_running = False

        # PyGame Draw
        win.fill((0, 0, 0))
        win.blit(background, (0, 0))
        flappyBird.manualMove(win)
        obstaclePipe.move(win)

        # Collision Handling (pipe width = 60 and slit size is 200 allowable, bird is at 60 + 64 and height - 64)
        if currClosestPos < obstaclePos[crash_Index]:
            crash_Index = circularArray(crash_Index)

        slitCenter = obstacleHeight[crash_Index] - 100
        currClosestPos = obstaclePos[crash_Index]
        bird_Y = flappyBird.birdHeight()

        if 60 <= currClosestPos <= 124 and abs((bird_Y + 32) - slitCenter) >= 70:
            sliding_window_hit = True
        else:
            sliding_window_hit = False

        # Test Collision
        # pygame.draw.rect(win, (255, 0, 255), pygame.Rect(30, slitCenter, 30, 10))
        # pygame.draw.rect(win, (255, 0, 0), pygame.Rect(30, (bird_Y + 32), 30, 10))
        # pygame.draw.rect(win, (255, 0, 255), pygame.Rect(124, 300, 30, 10))
        # print(abs((bird_Y + 32) - slitCenter))

        # PyGame Update
        pygame.time.delay(50)
        clock.tick(500)
        pygame.display.update()

if __name__ == '__main__':
    main()