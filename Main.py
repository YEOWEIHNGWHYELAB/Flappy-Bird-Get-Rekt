import FlappyEngine
import pygame

def main():
    global is_mainloop_running
    global bird_Y

    # Set up Screen & PyGame
    is_mainloop_running = True
    is_initialized = False
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

        # PyGame Update
        pygame.time.delay(50)
        clock.tick(500)
        pygame.display.update()

if __name__ == '__main__':
    main()