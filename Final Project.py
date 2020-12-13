import pygame
pygame.init()
wnd_width = 612
wnd_height = 470
wnd = pygame.display.set_mode((wnd_width, wnd_height))

pygame.display.set_caption('Project Defender')

bg = pygame.image.load('Background.png')
spaceship = pygame.image.load('Spaceship.png')
alienPic = pygame.image.load('Alien.png')
alienDeath = pygame.image.load('Alien pop.png')
hostage_pic = pygame.image.load('Hostage.png')

font1 = pygame.font.SysFont('arial', 20, True)
font2 = pygame.font.SysFont('comicsans', 20, True)
font3 = pygame.font.SysFont('comicsans', 65, True)
res_font = pygame.font.SysFont('comicsans', 100, True)

bulletSound = pygame.mixer.Sound('bullet sound.wav')
bg_music = pygame.mixer.music.load('back music.mp3')
pygame.mixer.music.play(-1)


class player():
    def __init__(self, pl_x, pl_y, pl_width, pl_height, lsr_height, lsr_width, vel):
        self.pl_x = pl_x
        self.pl_y = pl_y
        self.pl_width = pl_width
        self.pl_height = pl_height
        self.pl_vel = vel
        self.lsr_height = lsr_height
        self.lsr_y = pl_y + 1
        self.lsr_width = lsr_width

    def draw(self, wnd):
        a = (self.pl_x+21, self.lsr_y, self.lsr_width, self.lsr_height)
        pygame.draw.rect(wnd, (255, 0, 0), a)
        wnd.blit(spaceship, (self.pl_x, self.pl_y))

ship = player(280, 387, 51, 64, 15, 5, 10)


class enemy():
    def __init__(self, x, y, width, height, facing, vel):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.facing = facing
        self.vel = vel

    def drawEn(self, wnd):
        wnd.blit(alienPic, (self.x, self.y))

alien = enemy(274, 50, 64, 64, 1, 2)


class hostage():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.facing = 1
        self.vel = 2

    def draw(self, wnd):
        wnd.blit(hostage_pic, (self.x, self.y))

hostage = hostage(0, 144, 64, 64)


def frameFormat1():
    wnd.blit(bg, (0, 0))
    ship.draw(wnd)
    alien.drawEn(wnd)
    hostage.draw(wnd)
    text1 = font1.render('Score: ' + str(hit), 1, (158, 172, 175))
    text2 = font1.render('Lives: ' + str(lives), 1, (158, 172, 175))
    wnd.blit(text1, (520, 10))
    wnd.blit(text2, (10, 10))
    pygame.display.update()




def gameScreen():
    global hit, lives
    lives = 5
    hit = 0
    fire = False
    run1 = True
    while run1:
        pygame.time.delay(50)
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        if hostage.x + hostage.width >= wnd_width:
            hostage.facing = -1
        elif hostage.x <= 0:
            hostage.facing = 1
        hostage.x = hostage.x + hostage.vel * hostage.facing
        
        if alien.x + alien.width >= wnd_width:
            alien.facing = -1
        elif alien.x <= 0:
            alien.facing = 1
        alien.x = alien.x + alien.vel * alien.facing
        
        if keys[pygame.K_LEFT]:
            if 0 < ship.pl_x:
                ship.pl_x -= ship.pl_vel
        if keys[pygame.K_RIGHT]:
            if ship.pl_x + 58 < wnd_width:
                ship.pl_x += ship.pl_vel

        if fire is False:
            if keys[pygame.K_SPACE]:
                fire = True
                bulletSound.play()
        if fire is True:
            if ship.lsr_y > 0:
                ship.lsr_y = ship.lsr_y - 10
                if alien.x < ship.pl_x + 21 < alien.x + 64:
                    if alien.y < ship.lsr_y < alien.y + 40:
                        fire = False
                        ship.lsr_y = ship.pl_y
                        hit += 1
                        if hit % 5 == 0:
                            alien.vel += 3
                        if hit % 10 == 0:
                            ship.pl_vel += 1
                if hostage.x + 7 < ship.pl_x + 21 < hostage.x + 57:
                    if hostage.y < ship.lsr_y < hostage.y + 55:
                        hit -= 5
                        lives -= 1
                        ship.lsr_y = ship.pl_y
                        fire = False
                        if lives <= 0:
                            player.pl_x = 280
                            res_text = res_font.render('Game Over!', 1, (255, 255, 255))
                            wnd.blit(res_text, (306-res_text.get_width()//2, 185))
                            pygame.display.update()
                            i = 0
                            ship.pl_vel = 10
                            alien.vel = 2
                            while i < 300:
                                pygame.time.delay(10)
                                i += 1
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        i = 301
                                        pygame.quit()
                                if keys[pygame.K_SPACE]:
                                    fire = False
                                    i = 301
                            lives = 5
                            hit = 0
                            
                            
            elif ship.lsr_y <= 0:
                fire = False
                lives -= 1
                ship.lsr_y = ship.pl_y
                if lives <= 0:
                    player.pl_x = 280
                    res_text = res_font.render('Game Over!', 1, (255, 255, 255))
                    wnd.blit(res_text, (306-res_text.get_width()//2, 185))
                    pygame.display.update()
                    i = 0
                    alien.vel = 2
                    ship.pl_vel = 10
                    while i < 300:
                        pygame.time.delay(10)
                        i += 1
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                i = 301
                                pygame.quit()
                        if keys[pygame.K_SPACE]:
                            fire = False
                            i = 301
                    lives = 5
                    hit = 0
                    

        frameFormat1()




def frameFormat2():
    wnd.fill((0, 0, 0))
    startText = font3.render('Start (up arrow)', 1, (255, 255, 255))
    difText = font3.render('Difficulty (down arrow)', 1, (255, 255, 255))
    wnd.blit(startText, (306-startText.get_width()//2, 135))
    wnd.blit(difText, (306-difText.get_width()//2, 235))
    pygame.display.update()


def startScreen():
    run2 = True
    while run2:
        pygame.time.delay(50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            run2 = False
            gameScreen()

        if keys[pygame.K_DOWN]:
            run2 = False
            difficultyScreen()
        frameFormat2()

def frameFormat3():
    wnd.fill((0, 0, 0))
    chngtext1 = font3.render('Easy(1)',1 , (255, 255, 255))
    wnd.blit(chngtext1, (306-chngtext1.get_width()//2, 130))
    chngtext2 = font3.render('Normal(2)',1 , (255, 255, 255))
    wnd.blit(chngtext2, (306-chngtext2.get_width()//2, 200))
    chngtext3 = font3.render('Difficult(3)',1 , (255, 255, 255))
    wnd.blit(chngtext3, (306-chngtext3.get_width()//2, 270))
    pygame.display.update()

    
def difficultyScreen():
    run3 = True
    while run3:
        pygame.time.delay(50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        keys = pygame.key.get_pressed()
        

        if keys[pygame.K_1]:
            ship.pl_vel = 18
            alien.vel = 1
            run3 = False
            gameScreen()
        if keys[pygame.K_2]:
            ship.pl_vel = 10
            alien.vel = 2
            run3 = False
            gameScreen()
        if keys[pygame.K_3]:
            ship.pl_vel = 7
            alien.vel = 4
            run3 = False
            gameScreen()

        frameFormat3()


startScreen()
