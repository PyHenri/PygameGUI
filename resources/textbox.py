import pygame


def splitkeep(s, delimiter):
    return [word + delimiter for word in s.split(delimiter)]


class Text:

    def __init__(self, screen, x, y, text_, width="auto", height="auto", color=(0, 0, 0), font=None, lineSpacing=0, border=2, border_color=(0, 0, 0), align="left"):
        self.max_width = None
        self.screen = screen
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.lineSpacing = lineSpacing
        self.color = color
        self.border = border
        self.border_color = border_color
        self.align = align

        if type(font) != pygame.font.Font and font is not None:  # font variable must be pygame.font.Font type
            raise TypeError
        if font is None:
            font = pygame.font.SysFont("Consolas", 21)
        self.font = font

        self.text_ = self.format_text(text_)

    def format_text(self, text_):
        text = splitkeep(text_, " ")

        if self.width == "auto":
            self.max_width = self.screen.get_width() - self.x - self.border
        else:
            self.max_width = self.width

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
                if line_width + self.font.size(w)[0] > self.max_width - self.border or idx == 1:
                    split_text.append(line)
                    line = w
                    line_width = self.font.size(w)[0]
                else:
                    line_width += self.font.size(w)[0]
                    line += w
        split_text.append(line)
        return split_text

    def blit_text(self):
        height = 0

        for idx, line in enumerate(self.text_):
            l = self.font.render(line, True, self.color)
            y = (idx * l.get_height()) + (self.lineSpacing * idx) + self.y + self.border

            if self.align == "left":
                x = self.x + self.border
            elif self.align == "right":
                x = self.x + self.max_width - l.get_width() + self.border
            if self.align == "center":
                x = self.x + self.border + (self.max_width - l.get_width())//2
            self.screen.blit(l, (x, y))

        if self.height == "auto":
            height = y + l.get_height()

        if self.border > 0:
            if self.height == "auto":
                pygame.draw.rect(self.screen, self.border_color, (self.x, self.y, self.max_width, height), self.border)
            else:
                pygame.draw.rect(self.screen, self.border_color, (self.x, self.y, self.max_width, self.height), self.border)
