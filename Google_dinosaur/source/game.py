import random

from cocos.sprite import Sprite
from cocos.layer import Layer, ColorLayer
from cocos.scene import Scene
from cocos.text import Label
from cocos.actions import FadeIn, FadeOut
from cocos.director import director
from cocos.collision_model import CollisionManagerGrid
from cocos.actions import Blink
from pyglet.window import key as k

from image import Image
from background import BackgroundLayer
from stats import stats
from actor import Hero
from enemy import Bird


class GameScene(Scene):
    def __init__(self):
        super().__init__()

        # 游戏场景---有游戏层, 灰色背景, 地面背景层
        self.add(GameLayer(), z=10)
        self.add(BackgroundLayer(), z=2, name="background")
        self.background_color1 = ColorLayer(255, 255, 255, 255)
        self.background_color2 = ColorLayer(0, 0, 0, 255)
        self.background_color2.opacity = 0
        self.add(self.background_color1, z=0)
        self.add(self.background_color2, z=1)


class GameLayer(Layer):
    is_event_handler = True

    def __init__(self):
        super().__init__()

        # 状态参数
        self.stats = stats

        # 创建分数条
        self.create_score_text()

        # 创建dinosaur
        self.hero = Hero()
        self.add(self.hero)

        # 管理鸟类
        self.create_elapsed = 0
        self.birds = []

        # 管理背景颜色
        self.background_color_lock = False

        # 更新生命值
        self.life_icon_lst = []

        # 更新无敌时间
        self.invincible_elapsed = 0

        # 碰撞
        self.collide_manager = CollisionManagerGrid(0, director.get_window_size()[0],
                                                    0, 500,
                                                    self.hero.width * 1.25,
                                                    self.hero.height * 1.25)
        # dash提示
        self.create_dash_prompt()

        self.schedule(self.update)

    def update(self, dt):
        # background move
        self.parent.get("background").update()
        # dinosaur move
        self.hero._update()
        # 更新分数
        self.update_score()
        # 创建鸟类
        self.create_birds()
        # 更新背景色
        self.update_background_color()
        # 判断游戏是否结束
        self.judge_success()
        self.judge_fail()
        # 更新生命值
        self.update_life()
        # 更新碰撞
        self.update_collide()

    def create_score_text(self):
        self.score_text = Label("",
                                font_size=30,
                                color=(128, 128, 128, 255),
                                anchor_x="right",
                                anchor_y="top")
        self.score_text.position = 1320, 720
        self.add(self.score_text)

    def update_score(self):
        self.stats.score += 0.5
        self.score_text.element.text = "Target Score: 4514 - Score: " + str(int(self.stats.score))

    def create_birds(self):
        self.create_elapsed += 0.1
        if self.create_elapsed >= 12:
            direction = ["left", "right"]
            temp = Bird(random.choice(direction))
            self.add(temp)
            self.birds.append(temp)
            self.create_elapsed = 0

    def update_background_color(self):
        if 2000 > self.stats.score >= 1000 and not self.background_color_lock:
            self.parent.background_color2.do(FadeIn(1))
            self.background_color_lock = True
        elif 3000 > self.stats.score >= 2000 and self.background_color_lock:
            self.parent.background_color2.do(FadeOut(1))
            self.background_color_lock = False
        elif 4000 > self.stats.score >= 3000 and not self.background_color_lock:
            self.parent.background_color2.do(FadeIn(1))
            self.background_color_lock = True
        elif self.stats.score >= 4000 and self.background_color_lock:
            self.parent.background_color2.do(FadeOut(1))
            self.background_color_lock = False

    def judge_success(self):
        if self.stats.score >= 4514:
            print("sldfjlsdkfj")

    def update_life(self):
        if len(self.life_icon_lst) < self.hero.life:
            life_icon = Sprite(Image.dinosaur_run_set[0])
            life_icon.image_anchor = (0, life_icon.height)
            life_icon.scale = 0.4
            life_icon.position = len(self.life_icon_lst) * life_icon.width, \
                                 director.get_window_size()[1]
            self.life_icon_lst.append(life_icon)
            print(len(self.life_icon_lst), self.hero.life)
            self.add(life_icon)
        else:
            for i in range(len(self.life_icon_lst) - self.hero.life):
                self.life_icon_lst[len(self.life_icon_lst) - 1 - i].kill()
                # 这里要从list解除引用, 否则会对同一个sprite进行多次kill, 而报错
                del self.life_icon_lst[len(self.life_icon_lst) - 1 - i]

    def update_collide(self):
        if not self.hero.invincible:
            self.collide_manager.clear()

            for _, i in self.children:
                if isinstance(i, (Hero, Bird)):
                    self.collide_manager.add(i)

            for collided in self.collide_manager.objs_colliding(self.hero):
                self.hero.life -= 1
                self.hero.invincible = True
                self.hero.do(Blink(2, 0.5))
                break
        else:
            self.invincible_elapsed += 0.1
            if self.invincible_elapsed > 10:
                self.hero.invincible = False
                self.invincible_elapsed = 0

    def judge_fail(self):
        if self.hero.life == 0:
            self.unschedule(self.update)
            self.over_prompt()

    def on_key_press(self, key, modifier):
        self.key = key
        if self.hero.life == 0 and self.key == k.R:
            self.restart()
            print("restart")

    def restart(self):
        self.stats.restart()
        self.hero.restart()
        self.birds_restart()
        self.remove(self.over_label)
        self.schedule(self.update)

    def birds_restart(self):
        for _, i in self.children:
            if isinstance(i, Bird):
                self.remove(i)

    def on_enter(self):
        super().on_enter()
        self.key = None

    def over_prompt(self):
        w, h = director.get_window_size()
        self.over_label = Label("press R to restart",
                                position=(w / 2, h / 2),
                                color=(127, 127, 127, 200),
                                font_size=50,
                                anchor_x="center",
                                anchor_y="center")
        self.add(self.over_label)
        self.over_label.do(FadeIn(1))

    def create_dash_prompt(self):
        w, h = director.get_window_size()
        self.dash_label = Label("press D to Dash(or Teleport)",
                                position=(w, h - 100),
                                color=(127, 127, 127, 200),
                                font_size=20,
                                anchor_x="right",
                                anchor_y="center")
        self.add(self.dash_label)
