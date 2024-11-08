import pygame
import os
import random
import time

import pygame.locals
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
BG_IMAGE = pygame.image.load(r'assets\bg\bg.png')
BATTLEGROUND_IMAGE = pygame.image.load(r'assets\battleground\columns&floor.png')
pygame.display.set_caption("Samurai Game")
bg_color = (100, 220, 186)
SAMURAI_IMAGE = pygame.image.load(os.path.join('assets', 'Samurai1', '01-Idle', '__Samurai1_Idle_000.png'))
SAMURAI_IMAGE_SCALED = pygame.transform.scale(SAMURAI_IMAGE , (250, 150))
SAMURAI_SLASH = pygame.image.load(os.path.join('assets', 'ultimateslash.png'))
VEL = 5
clock = pygame.time.Clock()
pygame.font.init()
pygame_font_for_game_over = pygame.font.Font(r'C:\Users\gald1\Desktop\stufff\Coding projects\MyPyGame\Samurai-Pygame\assets\Minecraft.ttf', 40)
pygame_font_for_ult = pygame.font.Font(r'C:\Users\gald1\Desktop\stufff\Coding projects\MyPyGame\Samurai-Pygame\assets\Minecraft.ttf', 20)

def draw_game_over(text, font_size, text_col, x, y):
    font = pygame.font.Font(r'C:\Users\gald1\Desktop\stufff\Coding projects\MyPyGame\Samurai-Pygame\assets\Minecraft.ttf', font_size)
    img = font.render(text, True, text_col)
    WIN.blit(img, (x, y))

class UltimateBar():
    def __init__(self, x, y, w, h, max_ult, text_x, text_y):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text_x = text_x
        self.text_y = text_y
        self.ult = 0
        self.max_ult = max_ult

    def draw(self, surface):
        ratio = self.ult / self.max_ult
        pygame.draw.rect(surface, 'white', (self.x, self.y, self.w, self.h))
        pygame.draw.rect(surface, 'blue', (self.x, self.y, self.w * ratio, self.h))
        if self.ult >= self.max_ult:
                img = pygame_font_for_ult.render("PRESS Q FOR ULTIMATE", True, (0, 0, 255))
                WIN.blit(img, (self.text_x, self.text_y))




class Samurai(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.sprites = []
        self.scaled_sprites = []
        self.scaled_running_sprites = []
        self.x = x_pos
        self.y = y_pos
        self.width = 250
        self.height = 150
        self.is_attacking = False
        self.is_running = False
        self.attack_counter = 0
        self.running_counter = 0
        #Attacking Sprites
        for i in range(8):
            self.sprites.append(pygame.image.load(rf'C:\Users\gald1\Desktop\stufff\Coding projects\MyPyGame\Samurai-Pygame\assets\Samurai1\04-Attack\Attack1\__Samurai1_Attack1_00{i}.png'))
        #Running sprites
        for i in range(8):
            self.scaled_running_sprites.append(pygame.transform.scale(pygame.image.load(rf'C:\Users\gald1\Desktop\stufff\Coding projects\MyPyGame\Samurai-Pygame\assets\Samurai1\02-Run/__Samurai1_Run_00{i}.png'), (self.width, self.height)))
        print(self.scaled_running_sprites)

        
        for sprite in self.sprites:
            scaled_image = pygame.transform.scale(sprite, (self.width, self.height))
            self.scaled_sprites.append(scaled_image)
        

        self.image = self.scaled_sprites[self.attack_counter]
        self.anim_rect = self.image.get_rect(width=250, height=150)
        self.rect = pygame.Rect((x_pos, y_pos), (self.width, self.height))
    def draw(self):
        if self.is_attacking:
            self.attack_counter += 0.4
            if self.attack_counter >= len(self.sprites):
                self.is_attacking = False
                self.attack_counter = 0
            self.image = self.scaled_sprites[int(self.attack_counter)]
            WIN.blit(self.image, self.rect)
        elif self.is_running:
            self.running_counter += 0.5
            if self.running_counter >= len(self.scaled_running_sprites):
                self.running_counter = 0
            
            self.running_image = self.scaled_running_sprites[int(self.running_counter)]
            WIN.blit(self.running_image, self.rect)
        else:
            WIN.blit(SAMURAI_IMAGE_SCALED, self.rect)
    
    def attack(self):
        self.is_running = False
        self.is_attacking = True
        print(self.is_attacking)
        self.attack_counter = 0

    def run(self):
        if not self.is_attacking:
            self.is_running = True
            self.running_counter = 0
        
    
    def stop_run(self):
        self.is_running = False

    


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.sprites = []
        width, height = 250, 150
        for i in range(8):
            self.sprites.append(pygame.transform.scale(pygame.transform.flip(pygame.image.load(rf'C:\Users\gald1\Desktop\stufff\Coding projects\MyPyGame\Samurai-Pygame\assets\Samurai1\02-Run/__Samurai1_Run_00{i}.png'), True, False), (width, height)))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect(width=170, height=130)
        self.rect.topleft = [pos_x, pos_y]

    def update(self, lives):
        self.current_sprite += 0.5
        

        
        

        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]
        self.rect.x += 3
        if self.rect.x > 725:
            lives[0] -= 1 
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
        self.collision_count = 0
        self.speed = 8  # Speed at which the slash moves
        self.ult_speed = 3
        self.image = pygame.image.load(os.path.join('assets', 'ultimateslash.png'))
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.ult_image = pygame.transform.scale(self.image, (250, 250))
        self.ult_collision_count = 0
    def move(self):
        self.x -= self.speed

    def ult_move(self):
        self.x -= self.ult_speed

    def draw(self, surface):
        self.rect = self.image.get_rect(width=80, height=80)
        self.rect.center = (self.x, self.y + 50)
        surface.blit(self.image , self.rect)


    def ultimate(self, surface):
        # Create rect with the size of the ult_image
        self.rect = self.ult_image.get_rect(center=(self.x, self.y + 50))
        # Inflate the hitbox if needed
        self.hitbox = self.rect.inflate(-300, -300)  # Adjust inflate values as needed
        surface.blit(self.ult_image, self.rect)


def draw_window(samurai, slashes, sprites, enemy, text, textRect, lives, score, score_rect, game_over, score_text, ult_bar, ult_slashes):
    WIN.blit(BG_IMAGE, (0, 0))
    WIN.blit(BATTLEGROUND_IMAGE, (0, 0))
    samurai.draw()
    WIN.blit(text, textRect)
    WIN.blit(score_text, score_rect)
    ult_bar.draw(WIN)
    
    if slashes:
        for slash in slashes:
            slash.draw(WIN)
            slash.move()
            if slash.x < -50:
                slashes.remove(slash)
    if ult_slashes:
        for slash in ult_slashes:
            slash.ultimate(WIN)
            slash.ult_move()
            if slash.x < -90:
                ult_slashes.remove(slash)
    if sprites and enemy:
        sprites.draw(WIN)
        sprites.update(lives=lives)
    
    if game_over:
        draw_game_over(text="GAME OVER", text_col=(255, 0, 0), font_size=40, x=330, y=100)
        draw_game_over(text=f"Score : {score[0]}", text_col=(255, 0, 0), font_size=30, x=386, y=145)
        draw_game_over(text=f"Press SPACE to play again", text_col=(255, 0, 0), font_size=20, x=330, y=180)


    

    pygame.display.update()

def main():
    run = True
    pygame_font = pygame.font.Font(r'C:\Users\gald1\Desktop\stufff\Coding projects\MyPyGame\Samurai-Pygame\assets\Minecraft.ttf', 16)
    samurai = Samurai(600, 160)
    samurai_char = samurai.rect
    slash = None
    slashes = []
    ult_slashes = []
    ult_bar = UltimateBar(x=400, y=30, w=100, h=40, max_ult=5, text_x=330, text_y=80)
    enemy = None
    moving_sprites = None
    game_over = False
    start_time = pygame.time.get_ticks()
    moving_sprites = pygame.sprite.Group()
    ult_ready = False
    lives = [3]
    score = [0]
    start_cd = 0
    
    while run:

        clock.tick(FPS)
        if ult_bar.ult >= ult_bar.max_ult:
            ult_ready = True

        if game_over == False:
            score_text = pygame_font.render(f'Score: {score[0]}', True, (255, 0, 0))
            score_rect = score_text.get_rect()
            score_rect.center = (900 // 2, 10)
            text = pygame_font.render(f'Lives: {lives[0]}', True, (255, 0, 0))
            textRect = text.get_rect()
            textRect.center = (33, 13)
            current_time = pygame.time.get_ticks()
            random_appearence_time_enemy = random.randint(300, 600)
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
                            slash.collision_count += 1
                            if slash.collision_count == 2:
                                slashes.remove(slash)
                            score[0] += 1
                            if ult_bar.ult < 5:
                                ult_bar.ult += 1
                            print(ult_bar.ult)
                            moving_sprites.remove(sprite)
            if len(ult_slashes) > 0:
                for sprite in moving_sprites:
                    for ult_slash in ult_slashes:
                        if sprite.rect.colliderect(ult_slash):
                            score[0] += 1
                            ult_bar.ult += 0.2
                            ult_slash.ult_collision_count += 1
                            if ult_slash.ult_collision_count == 10:
                                ult_slashes.remove(ult_slash)
                            print('ult hit')
                            moving_sprites.remove(sprite)

        else:
            moving_sprites.empty()
            
            ult_ready = False
            ult_bar.ult = 0
            for slash in slashes:
                slashes.remove(slash)
            for ult_slash in ult_slashes:
                ult_slashes.remove(ult_slash)
                key = pygame.key.get_pressed()
                if key[pygame.K_SPACE]:
                    game_over = False
                    print('space pressed after lose')
                    score[0] = 0
                    lives[0] = 3
                


    

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print(f"start_Cd : {start_cd}")
                    if current_time - start_cd >= 2000 or start_cd == 0:
                        start_cd = pygame.time.get_ticks()
                        samurai.attack()
                        slash = Slash(x=samurai.rect.x - 30, y=samurai.rect.y)
                        slashes.append(slash)
                if event.key == pygame.K_q:
                    if ult_ready:
                        ult_ready = False
                        ult_bar.ult = 0
                        ult_slash = Slash(x=samurai.rect.x - 30, y=samurai.rect.y)
                        samurai.attack()
                        ult_slashes.append(ult_slash)
                if event.key == pygame.K_LEFT:
                    samurai.run()
                if event.key == pygame.K_RIGHT:
                    samurai.run()
                if event.key == pygame.K_DOWN:
                    samurai.run()
                if event.key == pygame.K_UP:
                    samurai.run()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    samurai.stop_run()
                if event.key == pygame.K_RIGHT:
                    samurai.stop_run()
                if event.key == pygame.K_DOWN:
                    samurai.stop_run()
                if event.key == pygame.K_UP:
                    samurai.stop_run()
                
        if lives[0] <= 0:
            game_over = True
        

                
        draw_window(samurai, slashes, sprites=moving_sprites, enemy=enemy, text=text, textRect=textRect, lives=lives, score_text=score_text, score=score, score_rect=score_rect, game_over=game_over, ult_bar=ult_bar, ult_slashes=ult_slashes)
        if game_over == False:
            keys_pressed = pygame.key.get_pressed()
            samurai_movement(keys=keys_pressed, samurai=samurai_char)
       

if __name__ == '__main__':

    main()