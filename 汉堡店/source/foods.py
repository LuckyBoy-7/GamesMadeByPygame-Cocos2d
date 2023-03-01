from cocos.sprite import Sprite
from cocos.director import director

from image import Image


class Food(Sprite):

    def __init__(self, img):
        super().__init__(img)

        # 更新位置
        self.pivot_y = director.get_window_size()[1] - 130
        self.position = 0, self.pivot_y


class Beef(Food):
    def __init__(self):
        super().__init__(Image.beef)
        self.name = "beef"


class Butter(Food):
    def __init__(self):
        super().__init__(Image.butter)
        self.name = "butter"


class Onion(Food):
    def __init__(self):
        super().__init__(Image.onion)
        self.name = "onion"


class Tomato(Food):
    def __init__(self):
        super().__init__(Image.tomato)
        self.name = "tomato"


class Tomatojam(Food):
    def __init__(self):
        super().__init__(Image.tomato_jam)
        self.name = "tomato_jam"


class Vegetable(Food):
    def __init__(self):
        super().__init__(Image.vegetable)
        self.name = "vegetable"


class Bottombread(Food):
    def __init__(self):
        super().__init__(Image.bottom_bread)
        self.name = "bread"


class Topbread(Food):
    def __init__(self):
        super().__init__(Image.top_bread)
        self.name = "bread"

class Cucumber(Food):
    def __init__(self):
        super().__init__(Image.cucumber)
        self.name = "cucumber"
