from typing import Any
from pygame import *
from random import randint
from time import time as timer

mixer.init()
mixer.music.load('space.ogg')
fire_sound = mixer.Sound('fire.ogg')

img_back = 'galaxy.jpg'
img_hero = 'rocket.png'
img_ufo = "ufo.png"
img_fire = "bullet.png"

window = display.set_mode((700,500))

font.init()
font2 = font.Font(None, 80)
font1 = font.Font(None, 36)
win = font2.render('YOU WIN!!!!!!!', True, (255, 255, 255))
luse = font2.render('YOU luse!!!!!!', True, (100, 0, 0))

score = 0
lost = 0




class GameSprite(sprite.Sprite):
    def __init__ (self, player_img, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_img), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def move(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 610:
            self.rect.x += self.speed  
    def fire(self):
        bullet = Bullet(img_fire, self.rect.centerx, self.rect.top, 15,20, -15 )
        bullets.add(bullet)

bullets = sprite.Group()

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()




class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.x = randint(80,620)
            self.rect.y = 0
            lost = lost + 1

            
background = transform.scale(image.load(img_back), (700, 500))

ship = Player(img_hero,5,400,80,100,10)
ufos = sprite.Group()
for i in range(1,6):
    ufo = Enemy(img_ufo, randint(80,620), -30, 80,50, randint(1,5))
    ufos.add(ufo)



run = True
finish = False

num_fire = 0 
rel_time = False



while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire <5 and rel_time == False:
                    num_fire = num_fire+1
                    ship.fire()

                if num_fire >=5 and rel_time == False:
                    last_time = timer()
                    rel_time = True



    
    if not finish: 
        window.blit(background,(0,0))
        text = font1.render("Рахунок:" + str(score), 1, (255,255,255))
        window.blit(text,(10,20))
        text_lost = font1.render("Пропущено:" + str(lost), 1, (255,255,255))
        window.blit(text_lost, (10,50))



        ship.draw()
        ship.move()
        ufos.update()
        ufos.draw(window)
        bullets.update()
        bullets.draw(window)
        
        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 1:
                load = font1.render('restart', 1, (150, 0, 0))
                window.blit(load, (250,450))
            else:
                num_fire = 0 
                rel_time = False



        collides = sprite.groupcollide(ufos, bullets, True, True)

        for c in collides:
            score = score+1
            ufo = Enemy(img_ufo, randint(80,620), -30, 80,50, randint(1,5))
            ufos.add(ufo)
        
        if sprite.spritecollide(ship , ufos, False) or lost >= 1:
            finish = True
            window.blit(luse,(200, 200))

        if score >= 15:
            finish = True
            window.blit(win,(200, 200))


        display.update()
    time.delay(40)

