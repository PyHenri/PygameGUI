import pygame
from math import sqrt


def distance(p1, p2):
    return sqrt(((p2[0] - p1[0]) ** 2) + ((p2[1] - p1[1]) ** 2))


class Button:
    def __init__(self, screen, x, y, width, height, border=0, border_color=(0, 0, 0), radius=0, text="",
                 color=(0, 0, 0), font=None,
                 image_up: str = None, image_down: str = None, image_active: str = None, background_color=(255, 0, 0),
                 active_color=(200, 0, 0), active_border_color=(0, 0, 0), clicked_color=(0, 255, 0),
                 action_mouse_button=0, advanced_calculations=True):
        # init all basic values
        self.screen = screen
        self.x = x
        self.y = y
        self.border = border
        self.border_color = border_color
        self.radius = radius
        self.color = color  # text color
        self.text = text

        if type(font) != pygame.font.Font and font is not None:  # font variable must be pygame.font.Font type
            raise TypeError
        if font is None:
            font = pygame.font.SysFont("Consolas", 21)
        self.font = font

        # if no image is given use a background_color, if background_color is None, then make button transparent
        if image_up is None or image_down is None:
            self.width = width
            self.height = height
            self.background_color = background_color

            self.image_up = None
            self.image_down = None
        # if image is given, adjust width/height
        else:
            self.image_up = pygame.image.load(image_up).convert_alpha()
            self.image_down = pygame.image.load(image_down).convert_alpha()

            if image_active is None:
                self.image_active = self.image_up
            else:
                self.image_active = image_active

            self.width = self.image_up.get_rect().width
            self.height = self.image_up.get_rect().height

        self.active = False
        self.active_color = active_color
        self.active_border_color = active_border_color
        self.clicked = False
        self.clicked_color = clicked_color
        self.action_mouse_button = action_mouse_button
        self.advanced_calculations = advanced_calculations

    def update(self, mouse, click):
        if self.radius > 0 and self.advanced_calculations:
            topRect = self.x + self.radius <= mouse[0] <= self.x + self.width - self.radius and self.y <= mouse[1] <= self.y + self.radius
            midRect = self.x <= mouse[0] <= self.x + self.width and self.y + self.radius <= mouse[1] <= self.y + self.height - self.radius
            bottomRect = self.x + self.radius <= mouse[0] <= self.x + self.width - self.radius and self.y + self.height - self.radius <= mouse[1] <= self.y + self.height
            midTopleft = distance((self.x + self.radius, self.y + self.radius), (mouse[0], mouse[1])) <= self.radius
            midBottomleft = distance((self.x + self.radius, self.y + self.height - self.radius), (mouse[0], mouse[1])) <= self.radius
            midTopright = distance((self.x + self.width - self.radius, self.y + self.radius), (mouse[0], mouse[1])) <= self.radius
            midBottomRight = distance((self.x + self.width - self.radius, self.y + self.height - self.radius), (mouse[0], mouse[1])) <= self.radius

            if topRect or midRect or bottomRect or midTopright or midTopleft or midBottomleft or midBottomRight:
                self.active = True
                if click[self.action_mouse_button]:
                    self.clicked = True
                else:
                    self.clicked = False
            else:
                self.active = False

        else:

            if self.x < mouse[0] < self.x + self.width and self.y < mouse[1] < self.y + self.height:  # if mouse is on button
                self.active = True
                if click[self.action_mouse_button]:
                    self.clicked = True
                else:
                    self.clicked = False
            else:
                self.active = False

    def draw(self):

        # if no image is given
        if self.image_up is None or self.image_down is None:
            if not self.active:
                pygame.draw.rect(self.screen, self.background_color, (self.x, self.y, self.width, self.height), 0,
                                 self.radius)  # Button
                pygame.draw.rect(self.screen, self.border_color, (self.x, self.y, self.width, self.height), self.border,
                                 self.radius)  # Border
            if self.active:
                pygame.draw.rect(self.screen, self.active_color, (self.x, self.y, self.width, self.height), 0,
                                 self.radius)  # Button
                pygame.draw.rect(self.screen, self.active_border_color, (self.x, self.y, self.width, self.height),
                                 self.border, self.radius)  # Border
            if self.clicked:
                pygame.draw.rect(self.screen, self.clicked_color, (self.x, self.y, self.width, self.height), 0,
                                 self.radius)  # Button
                pygame.draw.rect(self.screen, self.active_border_color, (self.x, self.y, self.width, self.height),
                                 self.border, self.radius)  # Border

        # if image is given
        else:
            if not self.active:
                self.screen.blit(self.image_up, [self.x, self.y])
            if self.active:
                self.screen.blit(self.image_active, [self.x, self.y])
            if self.clicked:
                self.screen.blit(self.image_down, [self.x, self.y])

        if self.text:  # if text is given, display it
            text = self.font.render(self.text, True, self.color)
            rect = text.get_rect()
            rect.center = (self.x + (self.width // 2), self.y + (self.height // 2))  # get center of rect
            self.screen.blit(text, rect)  # display rect
