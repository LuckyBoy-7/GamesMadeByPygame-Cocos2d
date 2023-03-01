from pygame import font


class Fonts(object):
    @classmethod
    def my_font(cls, font_size):
        return font.Font("./resources/fonts/Determination.otf", font_size)
