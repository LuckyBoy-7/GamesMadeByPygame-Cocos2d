from cocos.layer import Layer, ColorLayer
from cocos.scene import Scene
from cocos.text import Label
from cocos.actions import *
from cocos.collision_model import CollisionManagerGrid
from cocos.actions import Blink
from pyglet.window import key as k
from cocos.draw import Line
from cocos.batch import BatchNode

from stats import stats
from actor import Heart
from enemy import *
from broken import Broken
from level import Level
from sound import Sound


class GameScene(Scene):
    def __init__(self):
        super().__init__()

        # 游戏场景---有游戏层
        self.add(GameLayer(), z=75, name="GameLayer")
        self.add(ColorLayer(0, 0, 0, 255), z=0)


class GameLayer(Layer):
    is_event_handler = True

    def __init__(self):
        super().__init__()

        # 状态参数
        self.stats = stats

        # 基本参数
        self.w, self.h = director.get_window_size()

        # 创建heart
        self.heart = Heart()
        self.add(self.heart, z=100)

        # 创建sans
        self.create_sans()

        # 创建生命条
        self.hp_line = Line((1000, 50), (1200, 50), (255, 255, 30, 255), 25)
        self.add(self.hp_line, z=75)
        self.create_hp_ratio_label()

        # 更新无敌时间
        self.invincible_elapsed = 0

        # 碰撞
        self.collide_manager = CollisionManagerGrid(0, self.w,
                                                    0, 500,
                                                    self.heart.width * 1.25,
                                                    self.heart.height * 1.25)

        # 边界线
        self.up_edge = 450
        self.down_edge = 100
        self.line1 = Line((0, self.up_edge), (self.w, self.up_edge), (255, 255, 255, 255), 3)
        self.line2 = Line((0, self.down_edge), (self.w, self.down_edge), (255, 255, 255, 255), 3)
        self.add(self.line1, z=75)
        self.add(self.line2, z=75)
        # 创建蒙版
        self.mask1 = ColorLayer(0, 0, 0, 255)
        self.mask2 = ColorLayer(0, 0, 0, 255)
        self.mask1.height = 100
        self.mask2.position = 0, 450
        self.add(self.mask1, z=50)
        self.add(self.mask2, z=50)

        # 创建choice
        self.create_choice()
        self.choice_time = False

        # fight_duration
        self.fight_elapsed = 0

        # attack_effect
        self.attack_idx = 0
        self.attack = Sprite(Image.attack[self.attack_idx])
        self.add(self.attack, 76)
        self.attack.position = self.w / 2, 600
        self.attack_elapsed = 0
        self.is_attack = False
        self.attack.opacity = 0

        # 嘲讽
        self.mock_label = self.create_mock_label()
        self.create_mock_words()

        # 对战事件
        self.fighting = True
        self.level = Level(self.fighting, self.up_edge, self.down_edge, self)

        # bgm
        Sound.enter.play()
        self.bgm = Sound.bgm.play()
        self.bgm.loop = True

        self.schedule(self.update)

        # test
        # self.test2()

    def update(self, dt):
        # Heart move
        self.heart._update()
        # 判断游戏是否结束
        self.judge_fail()
        # 更新生命值
        self.update_life()
        # 更新碰撞
        self.update_collide()
        # 更新选择
        self.update_choice()
        # 处理对战事件
        self.level.update(self.choice_time, self.fighting)
        # 处理攻击特效
        self.show_attack()

        # test
        # self.test1()

    # def test1(self):
    #     self.test_elapsed += 1
    #     if self.test_elapsed > 100:
    #         self.test_elapsed = 0
    #
    # def test2(self):
    #     self.test_elapsed = 1
    #     # self.fight_elapsed = 90

    def update_life(self):
        ratio = self.heart.hp / 96
        self.hp_line.end = (1000 + 200 * ratio, 50)
        self.hp_ratio_label.element.text = f"{self.heart.hp}/88"

    def create_hp_ratio_label(self):
        self.hp_ratio_label = Label(f"{self.heart.hp}/96",
                                    position=(900, 50),
                                    font_name="Determination Mono",
                                    color=(238, 62, 221, 255),
                                    font_size=25,
                                    anchor_x="center",
                                    anchor_y="center")
        self.add(self.hp_ratio_label, z=75)

    def update_collide(self):
        if not self.heart.invincible:
            self.collide_manager.clear()

            for _, i in self.children:
                if isinstance(i, Bubble):
                    self.collide_manager.add(i)
                elif isinstance(i, BatchNode):
                    for j in i.children:
                        self.collide_manager.add(j[1])

            for collided in self.collide_manager.objs_colliding(self.heart):
                self.heart.hp -= 3
                self.heart.invincible = True
                self.heart.do(Blink(2, 0.5))
                Sound.hurt.play()
                break
        else:
            self.invincible_elapsed += 0.1
            if self.invincible_elapsed > 10:
                self.heart.invincible = False
                self.invincible_elapsed = 0

    def judge_fail(self):
        if self.heart.hp <= 0:
            self.heart.opacity = 0
            self.add(Broken(self.heart.position), z=75)
            self.unschedule(self.update)
            self.over_prompt()
            self.determination = Sound.determination.play()


    """on_key_press"""
    def on_key_press(self, key, modifier):
        # 调试
        if key == k.Q:
            self.fight_elapsed = 130
        self.key = key
        if self.heart.hp <= 0 and self.key == k.R:
            self.determination.pause()
            self.restart()
            print("restart")
        elif self.choice_time:
            if self.key == k.LEFT:
                self.fight_label.opacity = 255
                self.escape_label.opacity = 100
            elif self.key == k.RIGHT:
                self.fight_label.opacity = 100
                self.escape_label.opacity = 255
            elif self.key == k.C:
                if self.fight_label.opacity == 255:
                    print("fight")
                    self.is_attack = True
                    self.sans_sidestep()
                    self.sans_mock("fight")
                    Sound.attack.play()
                    mock = Sound.mock.play()
                    mock.volume = 3

                else:
                    print("escape")
                    self.sans_mock("escape")
                self.choice_time = False
                self.schedule(self.update)
                self.fighting = True

    def restart(self):
        self.stats.restart()
        self.heart.restart()
        self.remove(self.over_label)
        self.schedule(self.update)
        self.level.restart()

    def show_attack(self):
        if self.is_attack:
            self.attack.opacity = 255
            self.attack_elapsed += 1
            if self.attack_idx < len(Image.attack) - 1 and self.attack_elapsed > 15:
                self.attack_idx += 1
                self.attack_elapsed = 0
            elif self.attack_idx == len(Image.attack) - 1:
                self.attack_idx = 0
                self.attack.opacity = 0
                self.is_attack = False
            self.attack.image = Image.attack[self.attack_idx]

    def on_enter(self):
        super().on_enter()
        self.key = None

    def over_prompt(self):
        w, h = self.w, self.h
        self.over_label = Label("Don't lose your resolution(R)",
                                position=(w / 2, h / 2),
                                font_name="Determination Mono",
                                color=(230, 230, 230, 160),
                                font_size=50,
                                anchor_x="center",
                                anchor_y="center")
        self.add(self.over_label, z=1000)
        self.over_label.do(FadeIn(1))

    def update_choice(self):
        if not self.choice_time:
            self.fight_elapsed += 0.1
            if self.fight_elapsed > 120:
                self.fight_elapsed = 0

                self.heart.position = self.heart.position_backup
                self.unschedule(self.update)
                self.choice_time = True
                self.level.handle_fight_exit()

    def create_choice(self):
        w = self.w / 2
        self.fight_label = Label("Fight",
                                 position=(w - 100, 50),
                                 font_name="Determination Mono",
                                 color=(247, 119, 32, 255),
                                 font_size=25,
                                 anchor_x="center",
                                 anchor_y="center")
        self.escape_label = Label("Escape",
                                  position=(w + 100, 50),
                                  font_name="Determination Mono",
                                  color=(247, 119, 32, 100),
                                  font_size=25,
                                  anchor_x="center",
                                  anchor_y="center")

        self.add(self.fight_label, z=75)
        self.add(self.escape_label, z=75)

    def create_sans(self):
        w = self.w / 2
        self.sans_lower_part = Sprite(Image.sans_lower_part)
        self.sans_middle_part = Sprite(Image.sans_middle_part)
        self.sans_upper_part = Sprite(Image.sans_upper_part)
        self.sans_upper_part.position = w - 5, 625
        self.sans_middle_part.position = w - 5, 576
        self.sans_lower_part.position = w, 520

        self.sans_upper_part.do(Repeat(JumpBy((10, 0), -7, 1, 1)
                                       + JumpBy((-10, 0), -7, 1, 1)))
        self.sans_middle_part.do(Delay(0.02) + Repeat(JumpBy((10, 0), -7, 1, 1)
                                                      + JumpBy((-10, 0), -7, 1, 1)))

        self.add(self.sans_upper_part, z=76)
        self.add(self.sans_middle_part, z=75)
        self.add(self.sans_lower_part, z=75)

    def sans_sidestep(self):
        for i in [self.sans_upper_part,
                  self.sans_middle_part,
                  self.sans_lower_part]:
            i.actions.clear()

        w = self.w / 2
        self.sans_upper_part.position = w - 5, 625
        self.sans_middle_part.position = w - 5, 575
        self.sans_lower_part.position = w, 520

        self.sans_lower_part.do(MoveBy((-100, 0), 0.4) + MoveBy((100, 0), 0.4))

        self.sans_upper_part.do(MoveBy((-100, 0), 0.4) + MoveBy((100, 0), 0.4) + Repeat(JumpBy((10, 0), -7, 1, 1)
                                                                                        + JumpBy((-10, 0), -7, 1, 1)))
        self.sans_middle_part.do(
            MoveBy((-100, 0), 0.4) + MoveBy((100, 0), 0.4) + Delay(0.02) + Repeat(JumpBy((10, 0), -7, 1, 1)
                                                                                  + JumpBy((-10, 0), -7, 1, 1)))

    def sans_mock(self, mock_type):
        Sound.mock.play()
        if mock_type == "fight":
            self.mock_label.element.text = choice(self.mock_fight_words)
            self.mock_label.do(FadeIn(2))
        else:
            self.mock_label.element.text = choice(self.mock_escape_words)
            self.mock_label.do(FadeIn(2))
        self.mock_label.do(FadeOut(10))

    def create_mock_label(self):
        w, h = self.w, self.h
        label = Label("",
                      position=(w / 2 + 100, h - 20),
                      font_name="Determination Mono",
                      color=(250, 250, 250, 230),
                      font_size=20,
                      anchor_x="center",
                      anchor_y="center")
        self.add(label, z=1000)
        return label

    def create_mock_words(self):
        self.mock_escape_words = ["Go ahead and try to hit me if you're able",
                                  "So let's go,let the room get chiller"]

        self.mock_fight_words = ["Do you just like the feeling of your sins crawling on your back?",
                                 "Always wondered why people never use their strongest attack first",
                                 "Think that you can try[MERCY] and spare me like I'm some pawn"]

    def over(self):
        self.add(OverLayer())


class OverScene(Scene):
    def __init__(self):
        super().__init__()

        self.add(OverLayer())
        Sound.birthday.play()

class OverLayer(Layer):
    def __init__(self):
        super().__init__()

        center = director.get_window_size()[0] / 2
        self.line1 = self.create_label("beauty the sky is", (200, 400), 2)
        self.line2 = self.create_label("ice buried in mess", (210, 320), 4)
        self.line3 = self.create_label("return might be a choice", (260, 220), 6)
        self.line4 = self.create_label("towards with friends", (225, 130), 8)

        self.line5 = self.create_label("healed by truly warmth", (1080, 400), 10)
        self.line6 = self.create_label("defeat's only process", (1070, 320), 12)
        self.line7 = self.create_label("aligned the inner faith", (1090, 220), 14)
        self.line8 = self.create_label("yet the sun rises", (1045, 130), 16)

        self.create_label("Our", (center, 400), 20, 50)
        self.create_label("Best", (center, 300), 22, 50)
        self.create_label("Friend", (center, 200), 24, 50)

    def create_label(self, words, pos, appear_time, size=20):
        label = Label(f"{words}",
                      position=pos,
                      font_name="Determination Mono",
                      color=(230, 230, 230, 255),
                      font_size=size,
                      anchor_x="center",
                      anchor_y="center")
        self.add(label)
        label.opacity = 0
        label.do(Delay(appear_time + 3) + FadeIn(1))
        return label
