from cocos.text import Label

from settings import Settings
from stats import stats


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
        self.score_hint.element.text = f"Score: {stats.score}"
        self.best_score_hint.element.text = f"Best: {stats.best_score}"

    def game_over(self):
        stats.is_game_over = True
        self.create_label("YOU LOSE", Settings.WINDOW_SIZE, "right")
        self.create_label("press [enter] to restart", (0, Settings.HEIGHT))
