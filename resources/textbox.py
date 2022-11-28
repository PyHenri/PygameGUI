import pygame


def splitkeep(s, delimiter):
    return [word + delimiter for word in s.split(delimiter)]


class Text:

    def __init__(self, screen, x, y, height, width, text_, color=(0, 0, 0), font=None, lineSpacing=0):
        self.screen = screen
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.lineSpacing = lineSpacing
        self.color = color

        if type(font) != pygame.font.Font and font is not None:  # font variable must be pygame.font.Font type
            raise TypeError
        if font is None:
            font = pygame.font.SysFont("Consolas", 21)
        self.font = font

        self.text_ = self.format_text(text_)

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

    def blit_text(self):
        for idx, line in enumerate(self.text_):
            l = self.font.render(line, True, self.color)
            self.screen.blit(l, (self.x, (idx * l.get_height()) + (self.lineSpacing * idx)))
