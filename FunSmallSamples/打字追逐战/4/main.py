from cocos.scene import Scene
from cocos.layer import Layer, ColorLayer
from cocos.director import director

from settings import Settings
from typing_layer import TypeLayer
from grid import GridLayer, Player, Enemy


class GameScene(Scene):
    def __init__(self):
        super(GameScene, self).__init__()

        self.add(ColorLayer(127, 127, 155, 255), z=1)  # 背景涂白
        self.add(GameLayer(), z=2)


class GameLayer(Layer):
    is_event_handler = True

    def __init__(self):
        super(GameLayer, self).__init__()

        self.add(TypeLayer())
        grid_layer = GridLayer()
        self.add(grid_layer)

        self.route = grid_layer.route
        self.character_init()

        self.schedule(self.update)

    def character_init(self):
        self.player = Player(self.route)
        self.add(self.player)

        self.enemy = Enemy(self.route)
        self.add(self.enemy)

    def update(self, dt):
        self.player.draw()
        self.enemy.draw()
        self._handle_enemy_move()

    def _handle_enemy_move(self):
        self.enemy.move_elapsed += 1
        if self.enemy.move_elapsed > 10:
            self.enemy.move_elapsed = 0

            tmp = self.enemy.idx
            for _ in range(5):
                tmp = (tmp + self.enemy.direct * 1) % len(self.route)
                if tmp == self.player.idx:
                    self.enemy.direct = -1 if self.enemy.direct == 1 else 1
                    self.player.direct = -1 if self.player.direct == 1 else 1
            self.enemy.idx = (self.enemy.idx + self.enemy.direct * 1) % len(self.route)


if __name__ == '__main__':
    director.init(width=Settings.WIDTH, height=Settings.HEIGHT)
    director.run(GameScene())
