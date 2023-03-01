# _main.py
import pygame
import sys
import traceback
import myplane
import bullet
import enemy
from pygame.locals import *

pygame.init()
pygame.mixer.init()

bgSize = width, height = 480, 700
screen = pygame.display.set_mode(bgSize)
pygame.display.set_caption("飞机大战 -- ZBh Demo")

background = pygame.image.load("images/background.png").convert()

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)


#载入游戏音乐
pygame.mixer.music.load("sound/game_music.ogg")
pygame.mixer.music.set_volume(0.2)
bulletSound = pygame.mixer.Sound("sound/bullet.wav")
bulletSound.set_volume(0.2)
bombSound = pygame.mixer.Sound("sound/use_bomb.wav")
bombSound.set_volume(0.2)
supplySound = pygame.mixer.Sound("sound/supply.wav")
supplySound.set_volume(0.2)
getBombSound = pygame.mixer.Sound("sound/get_bomb.wav")
getBombSound.set_volume(0.2)
getBulletSound = pygame.mixer.Sound("sound/get_bullet.wav")
getBulletSound.set_volume(0.2)
upgradeSound = pygame.mixer.Sound("sound/upgrade.wav")
upgradeSound.set_volume(0.2)
enemy3FlySound = pygame.mixer.Sound("sound/enemy3_flying.wav")
enemy3FlySound.set_volume(0.2)
enemy1DownSound = pygame.mixer.Sound("sound/enemy1_down.wav")
enemy1DownSound.set_volume(0.2)
enemy2DownSound = pygame.mixer.Sound("sound/enemy2_down.wav")
enemy2DownSound.set_volume(0.2)
enemy3DownSound = pygame.mixer.Sound("sound/enemy3_down.wav")
enemy3DownSound.set_volume(0.2)
meDownSound = pygame.mixer.Sound("sound/me_down.wav")
meDownSound.set_volume(0.2)


def addSmallEnemies(group1, group2, num):
    for i in range(num):
        e1 = enemy.SmallEnemy(bgSize)
        group1.add(e1)
        group2.add(e1)

def addMidEnemies(group1, group2, num):
    for i in range(num):
        e1 = enemy.MidEnemy(bgSize)
        group1.add(e1)
        group2.add(e1)

def addBigEnemies(group1, group2, num):
    for i in range(num):
        e1 = enemy.BigEnemy(bgSize)
        group1.add(e1)
        group2.add(e1)

def incSpeed(target, inc):
    for each in target:
        each.speed += inc




def main():
    pygame.mixer.music.play(-1)
    clock = pygame.time.Clock()
    running = True
    
    # 生成我方飞机
    me = myplane.MyPlane(bgSize)

    # 生成敌方飞机
    enemies = pygame.sprite.Group()
    # 小型    
    smallEnemies = pygame.sprite.Group()
    addSmallEnemies(smallEnemies, enemies, 15)
    # 中型    
    midEnemies = pygame.sprite.Group()
    addMidEnemies(midEnemies, enemies, 4)
    # 大型    
    bigEnemies = pygame.sprite.Group()
    addBigEnemies(bigEnemies, enemies, 2)

    #生成普通子弹
    bullet1 = []
    bullet1Index = 0
    BULLET1NUM = 5    # 实现80%射程
    for i in range(BULLET1NUM):
        bullet1.append(bullet.Bullet1(me.rect.midtop))

    # 中弹图片索引
    e1DestroyIndex = 0
    e2DestroyIndex = 0
    e3DestroyIndex = 0
    meDestroyIndex = 0

    # 统计分数
    score = 0
    scoreFont = pygame.font.Font("font/font.ttf", 36)

    # 标志是否暂停游戏
    paused = False
    pauseNorImage = pygame.image.load("images/pause_nor.png").convert_alpha()
    pausePressedImage = pygame.image.load("images/pause_pressed.png").convert_alpha()
    resumeNorImage = pygame.image.load("images/resume_nor.png").convert_alpha()
    resumePressedImage = pygame.image.load("images/resume_pressed.png").convert_alpha()
    pausedRect = pauseNorImage.get_rect()
    pausedRect.left, pausedRect.top = width - pausedRect.width - 10, 10
    pausedImage = pauseNorImage

    # 设置难度级别
    level = 1

    # 全屏炸弹
    bombImage = pygame.image.load("images/bomb.png").convert_alpha()
    bombRect = bombImage.get_rect()
    bombFont = pygame.font.Font("font/font.ttf", 48)
    bombNum = 3

    # 用于切换图片
    switchImage = True
    # 用于延时
    delay = 100
    


# ==================================



    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and pausedRect.collidepoint(event.pos):
                    paused = not paused

            elif event.type == MOUSEMOTION:
                if pausedRect.collidepoint(event.pos):
                    if paused:
                        pausedImage = resumePressedImage
                    else:
                        pausedImage = pausePressedImage
                else:
                    if paused:
                        ppausedImage = resumeNorImage
                    else:
                        pausedImage = pauseNorImage

            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if bombNum:
                        bombNum -= 1
                        bombSound.play()
                        for each in enemies:
                            if each.rect.bottom > 0:
                                each.active = False
                            

        # 根据用户的得分增加难度
        if level == 1 and score > 50000:
            level = 2
            upgradeSound.play()
            # 增加3架小型敌机、2架中型敌机和1架大型敌机
            addSmallEnemies(smallEnemies, enemies, 3)
            addMidEnemies(MidEnemies, enemies, 2)
            addBigEnemies(BigEnemies, enemies, 1)
            # 提升小型敌机的速度
            incSpeed(smallEnemies, 1)

        elif level == 1 and score > 300000:
            level = 3
            upgradeSound.play()
            # 增加5架小型敌机、3架中型敌机和2架大型敌机
            addSmallEnemies(smallEnemies, enemies, 5)
            addMidEnemies(MidEnemies, enemies, 3)
            addBigEnemies(BigEnemies, enemies, 2)
            # 提升小型敌机和中型敌机的速度
            incSpeed(smallEnemies, 1)
            incSpeed(MidEnemies, 1)

        elif level == 1 and score > 600000:
            level = 4
            upgradeSound.play()
            # 增加5架小型敌机、3架中型敌机和2架大型敌机
            addSmallEnemies(smallEnemies, enemies, 5)
            addMidEnemies(MidEnemies, enemies, 3)
            addBigEnemies(BigEnemies, enemies, 2)
            # 提升小型敌机和中型敌机的速度
            incSpeed(smallEnemies, 1)
            incSpeed(MidEnemies, 1)

        elif level == 1 and score > 600000:
            level = 5
            upgradeSound.play()
            # 增加5架小型敌机、3架中型敌机和2架大型敌机
            addSmallEnemies(smallEnemies, enemies, 5)
            addMidEnemies(MidEnemies, enemies, 3)
            addBigEnemies(BigEnemies, enemies, 2)
            # 提升小型敌机和中型敌机的速度
            incSpeed(smallEnemies, 1)
            incSpeed(MidEnemies, 1)
            
        screen.blit(background, (0, 0))

        if not paused:
            # 检测用户的键盘操作
            keyPressed = pygame.key.get_pressed()

            if keyPressed[K_w] or keyPressed[K_UP]:
                me.moveUp()
            if keyPressed[K_s] or keyPressed[K_DOWN]:
                me.moveDown()
            if keyPressed[K_a] or keyPressed[K_LEFT]:
                me.moveLeft()
            if keyPressed[K_d] or keyPressed[K_RIGHT]:
                me.moveRight()
            

            # 发射子弹
            if not(delay % 12):
                bullet1[bullet1Index].reset(me.rect.midtop)
                bullet1Index = (bullet1Index + 1) % BULLET1NUM

            # 检测子弹是否击中敌机
            for b in bullet1:
                if b.active:
                    b.move()
                    screen.blit(b.image, b.rect)
                    enemyHit = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)
                    if enemyHit:
                        b.active = False
                        for e in enemyHit:
                            if e in midEnemies or e in bigEnemies:
                                e.hit = True
                                e.energy -= 1
                                if e.energy == 0:
                                    e.active = False
                            else:
                                e.active = False

            # 绘制敌机
            # 大
            for each in bigEnemies:
                if each.active:
                    each.move()
                    if each.hit:
                        # 绘制被击打特效
                        screen.blit(each.imageHit, each.rect)
                        each.hit = False
                    if switchImage:
                        screen.blit(each.image1, each.rect)
                    else:
                        screen.blit(each.image2, each.rect)

                    # 绘制血槽
                    pygame.draw.line(screen, BLACK, \
                                     (each.rect.left, each.rect.top - 5), \
                                     (each.rect.right, each.rect.top - 5), \
                                     2)
                    # 当生命值大于20%显示红色，否则显示红色
                    energyRemain = each.energy / enemy.BigEnemy.energy
                    if energyRemain > 0.2:
                        energyColor = GREEN
                    else:
                        energyColor = RED
                    pygame.draw.line(screen, energyColor, \
                                     (each.rect.left, each.rect.top - 5), \
                                     (each.rect.left + each.rect.width * energyRemain, \
                                      each.rect.top - 5), 2)
                    
                    # 即将出现在画面中,并播放音效
                    if each.rect.bottom == -50:
                        enemy3FlySound.play(-1)
                else:
                    # 毁灭
                    if not(delay % 3):
                        if e3DestroyIndex == 0:
                            enemy3DownSound.play()
                        screen.blit(each.destroyImages[e3DestroyIndex], each.rect)
                        e3DestroyIndex = (e3DestroyIndex + 1) % 6
                        if e3DestroyIndex == 0:
                            enemy3DownSound.stop()
                            score += 10000
                            each.reset()


            # 中
            for each in midEnemies:
                if each.active:
                    each.move()
                    if each.hit:
                        # 绘制被击打特效
                        screen.blit(each.imageHit, each.rect)
                        each.hit = False
                    else:
                        screen.blit(each.image, each.rect)

                    # 绘制血槽
                    pygame.draw.line(screen, BLACK, \
                                     (each.rect.left, each.rect.top - 5), \
                                     (each.rect.right, each.rect.top - 5), \
                                     2)
                    # 当生命值大于20%显示红色，否则显示红色
                    energyRemain = each.energy / enemy.MidEnemy.energy
                    if energyRemain > 0.2:
                        energyColor = GREEN
                    else:
                        energyColor = RED
                    pygame.draw.line(screen, energyColor, \
                                     (each.rect.left, each.rect.top - 5), \
                                     (each.rect.left + each.rect.width * energyRemain, \
                                      each.rect.top - 5), 2)
                else:
                    # 毁灭
                    if not(delay % 3):
                        if e2DestroyIndex == 0:
                            enemy2DownSound.play()
                        screen.blit(each.destroyImages[e2DestroyIndex], each.rect)
                        e2DestroyIndex = (e2DestroyIndex + 1) % 4
                        if e2DestroyIndex == 0:
                            score +=6000
                            each.reset()
            

            # 小
            for each in smallEnemies:
                if each.active:                  
                    each.move()
                    screen.blit(each.image, each.rect) 
                else:
                    # 毁灭
                    if not(delay % 3):
                        if e1DestroyIndex == 0:
                            enemy1DownSound.play()
                        screen.blit(each.destroyImages[e1DestroyIndex], each.rect)
                        e1DestroyIndex = (e1DestroyIndex + 1) % 4
                        if e1DestroyIndex == 0:
                            score += 1000
                            each.reset()

            # 检测我方飞机是否被撞
            enemiesDown = pygame.sprite.spritecollide(me, enemies, False, \
                                                      pygame.sprite.collide_mask)
            if enemiesDown:
                me.active = True
                for e in enemiesDown:
                    e.active = False
                
            # 绘制我方飞机
            if me.active:
                if switchImage:
                    screen.blit(me.image1, me.rect)
                else:
                    screen.blit(me.image2, me.rect)
            else:
                # 毁灭
                if not(delay % 3):
                    if meDestroyIndex == 0:
                            meDownSound.play()
                    screen.blit(me.destroyImages[meDestroyIndex], me.rect)
                    meDestroyIndex = (meDestroyIndex + 1) % 3
                    if meDestroyIndex == 0:
                        me.reset()

            # 绘制全屏炸弹数量
            bombText = bombFont.render("x %d" % bombNum, True, WHITE)
            textRect = bombText.get_rect()
            screen.blit(bombImage, (10, height - 10 - bombRect.height))
            screen.blit(bombText, (20 + bombRect.width, height -5 - textRect.height))
                
        # 绘制得分
        scoreText = scoreFont.render("Score : %s" % str(score), True, WHITE)
        screen.blit(scoreText, (10, 5))

        # 绘制暂停按钮
        screen.blit(pausedImage, pausedRect)
        
        # 延迟切换图片
        delay -= 1
        if not (delay % 5):    # 相当于帧数 / 5
            switchImage = not switchImage
        delay -= 1
        if not delay:
            delay = 100

    
        pygame.display.flip()

        clock.tick(60)
        



if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
