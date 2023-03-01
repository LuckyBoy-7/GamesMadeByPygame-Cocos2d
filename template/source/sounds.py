from pygame import mixer


class Sounds(object):
    sound1 = mixer.Sound("./resources/sounds/xxx")
    sound1.set_volume(2)


# mixer.music.load("./resources/sounds/bgm.mp3")
# mixer.music.play(-1)
