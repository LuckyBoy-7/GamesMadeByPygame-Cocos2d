from cocos.director import director

from game import GameScene

# 分辨率记得改
if __name__ == '__main__':
    director.init(
        caption="邦昊的假期料理",
        height=1080,
        width=1920,
        # fullscreen=True
    )
    director.run(GameScene())
