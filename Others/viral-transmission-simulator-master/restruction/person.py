import pygame
from pygame.sprite import Sprite
import random

from setting import Settings


class Person(Sprite):

    # 构造函数传入配置对象，和窗口对象
    def __init__(self, settingInfo, screen, grids):
        super(Person, self).__init__()
        self.screen = screen  # 保存screen 对象
        self.grids = grids

        # 用随机值初始化人员位置
        self.x = random.randint(50, settingInfo.screen_width - 100)
        self.y = random.randint(50, settingInfo.screen_height - 100)
        self.pos = self.get_pos(self.x, self.y, settingInfo)

        # 初始化人员位置和大小
        self.rect = pygame.Rect(self.x, self.y, settingInfo.person_size,
                                settingInfo.person_size)

        # 初始化人员颜色
        self.color = settingInfo.person_color

        # 是否被感染标识，默认为正常人员（非感染）
        self.infected = False

    # 刷新函数：传入设置和所有人员数组
    def update_position(self, settingInfo, persons):

        # 随机设置人员移动目的地（不超过最大步长）
        range = settingInfo.person_moving_range
        self.y += random.randint(-range, range)
        if self.y >= settingInfo.screen_height:
            self.y = settingInfo.screen_height - 1
        elif self.y < 0:
            self.y = 0
        self.x += random.randint(-range, range)
        if self.x >= settingInfo.screen_width:
            self.x = settingInfo.screen_width - 1
        elif self.x < 0:
            self.x = 0

        # 通过随机值刷新人员位置
        self.rect = pygame.Rect(self.x, self.y, settingInfo.person_size,
                                settingInfo.person_size)
        new_pos = self.get_pos(self.x, self.y, settingInfo)
        if new_pos != self.pos:
            self.grids[self.pos].remove(self)
            self.grids[new_pos].add(self)
            self.pos = new_pos

    def update_color(self, settingInfo, persons):

        # 绘制人员
        pygame.draw.rect(self.screen, self.color, self.rect)

        # 如果人员已经被感染 直接返回
        if self.infected is False:
            return

        # 循环被接触的人员，根据传染率，设定被传染人员的状态
        for person in (person for person in self.grids[self.pos]
                       if person != self and self.rect.colliderect(person.rect)):
            # 配置文件中传染率 infect_rate是一个数值，如果值是50，那么被传染概率就是 1/50，也就是2%
            if random.randint(0, settingInfo.infect_rate) == 1:
                # 执行传染函数
                person.infect(settingInfo)

    def get_pos(self, x, y, settings):
        gap_x, gap_y = settings.column_gap, settings.row_gap
        return x // gap_x, y // gap_y



    # 绘制自己
    def draw_person(self):
        # 其实就是一个小方框，也可以是一张图，喜欢的小伙伴根据自己的喜好可以修改
        pygame.draw.rect(self.screen, self.color, self.rect)

    # 被感染执行函数
    def infect(self, settingInfo):
        # 颜色设置为 被感染的颜色
        self.color = settingInfo.infect_person_color
        # 被感染标识设置为true
        self.infected = True
