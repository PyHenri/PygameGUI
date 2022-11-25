import pygame
from Textbox import textbox

pygame.init()
clock = pygame.time.Clock()
running = True
screen = pygame.display.set_mode((640, 480))
font = pygame.font.SysFont(None, 32)

box = textbox(screen, 100, 100, 300, 350, 50, font, (0, 0, 0), (150, 150, 255), (255, 0, 100))

while running:
    screen.fill((255, 255, 255))
    events = pygame.event.get()
    for e in events:
        if e.type == pygame.QUIT:
            running = False

    box.update(pygame.mouse.get_pos(), pygame.mouse.get_pressed(), events)

    clock.tick(60)
    pygame.display.flip()
    screen.fill((255, 255, 255))

pygame.quit()
