import os
from atexit import register


class Stats:
    def __init__(self):
        self.is_start = False
        self.is_game_over = False

        self.score = 0
        if not os.path.exists("score.txt"):
            with open("score.txt", "w", encoding="UTF-8") as f:
                f.write("0")
            self.best_score = 0
        else:
            with open("score.txt", "r+", encoding="UTF-8") as f:
                txt = f.read()
                if txt.isdigit():
                    self.best_score = int(txt)
                else:
                    if any(letter.isdigit() for letter in txt):
                        self.best_score = int("".join([num for num in txt if num.isdigit()]))
                    else:
                        self.best_score = 0

    def restart(self):
        self.is_start = False
        self.is_game_over = False

        self.score = 0


stats = Stats()


# 退出游戏时将分数写入文件
@register
def exit_write_score():
    with open("score.txt", "w", encoding="UTF-8") as f:
        f.write(f"{stats.best_score}")
