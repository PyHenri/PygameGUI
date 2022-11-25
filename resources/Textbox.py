import pygame


class textbox:

    def __init__(self, screen, x, y, minwidth, maxwidth, height, font, default_color, active_color, textcolor, border=2, initial=""):
        self.screen = screen
        self.x = x
        self.y = y
        self.minwidth = minwidth
        self.maxwidth = maxwidth
        self.height = height
        self.border = border
        self.font = font
        self.default_color = default_color
        self.active_color = active_color
        self.textcolor = textcolor

        self.active = False
        self.left = initial  # string on the left of the cursor
        self.right = ""  # string on the right of the cursor

    def draw(self):

        rendered_surface = self.font.render(self.value + " ", True, self.textcolor)
        width = max(self.minwidth, rendered_surface.get_width())
        if width > self.maxwidth:
            width = self.maxwidth

        box = pygame.Surface((width, self.height), pygame.SRCALPHA).convert_alpha()

        if not self.active:
            pygame.draw.rect(box, self.default_color, (0, 0, width, self.height), self.border)
        else:
            pygame.draw.rect(box, self.active_color, (0, 0, width, self.height), self.border)

        if rendered_surface.get_width() > self.maxwidth:
            offset = rendered_surface.get_width() - self.maxwidth
        else:
            offset = 0
        print(offset)

        box.blit(rendered_surface, (0 - offset, (self.height - rendered_surface.get_height())/2))
        self.screen.blit(box, (self.x, self.y))

    def update(self, mouse, click, events):
        # enable/disable all actions
        if self.x < mouse[0] < self.x + self.minwidth and self.y < mouse[1] < self.y + self.height:  # if mouse is on box

            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)  # change cursor
            if click[0] and self.active == False:
                self.active = True
                pygame.key.set_repeat(200, 25)  # makes keyinput slower
        else:

            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)  # change cursor
            if click[0] and self.active == True:
                self.active = False
                pygame.key.set_repeat(0, 0)  # sets keyinput to default

        if self.active:
            for e in events:
                if e.type == pygame.KEYDOWN:

                    # search function with the name "_process_" + e.key and execute it
                    attrname = f"_process_{pygame.key.name(e.key)}"
                    if hasattr(self, attrname):
                        getattr(self, attrname)()

                    else:
                        self._process_other(e)

        self.draw()

    def _process_delete(self):
        self.right = self.right[1:]

    def _process_backspace(self):
        self.left = self.left[:-1]

    def _process_right(self):
        self.cursor_pos += 1

    def _process_left(self):
        self.cursor_pos -= 1

    def _process_end(self):
        self.cursor_pos = len(self.value)

    def _process_home(self):
        self.cursor_pos = 0

    def _process_other(self, e):
        self.left += e.unicode

    @property
    def value(self):
        return self.left + self.right

    @property
    def cursor_pos(self):
        # Get / set the position of the cursor. Will clamp to [0, length of input].
        return len(self.left)

    @cursor_pos.setter
    def cursor_pos(self, value):
        complete = self.value
        self.left = complete[:value]
        self.right = complete[value:]
