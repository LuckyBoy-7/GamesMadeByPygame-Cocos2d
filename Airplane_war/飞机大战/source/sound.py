import pygame
from collections import defaultdict


class DummySound:
    def play(self, *args):
        pass
    
    def pause(self, *args):
        pass
    
    def unpause(self, *args):
        pass
    
    def fadeout(self, *args):
        pass


class Sound:
    def __init__(self):
        # 加载音乐
        try:
            pygame.mixer.music.load("../res/sound/game_music.wav")
        except pygame.error as e:
            self.music = DummySound()
            print(e)
        else:
            self.music = pygame.mixer.music

        # 加载音效
        self.sounds = defaultdict(DummySound)

        sounds_name = ["bullet", "enemy1_down", "enemy2_down", "enemy3_down", "game_over"]
        try:
            for sound in sounds_name:
                self.sounds[sound] = pygame.mixer.Sound(sound.join(["../res/sound/", ".wav"]))
        except pygame.error as e:
            print(e)
        

    def play(self, name):
        if name == "bg":
            self.music.play(-1)
        else:
            self.sounds[name].play()

    def pause(self, name):
        if name == "bg":
            self.music.pause()

    def unpause(self, name):
        if name == "bg":
            self.music.unpause()

    def fadeout(self, name):
        if name == "bg":
            self.music.fadeout(100)
