import pygame


class Music(object):
    ELAPSED_TIME = 50

    def __init__(self):
        # self.music = "his_theme.mp3"
        # self.music = "The_Magic_Inside.mp3"
        self.music = "your_name.mp3"
        pygame.mixer.music.load(self.music)
        pygame.mixer.music.play()

        self.elapsed = self.ELAPSED_TIME

    def pause(self):
        pygame.mixer.music.pause()

    def resume(self):
        pygame.mixer.music.unpause()

    def elapse(self, more_punish=False):  # 按错会减更多时间
        if more_punish:
            self.elapsed -= 100
        self.elapsed -= 1
        if self.elapsed <= 0:
            self.pause()

    def compensate_elapse(self):
        if self.elapsed >= 0:
            self.elapsed += self.ELAPSED_TIME
        else:
            self.elapsed = self.ELAPSED_TIME
        self.resume()
