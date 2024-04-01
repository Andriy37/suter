from pygame import *
mixer.init()
mixer.music.load('space.ogg')
fire_sound = mixer.Sound('fire.ogg')

img_back = 'galaxy.jpg'
img_hero = 'rocket.png'

window = display.set_mode((700,500))

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


background = transform.scale(image.load(img_back), (700, 500))

ship = Player(img_hero,5,400,80,100,10)

run = True
finish = False

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
    if not finish: 
        window.blit(background,(0,0))
        ship.draw()
        ship.move()

    display.update()
    time.delay(60)

