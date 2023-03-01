from cocos.text import Label

from foods import *
from Tool.my_cocos_tools.graphs import *
from sound import Sound


class GameScene(Scene):
    """
    简单的老爹汉堡店, 实现了:
        1. 菜单滑动
        2. 老八配音
        3. 食物DIY
        4. 上菜结束音效
    """

    def __init__(self):
        super().__init__()

        self.add(GameLayer())


class GameLayer(Layer):
    is_event_handler = True

    def __init__(self):
        super().__init__()

        # 滑动配置
        w, h = director.get_window_size()
        self.start = w - 50, 100
        self.end = w - 50, h - 100
        self.from_start_to_end = self.end[1] - self.start[1]
        self.slide_line = Line(self.start, self.end, (0, 255, 255, 255), 3)
        self.add(self.slide_line)

        self.slide_block = FilledRect((self.start[0] - 10, self.start[1] + 20), 20, 20, color=(0, 255, 0, 255))
        self.add(self.slide_block)
        self.slide_block_rect = self.slide_block.get_rect()

        self.mouse_pos = 0, 0
        self.can_move = False
        self.schedule(self.update_move)

        # 加载食物
        foods = [Beef, Butter, Onion, Tomato,
                 Tomatojam, Vegetable, Topbread, Bottombread,
                 Cucumber]
        self.foods = []
        for food in foods:
            temp = food()
            self.foods.append(temp)
            self.add(temp)

        self.set_position()
        self.current_food = None

        # show_button
        self.show_button()

        self.elapsed = 0
        self.schedule(self.begin)

    def begin(self, dt):
        self.elapsed += 0.1
        if self.elapsed > 100:
            Sound.beginning.play()
            self.unschedule(self.begin)

    def update_move(self, dt):
        if self.can_move and self.check_move_valid():
            self.slide_block.y = self.mouse_pos[1] - self.slide_block_rect.height / 2
            self.slide_block_rect.y = self.mouse_pos[1] - self.slide_block_rect.height / 2

            self.set_position()

    def on_mouse_drag(self, x, y, button, delta_x, delta_y, modifier):
        self.mouse_pos = x, y
        # 如果选中了食物
        if self.current_food:
            self.current_food.position = x, y

    def on_mouse_press(self, x, y, button, modifier):
        self.update_collision()
        self.mouse_pos = x, y
        if self.slide_block_rect.contains(*self.mouse_pos):
            self.can_move = True

        for food in self.foods:
            if food.get_rect().contains(*self.mouse_pos):
                temp = type(food)()
                temp.position = self.mouse_pos
                self.current_food = temp
                self.add(temp)
                temp = eval(f"Sound.{food.name}.play()")
                temp.volume = 2

    def on_mouse_release(self, x, y, button, modifier):
        self.can_move = False
        self.current_food = None

    def on_mouse_motion(self, x, y, *_):
        self.mouse_pos = x, y

    def check_move_valid(self):
        if self.start[1] < self.mouse_pos[1] < self.end[1]:
            return True
        return False

    def set_position(self):
        gap = 400
        total_len = len(self.foods) * gap
        ratio = (self.slide_block.mid_pos[1] - self.start[1]) / self.from_start_to_end

        # 基准牛排位置
        self.foods[0].x = director.get_window_size()[0] / 2 \
                          - ratio * total_len
        for idx, food in enumerate(self.foods[1:]):
            food.x = self.foods[0].x \
                     + gap * idx \
                     + food.width / 2 \
                     + self.foods[0].width / 2
            if isinstance(food, Butter):
                food.x += 100

    def show_button(self):
        self.label = Label("上交作业",
                           position=(100, 100),
                           font_size=30,
                           anchor_x="center",
                           anchor_y="center")
        self.label_rect = Rect(self.label.x - self.label.element.content_width / 2,
                               self.label.y - self.label.element.content_height / 2,
                               self.label.element.content_width,
                               self.label.element.content_height)
        self.add(self.label)

    def update_collision(self):
        if self.label_rect.contains(*self.mouse_pos):
            Sound.over.play()

