import pygame
from slider import Slider

pygame.init()
clock = pygame.time.Clock()
running = True
screen = pygame.display.set_mode((640, 480))
font = pygame.font.SysFont(None, 32)

slider = Slider(max_value=255, h=20, w=5, value=255, x_box=100, y_box=300, h_box=20, w_box=300,
                box_color=(0, 0, 0), slider_color=(100, 100, 100), box_border_size=2)

while running:
    screen.fill((255, 255, 255))
    events = pygame.event.get()
    for e in events:
        if e.type == pygame.QUIT:
            running = False

    slider.update(pygame.mouse.get_pos(), pygame.mouse.get_pressed())
    slider.draw(screen=screen)

    clock.tick(60)
    pygame.display.flip()
    screen.fill((255, 255, 255))

pygame.quit()
