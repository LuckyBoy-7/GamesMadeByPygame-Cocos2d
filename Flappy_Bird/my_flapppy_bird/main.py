import pygame
import sys
from bird import *
from pipelines import *


pygame.init()

size = (900, 512)
screen = pygame.display.set_mode(size)
color = (0, 0, 0)

pygame.mixer.music.load("sounds/bg.mp3")
pygame.mixer.music.set_volume(0.1)

dead_sound = pygame.mixer.Sound("sounds/dead.mp3")
dead_sound.set_volume(0.1)
fly_sound = pygame.mixer.Sound("sounds/fly.wav")
fly_sound.set_volume(0.1)

gap = 150

clock = pygame.time.Clock()

# 设置管道更新速度
delay = 100

# 记录得分
score = 0
font = pygame.font.SysFont("Arial", 30)


def check_dead():
    # 检测碰撞
    if pygame.sprite.spritecollide(bird, pipelines, False) or \
       bird.rect.bottom >= size[1] or bird.rect.top <= 0:
        bird.dead = True

    
def get_result():
        global restart_rect
        font = pygame.font.SysFont("Arial", 100)
        text = font.render("Your final score is " + str(int(score)), True, ("yellow"))

        arrow = pygame.image.load("images/arrow.png")
        arrow_rect = arrow.get_rect()

        restart = pygame.image.load("images/restart.png")
        restart_rect = restart.get_rect()
        restart_rect.x, restart_rect.y = (size[0] - restart_rect.w) // 2, 250
        

        screen.blit(text, ((size[0] - text.get_width()) // 2, 50))
        screen.blit(arrow, ((size[0] - arrow_rect.w) // 2, 150))
        screen.blit(restart, restart_rect)




def restart():
        global score
        
        dead_sound.play()
        pygame.mixer.music.stop()

        
        screen.blit(bird.status[1], bird.rect)
        pipelines.draw(screen)
        get_result()
        pygame.display.update()
        
        while True:
            clock.tick(100)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
            button = pygame.mouse.get_pressed()
            pos = pygame.mouse.get_pos()

            if restart_rect.collidepoint(pos) and button[0]:
                bird.reset()
                score = 0
                main()
                


"""主程序"""         
def main():
    global score, delay, bird, pipelines

    pygame.mixer.music.play(-1)

    bird = Bird(size)
    
    pipelines = pygame.sprite.Group()
    
    while True:
        clock.tick(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                fly_sound.play()
                bird.jump = True
                bird.jumpspeed = 5


        
        # 记录得分
        for i in pipelines:
            if  i.rect.centerx - 1 <= bird.rect.centerx < i.rect.centerx+5:
                score += 1 / 2 # 两根管子嘛
                

        """更新部分"""
        check_dead()
        
        # 刷屏幕
        screen.fill(color)
        
        if bird.dead:
            restart()
                
            
        else:
            # 更新分数
            text = font.render(str(int(score)), True, (255, 0, 0))
            screen.blit(text, ((size[0] - text.get_width()) / 2, 50))
            # 更新管道
            delay -= 1
            if delay < 2:
                delay = 100
            if delay % 100 == 0:
                y = randint(100, 400)
                pipelines.add(UpPipeline(size, y))
                pipelines.add(DownPipeline(size, y + gap))

            for i in pipelines:
                if i.rect.right < 0:
                    pipelines.remove(i)

            pipelines.draw(screen)
            pipelines.update()

            # 更新小鸟
            screen.blit(bird.status[0], bird.rect)
            bird.update()

            # 总更新
            pygame.display.update()


       
if __name__ == "__main__":
    main()
    
