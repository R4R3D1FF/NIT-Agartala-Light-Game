import pygame

image = pygame.image.load("E:/NitAgartala/winScreen.png")
def youWon(screen):
    print('inside')
    run = 1
    while (run):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                run = 0
        screen.blit(image, (0,0))
        pygame.display.update()