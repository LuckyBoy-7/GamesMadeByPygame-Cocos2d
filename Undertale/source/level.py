from cocos.batch import BatchNode
from cocos.text import Label
from cocos.actions import FadeIn, FadeOut, Delay

from enemy import *
from sound import Sound


class Level:
    def __init__(self, fighting, up_edge, down_edge, parent):
        self.up_edge = up_edge
        self.down_edge = down_edge
        self.parent = parent
        self.fight_level = 0
        self.final_part = False
        self.mess_time = False

        # test
        # self.fight_level = 8
        # self.final_part = True

    def update(self, choice_time, fighting):
        self.fighting = fighting
        self.handle_fight()

    def handle_fight(self):
        """
            elude bubbles gathering,    1(0)
            elude bones1,               2(1)
            elude bones2,               3(2)
            elude bones3,               4(3)
            exchange key order:
                elude bubbles gathering,    1(0)
                elude bones1,               2(1)
                elude bones2,               3(2)
                elude bones3,               4(3)
            Truly wishes                9(8)
        """
        if self.fighting:
            # 处理普通事件
            if not self.final_part:
                if self.fight_level % 4 == 0:
                    self.enter_level1()
                elif self.fight_level % 4 == 1:
                    self.enter_level2()
                elif self.fight_level % 4 == 2:
                    self.enter_level3()
                elif self.fight_level % 4 == 3:
                    self.enter_level4()
                    self.final_part = True
            # 处理混乱事件和结束事件
            else:
                self.mess_time = True
                if self.fight_level == 8:
                    self.enter_level5()
                    print("finalpart")
                else:
                    if self.fight_level % 4 == 0:
                        self.enter_level1()
                    elif self.fight_level % 4 == 1:
                        self.enter_level2()
                    elif self.fight_level % 4 == 2:
                        self.enter_level3()
                    elif self.fight_level % 4 == 3:
                        self.enter_level4()

            self.parent.fighting = False

    def enter_level1(self):
        for i in range(15):
            self.parent.add(Bubble(self.up_edge, self.down_edge))

    def exit_level1(self):
        temp = len(self.parent.children)
        for idx, i in enumerate(self.parent.children[::-1]):
            if isinstance(i[1], Bubble):
                self.parent.children.pop(temp - 1 - idx)

    def enter_level2(self):
        self.bone_batchnode1 = BatchNode()
        temp1 = 0  # height
        temp2 = 0  # frequency
        bone_numbers = 70
        T = 10
        for i in range(bone_numbers):
            self.bone_batchnode1.add(Bone(self.up_edge, self.down_edge, temp1, temp2, True, 1))
            self.bone_batchnode1.add(Bone(self.up_edge, self.down_edge, temp1, temp2, False, 1))
            temp1 += 3.14 / T
            temp2 += 1
        self.parent.add(self.bone_batchnode1)

    def exit_level2(self):
        for idx, child in enumerate(self.parent.children):
            if isinstance(child[1], BatchNode):
                self.parent.children.pop(idx)

    def enter_level3(self):
        self.bone_batchnode = BatchNode()
        temp1 = 0  # height
        temp2 = 0  # frequency
        bone_numbers = 30
        T = 10
        for i in range(bone_numbers):
            self.bone_batchnode.add(Bone(self.up_edge, self.down_edge, temp1, temp2, True, 2))
            self.bone_batchnode.add(Bone(self.up_edge, self.down_edge, temp1, temp2, False, 2))
            temp1 += 3.14 / T
            temp2 += 1
        self.parent.add(self.bone_batchnode)

    def exit_level3(self):
        for child in self.parent.children:
            if isinstance(child[1], BatchNode):
                self.parent.remove(self.bone_batchnode)

    def enter_level4(self):
        self.bone_batchnode = BatchNode()
        temp1 = 0  # height
        temp2 = 0  # frequency
        bone_numbers = 45
        for i in range(bone_numbers):
            self.bone_batchnode.add(Bone(self.up_edge, self.down_edge, temp1, temp2, True, 3))
            self.bone_batchnode.add(Bone(self.up_edge, self.down_edge, temp1, temp2, False, 3))
            temp1 += 2
            temp2 += 1
        self.parent.add(self.bone_batchnode)

    def exit_level4(self):
        for child in self.parent.children:
            if isinstance(child[1], BatchNode):
                self.parent.remove(self.bone_batchnode)

    def enter_level5(self):
        w, h = director.get_window_size()
        self.label1 = Label("亲爱的君豪, 希望你这次游玩开心, 第一次做有点次",
                            position=(w / 2, h / 2),
                            font_name="Determination Mono",
                            color=(250, 250, 250, 250),
                            font_size=30,
                            anchor_x="center",
                            anchor_y="center")
        self.label2 = Label("在这里祝你生日快乐, 天天都有好心情",
                            position=(w / 2, h / 2 - 50),
                            font_name="Determination Mono",
                            color=(250, 250, 250, 250),
                            font_size=30,
                            anchor_x="center",
                            anchor_y="center")
        self.label3 = Label("                    -----BEST WISHES",
                            position=(w / 2, h / 2 - 100),
                            font_name="Determination Mono",
                            color=(250, 250, 250, 250),
                            font_size=30,
                            anchor_x="center",
                            anchor_y="center")

        self.label1.do(FadeIn(2) + FadeOut(3))
        self.label2.do(FadeIn(2) + FadeOut(3))
        self.label3.do(FadeIn(2) + FadeOut(3))
        self.parent.add(self.label1, z=1000)
        self.parent.add(self.label2, z=1000)
        self.parent.add(self.label3, z=1000)

        self.parent.sans_lower_part.do(Delay(2) + FadeOut(3))
        self.parent.sans_middle_part.do(Delay(2) + FadeOut(3))
        self.parent.sans_upper_part.do(Delay(2) + FadeOut(3))
        self.parent.heart.do(Delay(2) + FadeOut(3))

        Sound.birthday.play()

        self.parent.bgm.pause()
        self.parent.unschedule(self.parent.update)
        self.parent.over()

    def handle_fight_exit(self):
        if self.fight_level % 4 == 0:
            self.exit_level1()
        elif self.fight_level % 4 == 1:
            self.exit_level2()
        elif self.fight_level % 4 == 2:
            self.exit_level3()
        elif self.fight_level % 4 == 3:
            self.exit_level4()
        self.fight_level += 1

    def restart(self):
        self.handle_fight_exit()

        # 原本进场直接开始所以是0, 现在选择后开始, 所以要-1, 所以没bug
        self.fight_level = -1
        self.final_part = False
        self.mess_time = False
