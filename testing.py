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
clock = pygame.time.Clock()
pygame.font.init()

class Samurai(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.sprites = []
        self.x = x_pos
        self.y = y_pos
        self.width = 400
        self.height = 300
        self.is_attacking = False
        self.attack_counter = 0
        self.sprites.append(pygame.image.load(r'C:\Users\gald1\Desktop\web development projects\PyGame\assets\Samurai1\04-Attack\Attack1\__Samurai1_Attack1_000.png'))
        self.sprites.append(pygame.image.load(r'C:\Users\gald1\Desktop\web development projects\PyGame\assets\Samurai1\04-Attack\Attack1\__Samurai1_Attack1_001.png'))
        self.sprites.append(pygame.image.load(r'C:\Users\gald1\Desktop\web development projects\PyGame\assets\Samurai1\04-Attack\Attack1\__Samurai1_Attack1_003.png'))
        self.sprites.append(pygame.image.load(r'C:\Users\gald1\Desktop\web development projects\PyGame\assets\Samurai1\04-Attack\Attack1\__Samurai1_Attack1_004.png'))
        self.sprites.append(pygame.image.load(r'C:\Users\gald1\Desktop\web development projects\PyGame\assets\Samurai1\04-Attack\Attack1\__Samurai1_Attack1_005.png'))
        self.sprites.append(pygame.image.load(r'C:\Users\gald1\Desktop\web development projects\PyGame\assets\Samurai1\04-Attack\Attack1\__Samurai1_Attack1_006.png'))
        self.sprites.append(pygame.image.load(r'C:\Users\gald1\Desktop\web development projects\PyGame\assets\Samurai1\04-Attack\Attack1\__Samurai1_Attack1_007.png'))

        self.image = self.sprites[self.attack_counter]
        self.anim_rect = self.image.get_rect(width=250, height=150)
        self.rect = pygame.Rect((x_pos, y_pos), (self.width, self.height))
    def draw(self):
        if self.is_attacking:
            self.attack_counter += 0.4
            if self.attack_counter >= len(self.sprites):
                self.is_attacking = False
                self.attack_counter = 0
            self.image = self.sprites[int(self.attack_counter)]
            WIN.blit(self.image, self.anim_rect)
        else:
            WIN.blit(SAMURAI_IMAGE_SCALED, self.rect)
    
    def attack(self):
        self.is_attacking = True
        print(self.is_attacking)
        self.attack_counter = 0


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
        if self.rect.x > 725:
            self.kill()




def samurai_movement(keys, samurai):
    if keys[pygame.K_LEFT] and samurai.x > -50:
        samurai.x -= VEL
    elif keys[pygame.K_RIGHT] and samurai.x < 725:
        samurai.x += VEL

    elif keys[pygame.K_DOWN] and samurai.y < 368:
        samurai.y += VEL
    elif keys[pygame.K_UP] and samurai.y > -24:
        samurai.y -= VEL



class Slash:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 8  # Speed at which the slash moves
        self.image = pygame.image.load(os.path.join('assets', 'Alternative_2_08.png'))

    def move(self):
        self.x -= self.speed

    def draw(self, surface):
        self.rect = self.image.get_rect(width=124, height=150)
        self.rect.size = (124, 150)
        self.rect.topleft = [self.x, self.y]
        self.hitbox = self.rect.inflate(-100, -100)
        surface.blit(self.image , self.rect)


def draw_window(samurai, slashes, sprites, enemy, text, textRect):
    WIN.fill(bg_color)
    samurai.draw()
    WIN.blit(text, textRect)
    if slashes:
        for slash in slashes:
            slash.draw(WIN)
            slash.move()
            if slash.x < -50:
                slashes.remove(slash)
    if sprites and enemy:
        sprites.draw(WIN)
        sprites.update()
            

    


    pygame.display.update()

def main():
    run = True
    samurai = Samurai(600, 160)
    samurai_char = samurai.rect
    slash = None
    slashes = []
    enemy = None
    moving_sprites = None
    game_started = False
    start_time = pygame.time.get_ticks()
    moving_sprites = pygame.sprite.Group()
    lives = 3
    start_cd = 0
    pygame_font = pygame.font.Font(r'C:\Users\gald1\Desktop\web development projects\PyGame\assets\Minecraft.ttf', 16)
    while run:
        text = pygame_font.render(f'Lives: {lives}', True, (255, 0, 0))
        textRect = text.get_rect()
        textRect.center = (33, 13)
        current_time = pygame.time.get_ticks()
        random_appearence_time_enemy = random.randint(2000, 7000)
        if current_time - start_time > random_appearence_time_enemy:
            print(start_time)
            start_time = pygame.time.get_ticks()
            random_y = random.randint(0, 350)
            enemy = Enemy(-300, random_y)
            moving_sprites.add(enemy)
            print(moving_sprites)
            if enemy.rect.x > 300:
                moving_sprites.remove(enemy)
                print(enemy)
        if len(slashes) > 0: 
            for sprite in moving_sprites:
                for slash in slashes:
                    if sprite.rect.colliderect(slash):
                        slashes.remove(slash)
                        moving_sprites.remove(sprite)

        clock.tick(FPS)
    

        for event in pygame.event.get():
             if event.type == pygame.QUIT:
                 run = False
             if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print(f"start_Cd : {start_cd}")
                    if current_time - start_cd >= 2000 or start_cd == 0:
                        start_cd = pygame.time.get_ticks()

                        slash = Slash(x=samurai.rect.x - 30, y=samurai.rect.y)
                        print(type(slash))
                        samurai.attack()
                        slashes.append(slash)


                

        draw_window(samurai, slashes, sprites=moving_sprites, enemy=enemy, text=text, textRect=textRect)
        keys_pressed = pygame.key.get_pressed()
        samurai_movement(keys=keys_pressed, samurai=samurai_char)
       

if __name__ == '__main__':

    main()