"""还需要调整功能"""

from math import sin, cos, radians

from cocos.director import director
from cocos.scene import Scene
from cocos.layer import Layer, ColorLayer
from cocos.sprite import Sprite
from cocos.text import Label
from cocos.draw import Line


class Tree(Sprite):
    def __init__(self, val, left=None, right=None, parent_=None, level=0):
        super().__init__("circle.png")
        self.val = val
        self.left = left
        self.right = right
        self.parent_ = parent_
        self.level = level

        self.flare_angle = 140 / 2 ** level  # 张角
        self.len_line = 150 - level * 15
        self.delta_x = int(sin(radians(self.flare_angle / 2)) * self.len_line)
        self.delta_y = int(cos(radians(self.flare_angle / 2)) * self.len_line)

        self.add(Label(f"{self.val}", font_size=20, color=(0, 0, 0, 255),
                       anchor_x="center", anchor_y="center"))

    def draw_(self):
        if not self.parent_:
            w, h = director.get_window_size()
            self.position = w / 2, h - 50
        else:
            if self.parent_.left is self:
                sign = -1
            else:
                sign = 1

            self.position = (self.parent_.position[0] + self.parent_.delta_x * sign,
                             self.parent_.position[1] - self.parent_.delta_y)
            self.parent.add(Line(self.position, self.parent_.position, color=(0, 0, 0, 255)), z=0)


class VisualTreesScene(Scene):
    def __init__(self):
        super().__init__()

        self.add(ColorLayer(100, 100, 100, 255))
        self.add(VisualTreesLayer())



class VisualTreesLayer(Layer):
    def __init__(self):
        super().__init__()

        self.root = self.build_trees()
        self.draw_trees(self.root)

        print("前序")
        pre_traverse(self.root)
        print("\n", "\r中序")
        mid_traverse(self.root)
        print("\n", "\r后序")
        post_traverse(self.root)

    @staticmethod
    def build_trees():
        trees = [None, 1, 2, 3, 4, 5, 6, 1, 2, 3, 4, None, 6, 1, 2, 3, 4, None, 5, 6, 7, 8, 9, 19, 20, 20, 20, 6, 7, 8,
                 9, 19,
                 20, 20, 20, None]
        origin_root = Tree(trees[1])

        def helper(root, pos):
            if root:
                if pos * 2 < len(trees) and trees[pos * 2]:
                    root.left = Tree(val=trees[pos * 2], parent_=root, level=root.level + 1)
                    helper(root.left, pos * 2)
                if pos * 2 + 1 < len(trees) and trees[pos * 2 + 1]:
                    root.right = Tree(val=trees[pos * 2 + 1], parent_=root, level=root.level + 1)
                    helper(root.right, pos * 2 + 1)

        helper(origin_root, 1)
        return origin_root

    def draw_trees(self, root):
        if root:
            self.add(root, z=10)
            root.draw_()  # 太早draw, left等还没绑定
            self.draw_trees(root.left)
            self.draw_trees(root.right)


def pre_traverse(root):
    if root:
        print(root.val, end=" ")
        pre_traverse(root.left)
        pre_traverse(root.right)


def mid_traverse(root):
    if root:
        mid_traverse(root.left)
        print(root.val, end=" ")
        mid_traverse(root.right)


def post_traverse(root):
    if root:
        post_traverse(root.left)
        post_traverse(root.right)
        print(root.val, end=" ")


if __name__ == '__main__':
    director.init(width=1000, height=600)
    director.run(VisualTreesScene())

