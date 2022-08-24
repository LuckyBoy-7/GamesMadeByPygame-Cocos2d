from cocos.text import Label
from cocos.rect import Rect

from settings import Settings


class Hint(object):
    def __init__(self, game_layer):
        self.game_layer = game_layer

        self.score_hint = self.create_label(f"Score: ", (0, Settings.HEIGHT - 50))
        self.best_score_hint = self.create_label(f"Best: ", (300, Settings.HEIGHT - 50))

    def create_label(self, text, pos, anchor_x="left"):
        label = Label(text=text,
                      position=pos,
                      font_size=30,
                      color=(0, 0, 0, 255),
                      anchor_x=anchor_x,
                      anchor_y="top")
        self.game_layer.add(label)
        return label

    def update_hint(self):
        self.score_hint.element.text = f"Score: {Settings.score}"
        self.best_score_hint.element.text = f"Best: {Settings.best_score}"

    def game_over(self):
        self.game_layer.is_game_over = True
        self.create_label("YOU LOSE", Settings.WINDOW_SIZE, "right")
        self.create_label("press [enter] to restart", (0, Settings.HEIGHT))


class Button(object):
    def __init__(self, game_layer):
        self.game_layer = game_layer

        self.low_level_rect = self.create_label("初级", (Settings.WIDTH - 20, 0))
        self.mid_level_rect = self.create_label("中级", (Settings.WIDTH - 120, 0))
        self.high_level_rect = self.create_label("高级", (Settings.WIDTH - 220, 0))

    def create_label(self, text, pos):
        label = Label(text=text,
                      position=pos,
                      font_name="Fira code",
                      font_size=30,
                      color=BLACK,
                      anchor_x="right",
                      anchor_y="bottom")
        self.game_layer.add(label)

        return Rect(label.x - label.element.content_width,
                    label.y,
                    label.element.content_width,
                    label.element.content_height)
