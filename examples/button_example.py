import pygame
from button import Button

pygame.init()

pygame.init()
clock = pygame.time.Clock()
running = True
screen = pygame.display.set_mode((640, 480))

b = Button(screen, 100, 100, 200, 100, border=4, radius=10, text="hello world", action_mouse_button=0)

b2 = Button(screen, 100, 300, 100, 50, border=3, border_color=(100, 0, 0), text="start", color=(200, 100, 150),
            font=pygame.font.SysFont("Consolas", 10), background_color=(255, 255, 200), active_color=(190, 90, 140),
            active_border_color=(150, 0, 0), clicked_color=(0, 255, 0))

while running:
    screen.fill((255, 255, 255))
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    b.update(pygame.mouse.get_pos(), pygame.mouse.get_pressed())
    b.draw()
    b2.update(pygame.mouse.get_pos(), pygame.mouse.get_pressed())
    b2.draw()


    clock.tick(60)
    pygame.display.flip()
    screen.fill((255, 255, 255))

pygame.quit()
