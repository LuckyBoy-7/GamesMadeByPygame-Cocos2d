"""
用mask当蒙版, 当敲上正确的字母时才创建对象

生成一个环
敌人一直走, 知道我出现在他前方n个格子处他就调转方向
我打字的时候维护一个serial_typing: int
随时间不断递减 >= 0, 打字会递增, 超过阈值时加速 + hint
"""
from cocos.layer import Layer
from cocos.text import Label
from pyglet.window import key

from settings import Settings



