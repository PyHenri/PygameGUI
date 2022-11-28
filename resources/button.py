# import modules
import pygame
from math import sqrt


def splitkeep(s, delimiter):
    return [word + delimiter for word in s.split(delimiter)]


def distance(p1, p2):
    return sqrt(((p2[0] - p1[0]) ** 2) + ((p2[1] - p1[1]) ** 2))


class ImageButton:
    def __init__(self, screen, x, y, text="", color=(0, 0, 0), font=None, image_up: str = None, image_down: str = None, image_active: str = None, action_mouse_button=0, lines=True, lineSpacing=0):
        # init all basic values
        self.screen = screen
        self.x = x
        self.y = y

        self.image_up = pygame.image.load(image_up).convert_alpha()
        self.image_down = pygame.image.load(image_down).convert_alpha()
        if image_active is None:
            self.image_active = self.image_up
        else:
            self.image_active = pygame.image.load(image_active).convert_alpha()
        self.width = self.image_up.get_rect().width
        self.height = self.image_up.get_rect().height

        if type(font) != pygame.font.Font and font is not None:  # font variable must be pygame.font.Font type
            raise TypeError
        if font is None:
            font = pygame.font.SysFont("Consolas", 21)
        self.font = font
        self.text = text
        self.lines = lines  # True if the text should be rendered with line breaks
        self.lineSpacing = lineSpacing
        if self.lines and text:
            self.text_ = self.format_text(text)
        self.color = color  # text color

        self.active = False
        self.clicked = False
        self.action_mouse_button = action_mouse_button

    def update(self, mouse, click):
        if self.x < mouse[0] < self.x + self.width and self.y < mouse[1] < self.y + self.height:  # if mouse is on button
            self.active = True
            if click[self.action_mouse_button]:
                self.clicked = True
            else:
                self.clicked = False
        else:
            self.active = False

    def draw(self):
        if not self.active:
            self.screen.blit(self.image_up, [self.x, self.y])
        if self.active:
            self.screen.blit(self.image_active, [self.x, self.y])
        if self.clicked:
            self.screen.blit(self.image_down, [self.x, self.y])

        if self.text:  # if text is given, display it
            if self.lines:
                for idx, line in enumerate(self.text_):
                    l = self.font.render(line, True, self.color)
                    y = (idx * l.get_height()) + (self.lineSpacing * idx) + self.y
                    self.screen.blit(l, (self.x, y))
            else:
                text = self.font.render(self.text, True, self.color)
                rect = text.get_rect()
                rect.center = (self.x + (self.width // 2), self.y + (self.height // 2))  # get center of rect
                self.screen.blit(text, rect)  # display rect

    def format_text(self, text_):
        text = splitkeep(text_, " ")

        max_width = self.width
        line_width = 0
        split_text = []
        line = ""
        # split text into lines
        for word in text:
            if "\n" in word:
                words = word.split()
                words[1] += " "
            else:
                words = [word]

            for idx, w in enumerate(words):
                if line_width + self.font.size(w)[0] > max_width or idx == 1:
                    split_text.append(line)
                    line = w
                    line_width = self.font.size(w)[0]
                else:
                    line_width += self.font.size(w)[0]
                    line += w
        split_text.append(line)
        return split_text


class Button:
    def __init__(self, screen, x, y, width, height, text="", font=None, background_color=(255, 0, 0), color=(0, 0, 0), border_color=(0, 0, 0), active_color=(200, 0, 0), active_border_color=(0, 0, 0), clicked_color=(0, 255, 0), border=5, radius=0, action_mouse_button=0, advanced_calculations=True, lines=True, lineSpacing=0):
        # init all basic values
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.border = border
        self.radius = radius

        self.border_color = border_color
        self.background_color = background_color
        self.color = color  # text color
        self.active_color = active_color  # color switches to this color if self.active
        self.active_border_color = active_border_color
        self.clicked_color = clicked_color

        if type(font) != pygame.font.Font and font is not None:  # font variable must be pygame.font.Font type
            raise TypeError
        if font is None:
            font = pygame.font.SysFont("Consolas", 21)
        self.font = font

        self.text = text
        self.lines = lines  # True if the text should be rendered with line breaks
        self.lineSpacing = lineSpacing
        if self.lines:
            self.text_ = self.format_text(text)

        self.active = False
        self.clicked = False
        self.action_mouse_button = action_mouse_button
        self.advanced_calculations = advanced_calculations  # enables calculations for the button corners

    def update(self, mouse, click):
        # if button should calculate the corners
        if self.radius > 0 and self.advanced_calculations:
            # create variables which turn to true if the mouse cursor is touching them
            # the following statements are self explaining
            topRect = self.x + self.radius <= mouse[0] <= self.x + self.width - self.radius and self.y <= mouse[1] <= self.y + self.radius
            midRect = self.x <= mouse[0] <= self.x + self.width and self.y + self.radius <= mouse[1] <= self.y + self.height - self.radius
            bottomRect = self.x + self.radius <= mouse[0] <= self.x + self.width - self.radius and self.y + self.height - self.radius <= mouse[1] <= self.y + self.height

            # calculate the distance of the mouse cursor from side pointing inside the button of a circle with the given radius
            # and set the corners to true if the distance if smaller than the radius
            midTopleft = distance((self.x + self.radius, self.y + self.radius), (mouse[0], mouse[1])) <= self.radius
            midBottomleft = distance((self.x + self.radius, self.y + self.height - self.radius), (mouse[0], mouse[1])) <= self.radius
            midTopright = distance((self.x + self.width - self.radius, self.y + self.radius), (mouse[0], mouse[1])) <= self.radius
            midBottomRight = distance((self.x + self.width - self.radius, self.y + self.height - self.radius), (mouse[0], mouse[1])) <= self.radius

            # if cursor is touching one of those areas self.active is turned to true
            if topRect or midRect or bottomRect or midTopright or midTopleft or midBottomleft or midBottomRight:
                self.active = True
                if click[self.action_mouse_button]:
                    self.clicked = True
                else:
                    self.clicked = False
            else:
                self.active = False

        else:
            # if the button schould not calculate the corners, the detection might not be pixel perfect
            if self.x < mouse[0] < self.x + self.width and self.y < mouse[1] < self.y + self.height:  # if mouse is on button
                self.active = True
                if click[self.action_mouse_button]:
                    self.clicked = True
                else:
                    self.clicked = False
            else:
                self.active = False

    def draw(self):

        if not self.active:
            pygame.draw.rect(self.screen, self.background_color, (self.x, self.y, self.width, self.height), 0, self.radius)  # Button
            if self.border:
                pygame.draw.rect(self.screen, self.border_color, (self.x, self.y, self.width, self.height), self.border, self.radius)  # Border
        if self.active:
            pygame.draw.rect(self.screen, self.active_color, (self.x, self.y, self.width, self.height), 0, self.radius)  # Button
            if self.border:
                pygame.draw.rect(self.screen, self.active_border_color, (self.x, self.y, self.width, self.height), self.border, self.radius)  # Border
        if self.clicked:
            pygame.draw.rect(self.screen, self.clicked_color, (self.x, self.y, self.width, self.height), 0, self.radius)  # Button
            if self.border:
                pygame.draw.rect(self.screen, self.active_border_color, (self.x, self.y, self.width, self.height), self.border, self.radius)  # Border
        
        if self.text:  # if text is given, display it
            if self.lines:
                for idx, line in enumerate(self.text_):
                    l = self.font.render(line, True, self.color)
                    y = (idx * l.get_height()) + (self.lineSpacing * idx) + self.y + self.border
                    self.screen.blit(l, (self.x + self.border, y))
            else:
                text = self.font.render(self.text, True, self.color)
                rect = text.get_rect()
                rect.center = (self.x + (self.width // 2), self.y + (self.height // 2))  # get center of rect
                self.screen.blit(text, rect)  # display rect

    def format_text(self, text_):
        text = splitkeep(text_, " ")

        max_width = self.width
        line_width = 0
        split_text = []
        line = ""
        # split text into lines
        for word in text:
            if "\n" in word:
                words = word.split()
                words[1] += " "
            else:
                words = [word]

            for idx, w in enumerate(words):
                if line_width + self.font.size(w)[0] > max_width or idx == 1:
                    split_text.append(line)
                    line = w
                    line_width = self.font.size(w)[0]
                else:
                    line_width += self.font.size(w)[0]
                    line += w
        split_text.append(line)
        return split_text
