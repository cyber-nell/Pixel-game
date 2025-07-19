#notes
#add feature to move camera to enemy briefly when appears?
#different enemies == different ways to defeat e.g. wizards - puzzle, troll - fighting, etc
#enemy that changes keys when playing e.g swaps left and right key?
#add portals where glitches are
#crouch animation??


# to do: design health pack // write help section //  level 2 when all enemies are defeated...tbc // remove map class + excess code

import pygame  
import random  
import time
import csv
import os
import textwrap

from abc import ABC, abstractmethod
 


# GLOBAL VARIABLES  
WHITE = (255,255,255)  
GREEN = (8, 77,27)
BLUE = (0,160,180)
WIDTH = 700
HEIGHT = 500  
size  = (WIDTH, HEIGHT)  
screen = pygame.display.set_mode(size)  
pygame.display.set_caption("Magic Kingdom")
JUMP_STRENGTH = -10.5  
GROUND_Y = HEIGHT - 50
GRAVITY = 0.5
ene_health = 80
ene_mindamage = 10
hpack = []




#font settings
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 20)
text_surface = font.render('health:', False, (0, 0, 0))








#classes
            
#button
class Button():
    def __init__(self, text,pos, font, colour, hovering):
        self.text = text
        self.pos = pos
        self.font= font
        self.colour = colour
        self.hovering = hovering 
        self.render_text()

    #Text to display    
    def render_text(self):
        self.text_surface = self.font.render(self.text, True, self.colour)
        self.text_rect = self.text_surface.get_rect(center = self.pos)

    def draw(self,screen):
        screen.blit(self.text_surface, self.text_rect)

    def update(self,menu_mouse):
        if self.text_rect.collidepoint(menu_mouse):
            self.text_surface = self.font.render(self.text, True, self.hovering)
        else:
            self.text_surface = self.font.render(self.text, True, self.colour)
    
    #checking if button is pressed
    def checkforInput(self, menu_mouse, mouse_click):
        if self.text_rect.collidepoint(menu_mouse):
            if mouse_click:
                return True
        return False
    
    #change colour when button pressed
    def changeColour(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering)
        else:
            self.text = self.font.render(self.text_input, True, self.colour)



#Wall class
class Wall(pygame.sprite.Sprite):
   
    def __init__(self, height, width):
        super().__init__()
        ground_image = pygame.image.load("D:\images/ground.png")
        self.image =  pygame.Surface([width, height])
        self.rect = self.image.get_rect()
        self.image.blit(ground_image, (0,0))  

#moving walls
class M_X_Walls(Wall):
    def __init__(self,height,width,start_x):
        super().__init__(height,width)
        self.vel = 3
        self.direction = 1
        self.start = start_x
        self.end = start_x + 100
       
    def motion(self):
        self.rect.x += self.vel * self.direction

        if self.rect.x >= self.end:
            self.direction = -1

        elif self.rect.x <= self.start:
            self.direction = 1

        
        
#ground class

class Tile(pygame.sprite.Sprite):
    def __init__(self,x,y,):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("D:\images/ground.png")
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y
        
    def draw(self,surface):
        surface.blit(self.image, (self.rect.x,self.rect.y))
        



# Sprite Class  
class Sprite(pygame.sprite.Sprite):  


    def __init__(self, height, width):  
        super().__init__()
        
        #loading images
        self.sprites = []
        self.sprites.append(pygame.image.load('D:\images/player/idle_1.png'))
        self.sprites.append(pygame.image.load('D:\images/player/idle_2.png'))
    
        #setting intial picture    
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = [width,height] 

        
        self.isjump = False
        self.vely = 0
        self.velx = 0
        self.rect.x =250
        self.rect.y = GROUND_Y - self.rect.height
        self.health = 100
        
    

    #updating sprite functions
    def update(self, surfaces):
            self.vely += GRAVITY
            self.rect.y += self.vely
            key = pygame.key.get_pressed()

            

         # animation, depending on what sprite is doing
            if key[pygame.K_w]==True and self.velx < 0:
                self.sprites = []
                self.sprites.append(pygame.image.load('D:\images/player/left_walk_weapon1.png'))
                self.sprites.append(pygame.image.load('D:\images/player/left_walk_weapon2.png'))
            elif key[pygame.K_w]==True == True and self.velx > 0:
                self.sprites = []
                self.sprites.append(pygame.image.load('D:\images/player/right_walk_weapon1.png'))
                self.sprites.append(pygame.image.load('D:\images/player/right_walk_weapon2.png'))
            elif self.velx > 0:
                self.sprites=[]
                self.sprites.append(pygame.image.load('D:\images/player/right_walk.png'))
                self.sprites.append(pygame.image.load('D:\images/player/right_walk2.png'))
            elif self.velx < 0:
                self.sprites = []
                self.sprites.append(pygame.image.load('D:\images/player/left_walk.png'))
                self.sprites.append(pygame.image.load('D:\images/player/left_walk2.png'))
            else:
                self.sprites = []
                self.sprites.append(pygame.image.load('D:\images/player/idle_1.png'))
                self.sprites.append(pygame.image.load('D:\images/player/idle_2.png'))



           
            self.current_sprite += 0.1

            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0

            self.image = self.sprites[int(self.current_sprite)]
            self.image.set_colorkey((255,255,255))

            #if sprite goes off screen
            if self.rect.y > 500:
                self.death()



 

       #checking for collsions with the surfaces
            wall_collision = pygame.sprite.spritecollide(self, surfaces, False)
           
            for surfaces in wall_collision:
                if self.velx > 0 and self.rect.left < surfaces.rect.left:
                    self.rect.right = surfaces.rect.left -10
                    self.rect.x -=3
                    self.velx = 0

                #if it collides walking left
                if self.velx < 0 and self.rect.right > surfaces.rect.right:
                    self.rect.left = surfaces.rect.right + 10
                    self.rect.x +=3
                    self.velx = 0

                    if surfaces in x_moving:
                        self.rect.x = self.rect.right

                #if it collides walking right
                if self.vely > 0:
                    self.rect.bottom = surfaces.rect.top
                    self.vely = 0
                    self.isjump = False
                    
                    if surfaces in x_moving:
                        self.rect.x += surfaces.vel * surfaces.direction
                
                if self.vely < 0:
                    self.rect.top = surfaces.rect.bottom
                    self.vely = 0
               
    #restart
    def death(self):
        self.health -= ene_mindamage        
        self.rect.x = 100
        self.rect.y = 0 
        
        if self.health <= 0:
            self.health = 0
            game_over()
    
    
    #health bar
    def health_bar(self,surface):
        bar_w = 200
        bar_h = 15
        health_ratio = self.health/100
        bar_colour = (255,0,0)
        bar_x = 500
        bar_y = 20
        
        #black
        pygame.draw.rect(surface, (0,0,0), (bar_x-5, bar_y-5, bar_w+15, bar_h+10))
        
        #white
        pygame.draw.rect(surface, (255,255,255), (bar_x-3, bar_y-3, bar_w+10, bar_h+5  ))
        
        #red
        pygame.draw.rect(surface, (bar_colour), (bar_x, bar_y, bar_w*health_ratio, bar_h  ))
        
        
    
    #Moving sprite
    def MoveSprite(self):
        key = pygame.key.get_pressed()

        if key[pygame.K_LEFT]==True:
            self.moveLeft()

        elif key[pygame.K_RIGHT]==True:
            self.moveRight()

        elif key[pygame.K_SPACE]==True:
            self.jump()
        else:
            self.velx = 0
            

   
 #movement funcions        
    def moveRight(self):
        self.velx = 5
        self.rect.x += self.velx
    def moveLeft(self):
        self.velx = -5
        self.rect.x += self.velx  
    def jump(self):
        if not self.isjump:
                self.vely = JUMP_STRENGTH
                self.isjump = True
    

        

class Enemies(pygame.sprite.Sprite):
    def __init__(self, height, width,posx, posy, health):
        super().__init__()

        #setting images
        self.pics = []
        self.pics.append(pygame.image.load('D:\images/enemies/hooded figure/idle_1.png'))
        self.pics.append(pygame.image.load('D:\images/enemies/hooded figure/idle_2.png'))

        #setting start pic
        self.current_sprite = 0
        self.image = self.pics[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = [width,height]
        self.rect.x = posx
        self.rect.y = posy
        self.health = health
        

    def ene_update(self):
        key = pygame.key.get_pressed()

        #animation
        self.current_sprite += 0.1

        if self.current_sprite >= len(self.pics):
            self.current_sprite = 0

        self.image = self.pics[int(self.current_sprite)]
        self.image.set_colorkey((0,0,0))

        # Calculate the distance between the enemy and the player
        distance_x = sprite_.rect.x - self.rect.x
        distance_y = sprite_.rect.y - self.rect.y
        distance = (distance_x ** 2 + distance_y ** 2) ** 0.5

        # Move the enemy toward the player - pythagorous theorem
        speed = 2

        if distance < 300:
            if distance != 0:
                self.rect.x += speed * distance_x / distance
                self.rect.y += speed * distance_y / distance
            
        if pygame.sprite.collide_rect(self, sprite_):
            if key[pygame.K_w]==True and sprite_.velx!=0:
                self.death()
            else:
                sprite_.death()
                

    def health_bar(self,surface):
        bar_w = 90
        bar_h = 10
        health_ratio = self.health/100
        bar_colour = (255,0,0)
        bar_x = self.rect.x -10 + camera.camera.topleft[0]
        bar_y = self.rect.y -15 + camera.camera.topleft[1]
        
        #black
        pygame.draw.rect(surface, (0,0,0), (bar_x-5, bar_y-5, bar_w-3, bar_h+10  ))
        
        #white
        pygame.draw.rect(surface, (255,255,255), (bar_x-3, bar_y-3, bar_w-7, bar_h+5  ))
        
        #red
        pygame.draw.rect(surface, (bar_colour), (bar_x, bar_y, bar_w*health_ratio, bar_h  ))

    def death(self):
        self.health -= 5     
        
        if self.health <= 0:
            self.health = 0
            self.kill()
            self.rect.y=1000
            
        if self.health % 2 ==0:
            self.retreat()
    
    def retreat(self):
        speed = 200
        #moves enemy away from player
        distance_x = sprite_.rect.x - self.rect.x
        distance_y = sprite_.rect.y - self.rect.y
        distance = (distance_x ** 2 + distance_y ** 2) ** 0.5
        
        self.rect.x -= speed * distance_x / distance
        self.rect.y -= speed * distance_y / distance
            

            

class Health_pack(pygame.sprite.Sprite): 
    def __init__(self, height, width,posx, posy):
        super().__init__()

        self.pics = []
        self.pics.append(pygame.image.load('D:\images/health pack/health pack1.png'))
        self.pics.append(pygame.image.load('D:\images/health pack/health pack2.png'))
        self.pics.append(pygame.image.load('D:\images/health pack/health pack3.png')) 

        self.current_sprite = 0
        self.image = self.pics[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = [width,height]

        self.rect.x = posx
        self.rect.y = posy

    def health_update(self):
        self.current_sprite += 0.1

        if self.current_sprite >= len(self.pics):
            self.current_sprite = 0
        
        self.image = self.pics[int(self.current_sprite)]
        self.image.set_colorkey((0,0,0))


        if pygame.sprite.collide_rect(self, sprite_) and sprite_.health < 100:
            sprite_.health +=10 
            self.kill()
            self.rect.y -=700

        
        
 



class Camera():
    def __init__(self,width,height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
       
    def apply(self,entity):
        return entity.rect.move(self.camera.topleft)

   #follows sprite + keeps in center
    def update (self, sprite_,surfaces):
        x = -sprite_.rect.centerx + int(WIDTH / 2)
        y = -sprite_.rect.centery + int(HEIGHT / 2)
       
        x = max(min(0, x), -(self.width - WIDTH))
        y = max(min(0, y), -(self.height - HEIGHT))
       
        self.camera = pygame.Rect (x, y, self.width, self.height)
       
       
     
     
 
   
pygame.init()  
 

#calling sprites
all_sprites_list = pygame.sprite.Group()  
sprite_ = Sprite(30, 30)
enemy = []
n_enemies = 0 

#map = Map('D:\images/world.csv')





#generating moving platforms
x_moving = [' ']*7
n_xmoving = 7
start = [500,1800,2355, 2700,4900,5600,6500]
y = [230,200,100,120,200,210,340]

nums = 1
#creating a set number with certain coordinates
for i in range (n_xmoving):
    str_nums =str(nums)
    names = 'xmoving' + str_nums
    names = M_X_Walls(50,200,start[i])
    x_moving[i] = names
    names.rect.x = start[i]
    names.rect.y = y[i]
    nums = nums + 1
    



#generating wall postions
walls =[' ']*50
nwalls = 50
xcoordinates = [0,200,1100,1300,3100,6100,6300,0, 350, 600,800,720,800,1200, 1500,1700,2100,2100,2100,2100,2100,2100,2100,2300,2300,2300,2300,2300,2500,2500,2500,2700,3350,3550,3750,3900,4050,4150,4500,4700,5200,5400,5800,6900,6900,6800,6900,6800,6900,6800]
ycoordinates = [480,480,480,480,480,480,480,375,380, 430, 430,400,285,345, 310,290,150,200,250,300,350,400,450,250,300,350,400,450,350,400,450,450,380,340,340,390,440,270,350,300,250,100,300,300,350,350,400,400,450,450]


num = 1
#creating the walls
for i in range (nwalls):
    str_num = str(num)
    name = 'Wall' + str_num
    name = Wall(50,200)
    walls[i] = name
    name.rect.x = xcoordinates[i]
    name.rect.y = ycoordinates [i]
    num = num + 1




#wall positions
surfaces = pygame.sprite.Group()
surfaces.add(walls,x_moving)


#generating health pack + positions

for i in range (5):
    posx = random.randint(0,7000)
    posy = random.randint(200,400)
    hpack.append(Health_pack(50, 50, posx, posy))

    #recreating health pack if in unreachable place
    if pygame.sprite.spritecollide(hpack[i], surfaces,True):
        i = i-1


all_sprites_list.add(sprite_, surfaces,hpack)

#implementing camera
camera = Camera(WIDTH * 10, HEIGHT)

#spawning enemy
def spawn():
        #need time for enemy to spawn, need to increase damage + health of enemy every 4 spawns (change character every 4th spawn)
        
        posx = random.randint(sprite_.rect.x - 200, sprite_.rect.x + 500)
        posy = random.randint(0,500)
        
        health = ene_health
        
        new_ene = Enemies(30,30, posx, posy, health)
        
        return new_ene


#running game
exit = True
clock = pygame.time.Clock()  
time_interval = 20000
pygame.time.set_timer(pygame.USEREVENT, time_interval)


#menu
def draw_start_menu():
    pygame.display.set_caption('Menu')
    font = pygame.font.SysFont('Comic Sans MS', 80)
    play_button = Button('PLAY', (350,150), font, (255,255,255), BLUE)
    help_button = Button('HELP', (350,350), font, (255,255,255), BLUE)

    while True:
        screen.fill((0,0,0))

        menu_mouse = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]
        
        #drawing buttons onto screen
        play_button.update(menu_mouse)
        play_button.draw(screen)
        help_button.update(menu_mouse)
        help_button.draw(screen)

        if play_button.checkforInput(menu_mouse, mouse_click):
            return 
        
        if help_button.checkforInput(menu_mouse, mouse_click):
            return help_screen()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                
        pygame.display.flip()
        clock.tick(60)
        
        

#play screen
def play():
    global n_enemies
    exit = True
     
    while exit:  


        for event in pygame.event.get():  


            if event.type == pygame.QUIT:  
                
                pygame.quit()
                exit = False
                
            if event.type == pygame.USEREVENT:
                if n_enemies < 5:
                    new_ene = spawn()
                    all_sprites_list.add(new_ene)
                    enemy.append(new_ene)
                    n_enemies = n_enemies +1
                



            if sprite_.health == 0:
                draw_start_menu()

    
        pygame.display.update()

        #moving the walls
        for i in x_moving:
            i.motion()

        #moving the sprite
        sprite_.MoveSprite()
        all_sprites_list.update(surfaces) 
        camera.update(sprite_,surfaces)
        screen.fill(BLUE)
        sprite_.health_bar(screen)
        #HP_generation()

        #updating sprite images + drawing on screen
        for sprite in all_sprites_list:
            screen.blit(sprite.image, camera.apply(sprite))
        
        for current_ene in enemy:
            current_ene.ene_update()
            current_ene.health_bar(screen)
        
        for current_h in hpack:
            current_h.health_update()

            
        
        screen.blit(text_surface,(425,10))
    

            
        pygame.display.flip()  
        clock.tick(60)  
        
#help screen
def help_screen():
    pygame.display.set_caption('Menu')
    font = pygame.font.SysFont('Comic Sans MS', 20)
    help_button = Button('Main Menu', (50,10), font, (255,255,255), BLUE)

    
    while True:
        screen.fill((0,0,0))

        menu_mouse = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]
        menu_text = font.render('Help screen', True, (255,255,255))
        
        #display main menu button
        help_button.update(menu_mouse)
        help_button.draw(screen)

        if help_button.checkforInput(menu_mouse, mouse_click):
            return draw_start_menu()
        
        #display help text
        file = open("D:Help menu.txt", "r")
        words = file.read().strip()
        Y=0
        file.close()
        contents = textwrap.TextWrapper(width=70)
        after_Wrap = contents.wrap(text= words)
        for i in after_Wrap:
            Y+=50
            wrapped_text = font.render(f"{i}",False, (255,255,255))
            screen.blit(wrapped_text,(0,Y))


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                
        pygame.display.flip()
        clock.tick(60)

#game over        
def game_over():
    pygame.display.set_caption('Menu')
    font = pygame.font.SysFont('Comic Sans MS', 20)
    large_font = pygame.font.SysFont('Comic Sans MS', 100)
    try_button = Button('try again', (350,400), font, (255,255,255), BLUE)
    Game_over = large_font.render('GAME OVER', False, (255,0,0))

    while True:
        screen.fill((0,0,0))
        screen.blit(Game_over, (60,150))

        menu_mouse = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]
        menu_text = font.render('Help screen', True, (255,255,255))
        
        
        
        try_button.update(menu_mouse)
        try_button.draw(screen)

        if try_button.checkforInput(menu_mouse, mouse_click):
            reset()
            return draw_start_menu()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                
        pygame.display.flip()
        clock.tick(60)

#revival
def reset():
    sprite_.health = 100
    for i in enemy:
        enemy.remove(i)
        i.kill()
    play()


    



pygame.init()
screen = pygame.display.set_mode(size)
draw_start_menu()
play()


