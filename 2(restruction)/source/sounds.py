from pygame import mixer


class Sounds(object):
    sound_reap = mixer.Sound("./resources/sounds/reap.wav")
    sound_seed = mixer.Sound("./resources/sounds/seed.wav")
    sound_button = mixer.Sound("./resources/sounds/button.wav")
    sound_expand = mixer.Sound("./resources/sounds/terrain.wav")


mixer.music.load("./resources/sounds/nyxkn_music.ogg")
mixer.music.play(-1)
