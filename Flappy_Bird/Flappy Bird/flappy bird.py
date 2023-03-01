import pygame
import sys
import random

class Bird(object):
    def __init__(self):
        self.birdRect = pygame.Rect(65,206,40,40 - 10.5)
        self.birdStatus = [pygame.image.load("1.png"), pygame.image.load("2.png"), pygame.image.load("3.png"), \
                           pygame.image.load("dead.png")]
        self.status = 0
        self.birdX = 65
        self.birdY = 206
        self.jump = False
        self.jumpSpeed = 8
        self.gravity = 5
        self.dead = False

    def birdUpdate(self):
        if self.jump == True:
            self.jumpSpeed -= 0.5
            self.birdY -= self.jumpSpeed
        else:
            self.gravity += 0.2
            self.birdY += self.gravity
        self.birdRect[1] = self.birdY+10.5

class Pipeline(object):
    def __init__(self):
        self.wallx = 400
        self.pipeUp = pygame.image.load("top.png")
        self.pipeDown = pygame.image.load("bottom.png")

    def updatePipeline(self):
        self.wallx -=5
        if self.wallx < 85:
            global sum,score
            sum += 1
        if self.wallx < -52:
            self.wallx = 400
        score = sum // 22


def createMap():
    # 显示地图
    screen.fill(color)
    screen.blit(bg, (0, 0))
    # 显示管道
    screen.blit(pipeline.pipeUp, (pipeline.wallx, -150))
    screen.blit(pipeline.pipeDown, (pipeline.wallx, 300))
    pipeline.updatePipeline()
    # 显示小鸟
    if bird.dead:
        bird.status = 3
    elif bird.jump:
        bird.status = 0

    screen.blit(bird.birdStatus[bird.status], (bird.birdX, bird.birdY))
    bird.birdUpdate()
    # 显示分数
    text = font.render(str(score), True, (0, 0, 0))
    screen.blit(text, (134,50))
    pygame.display.update()
    

def checkDead():
    upRect = pygame.Rect(pipeline.wallx,-150,pipeline.pipeUp.get_width(),pipeline.pipeUp.get_height())
    downRect = pygame.Rect(pipeline.wallx,300,pipeline.pipeDown.get_width(),pipeline.pipeDown.get_height())

    if upRect.colliderect(bird.birdRect) or downRect.colliderect(bird.birdRect):
        bird.dead = True
        return True
    if not 0 < bird.birdRect[1] < height:
        bird.dead = True
        return True
    else:
        return False



if __name__ == "__main__":
    """主程序"""
    pygame.init()
    size = width, height = (288, 512)
    screen = pygame.display.set_mode(size)
    color = (255, 255, 255)
    bg = pygame.image.load("bg.png")
    time = pygame.time.Clock()
    bird = Bird()
    pipeline = Pipeline()

    score = 0
    sum = 0

    font = pygame.font.SysFont('隶书', 50)

    while True:
        time.tick(60)
        for event in  pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN) and not bird.dead:
                bird.jump = True
                bird.gravity = 5
                bird.jumpSpeed = 8

        if checkDead():
            createMap()
            break
        else:
            createMap()

