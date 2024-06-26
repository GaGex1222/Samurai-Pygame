import pygame
import os
import random
import time

import pygame.locals
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
pygame.display.set_caption("Samurai Game")
bg_color = (100, 220, 186)
SAMURAI_IMAGE = pygame.image.load(os.path.join('assets', 'Samurai1', '01-Idle', '__Samurai1_Idle_000.png'))
SAMURAI_IMAGE_SCALED = pygame.transform.scale(SAMURAI_IMAGE , (250, 150))
SAMURAI_SLASH = pygame.image.load(os.path.join('assets', 'Alternative_2_08.png'))
VEL = 5

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.sprites = []
        width, height = 250, 150
        self.sprites.append(pygame.transform.scale(pygame.transform.flip(pygame.image.load(r'assets/Samurai1/02-Run/__Samurai1_Run_000.png'), True, False), (width, height)))
        self.sprites.append(pygame.transform.scale(pygame.transform.flip(pygame.image.load(r'assets/Samurai1/02-Run/__Samurai1_Run_001.png'), True, False), (width, height)))
        self.sprites.append(pygame.transform.scale(pygame.transform.flip(pygame.image.load(r'assets/Samurai1/02-Run/__Samurai1_Run_002.png'), True, False), (width, height)))
        self.sprites.append(pygame.transform.scale(pygame.transform.flip(pygame.image.load(r'assets/Samurai1/02-Run/__Samurai1_Run_003.png'), True, False), (width, height)))
        self.sprites.append(pygame.transform.scale(pygame.transform.flip(pygame.image.load(r'assets/Samurai1/02-Run/__Samurai1_Run_004.png'), True, False), (width, height)))
        self.sprites.append(pygame.transform.scale(pygame.transform.flip(pygame.image.load(r'assets/Samurai1/02-Run/__Samurai1_Run_005.png'), True, False), (width, height)))
        self.sprites.append(pygame.transform.scale(pygame.transform.flip(pygame.image.load(r'assets/Samurai1/02-Run/__Samurai1_Run_006.png'), True, False), (width, height)))
        self.sprites.append(pygame.transform.scale(pygame.transform.flip(pygame.image.load(r'assets/Samurai1/02-Run/__Samurai1_Run_007.png'), True, False), (width, height)))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect(width=250, height=150)
        self.rect.size = (250, 150)
        self.rect.topleft = [pos_x, pos_y]

    def update(self):
        self.current_sprite += 0.6
        

        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]
        self.rect.size = (250, 150)
        self.rect.x += 3



class Slash:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 3  # Speed at which the slash moves

    def move(self):
        distance_to_move = -124 - self.x
        self.x += distance_to_move  # Update x by the difference

    def draw(self, surface):
        surface.blit(SAMURAI_SLASH, (self.x, self.y))

def samurai_movement(keys, samurai):
    if keys[pygame.K_LEFT] and samurai.x > -50:
        samurai.x -= VEL
    elif keys[pygame.K_RIGHT] and samurai.x < 725:
        samurai.x += VEL

    elif keys[pygame.K_DOWN] and samurai.y < 368:
        samurai.y += VEL
    elif keys[pygame.K_UP] and samurai.y > -24:
        samurai.y -= VEL

draw_slash = False

moving_sprites = pygame.sprite.Group()
#random y pos for enemy
random_y = random.randint(0, 350)
enemy = Enemy(-300, random_y)
moving_sprites.add(enemy)
print(moving_sprites)

def draw_window(samurai, slash, draw_slash):
    WIN.fill(bg_color)
    WIN.blit(SAMURAI_IMAGE_SCALED, samurai)
    if draw_slash:
        slash.draw(WIN)
        slash.move()
        if slash.x > -50:
            draw_slash = False

    pygame.display.update()

def main():
    samurai = pygame.Rect(100, 0, 400, 300)
    slash_rect = pygame.Rect((samurai.x - 30, samurai.y), (124, 150))

    clock = pygame.time.Clock()
    run = True
    while run:
        mouse_pos = pygame.mouse.get_pos()
        slash = Slash(x=samurai.x - 30, y=samurai.y)
        #print(mouse_pos)


        clock.tick(FPS)
    

        for event in pygame.event.get():
             if event.type == pygame.QUIT:
                 run = False

             if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    global draw_slash
                    draw_slash = True
                    slash = Slash(x=samurai.x - 30, y=samurai.y)
                    



    

    
    
    

        draw_window(samurai, slash=slash, draw_slash=draw_slash )
        keys_pressed = pygame.key.get_pressed()
        samurai_movement(keys=keys_pressed, samurai=samurai)
        
    
    pygame.quit()


if __name__ == '__main__':

    main()