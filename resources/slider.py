# import modules
import pygame


class Slider:
    def __init__(self, max_value, h, w, value, x_box, y_box, h_box, w_box, box_color, slider_color, box_border_size):
        self.max_value = max_value
        self.h = h
        self.w = w
        self.x_box = x_box
        self.y_box = y_box
        self.h_box = h_box
        self.w_box = w_box
        self.box_color = box_color
        self.slider_color = slider_color
        self.box_border_size = box_border_size
        self.active = False
        self.value = value
        self.x = self.x_box + (self.w_box / self.max_value * value - self.w)

        self.font = pygame.font.SysFont(None, 24)

    def update(self, pos, click):
        
        # if cursor is inside the box
        if self.x_box < pos[0] < self.x_box + self.w_box and self.y_box < pos[1] < self.y_box + self.h_box:
            if click[0] == 1:
                # set active to true
                self.active = True
        
        # reset self.active to False if cursor is no longer dragging
        if click[0] == 0:
            self.active = False

        if self.active:
            # set value to cursor x
            self.x = pos[0]
            # adjust self.x if cursor x is smaller than the box
            if (self.x - self.x_box) / ((self.w_box - self.w) / self.max_value) < 0:
                self.x = self.x_box
            # adjust value if cursor x is bigger than the box
            if (self.x - self.x_box) / ((self.w_box - self.w) / self.max_value) > 255:
                self.x = self.x_box + (self.w_box / self.max_value * 255 - self.w)
            # calculate the value depending on position of the rect thingie
            self.value = round((self.x - self.x_box) / ((self.w_box - self.w) / self.max_value))

    def draw(self, screen):
        # draw box
        pygame.draw.rect(screen, self.box_color, (self.x_box, self.y_box, self.w_box, self.h_box), self.box_border_size)
        # draw cursor rect thingie
        pygame.draw.rect(screen, self.slider_color, (self.x, self.y_box, self.w, self.h))
        # display the value
        text_surface = self.font.render(str(self.value), True, (0, 0, 0))
        screen.blit(text_surface, (self.x_box + self.w_box + 5, self.y_box))
