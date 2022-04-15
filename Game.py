from turtle import screensize
import pygame,sys,random
from pygame.math import Vector2

class SNAKE:
    def __init__(self):#class constructor
        self.body = [Vector2((size)/2+1,(size)/2-1),Vector2((size)/2,(size)/2-1),Vector2((size)/2-1,(size)/2-1)]
        self.direction = Vector2(1,0)
        self.munch = False
        self.game_over = False
        #importing head images
        self.head_up = pygame.image.load('assets/head.png').convert_alpha()
        self.head_down = pygame.transform.rotate(self.head_up,180)
        self.head_left = pygame.transform.rotate(self.head_up,90)
        self.head_right = pygame.transform.rotate(self.head_up,-90)
        #importing body images
        self.body_horizontal = pygame.image.load('assets/body.png').convert_alpha()
        self.body_vertical = pygame.transform.rotate(self.body_horizontal,90)
        self.body_tr = pygame.image.load('assets/body_corner.png').convert_alpha()
        self.body_tl = pygame.transform.rotate(self.body_tr,90)
        self.body_br = pygame.transform.rotate(self.body_tr,-90)
        self.body_bl = pygame.transform.rotate(self.body_tr,180)
        #importing tail images
        self.tail_up = pygame.image.load('assets/tail.png').convert_alpha()
        self.tail_down = pygame.transform.rotate(self.tail_up,180)
        self.tail_right = pygame.transform.rotate(self.tail_up,-90)
        self.tail_left = pygame.transform.rotate(self.tail_up,90)

    def draw_snake(self):
        #Draw Head
        x = self.body[0].x*cell_size
        y = self.body[0].y*cell_size
        snake_rect = pygame.Rect(x,y,cell_size,cell_size)
        if self.body[0]-self.body[1]==Vector2(1,0):
            screen.blit(self.head_right,snake_rect)
        if self.body[0]-self.body[1]==Vector2(-1,0):
            screen.blit(self.head_left,snake_rect)
        if self.body[0]-self.body[1]==Vector2(0,1):
            screen.blit(self.head_down,snake_rect)
        if self.body[0]-self.body[1]==Vector2(0,-1):
            screen.blit(self.head_up,snake_rect)
        #pygame.draw.rect(screen,(20,190,10),snake_rect)

        for i in range(len(self.body))[1:-1]:
            next=self.body[i+1]
            curr=self.body[i]
            prev=self.body[i-1]
            
            x = curr.x*cell_size
            y = curr.y*cell_size
            snake_rect = pygame.Rect(x,y,cell_size,cell_size)

            #snake straight
            if next.y-curr.y==0 and curr.y-prev.y==0:
                screen.blit(self.body_horizontal,snake_rect)
            
            if next.x-curr.x==0 and curr.x-prev.x==0:
                screen.blit(self.body_vertical,snake_rect)
            ##snake curves
            #bottom left
            if next-curr==Vector2(-1,0) and curr-prev==Vector2(0,-1):
                screen.blit(self.body_bl,snake_rect)
            if next-curr==Vector2(0,1) and curr-prev==Vector2(1,0):
                screen.blit(self.body_bl,snake_rect)
            #bottom right
            if next-curr==Vector2(1,0) and curr-prev==Vector2(0,-1):
                screen.blit(self.body_br,snake_rect)
            if next-curr==Vector2(0,1) and curr-prev==Vector2(-1,0):
                screen.blit(self.body_br,snake_rect)
            #top left
            if next-curr==Vector2(0,-1) and curr-prev==Vector2(1,0):
                screen.blit(self.body_tl,snake_rect)
            if next-curr==Vector2(-1,0) and curr-prev==Vector2(0,1):
                screen.blit(self.body_tl,snake_rect)
            #top right
            if next-curr==Vector2(1,0) and curr-prev==Vector2(0,1):
                screen.blit(self.body_tr,snake_rect)
            if next-curr==Vector2(0,-1) and curr-prev==Vector2(-1,0):
                screen.blit(self.body_tr,snake_rect)
            
        
        #Draw Tail
        tail_index=len(self.body)-1
        x = self.body[tail_index].x*cell_size
        y = self.body[tail_index].y*cell_size
        snake_rect = pygame.Rect(x,y,cell_size,cell_size)
        if self.body[tail_index-1]-self.body[tail_index]==Vector2(-1,0):
            screen.blit(self.tail_right,snake_rect)
        if self.body[tail_index-1]-self.body[tail_index]==Vector2(1,0):
            screen.blit(self.tail_left,snake_rect)
        if self.body[tail_index-1]-self.body[tail_index]==Vector2(0,-1):
            screen.blit(self.tail_down,snake_rect)
        if self.body[tail_index-1]-self.body[tail_index]==Vector2(0,1):
            screen.blit(self.tail_up,snake_rect)

    def move_snake(self):
        if self.munch==False:
            self.body.pop(len(self.body)-1)
        if self.munch==True:
            self.munch=False
        self.body.insert(0,self.body[0]+self.direction)

        if self.body[0].x >= size or self.body[0].y >= size or self.body[0].x < 0  or self.body[0].y < 0:
            self.game_over=True
        for block in self.body[1:]:
            if block.x==self.body[0].x and block.y == self.body[0].y:
                self.game_over=True
                break

    def add_block(self):
        self.munch = True

class FOOD:
    def __init__(self):
        self.random_pos()
        self.food_image = pygame.image.load('assets/apple.png').convert_alpha()
    
    def draw_food(self):
        food_rect = pygame.Rect( self.pos.x*cell_size , self.pos.y*cell_size , cell_size, cell_size )
        screen.blit(self.food_image,food_rect)
        #pygame.draw.rect(screen,(200,70,90),food_rect)   
        ##draw.rect(surface,colour,rectangle)
    
    def random_pos(self):
        self.x=random.randint(0,size-1)
        self.y=random.randint(0,size-1)
        self.pos = Vector2(self.x,self.y)

class MAIN_GAME:
    def __init__(self):
        self.snake=SNAKE()
        self.food=FOOD()
    
    def draw_elements(self):
        self.draw_grass()
        self.food.draw_food()
        self.snake.draw_snake()
        self.draw_score()

    def update(self):
        self.check_gameover()
        self.check_munch()
        self.snake.move_snake()
        
    def check_munch(self):
        if self.food.pos == self.snake.body[0]:
            self.food.random_pos() #make new food if munched
            self.snake.add_block() #add extra block to snake
        
        # re randomize position if food is on snake
        for i in range(len(self.snake.body)):
            if self.snake.body[i]==self.food.pos:
                self.food.random_pos()
                i=0

    def check_gameover(self):
        if self.snake.game_over == True:
            pygame.time.wait(1000)
            # self.snake.body=[Vector2((size)/2,(size)/2-1),Vector2((size)/2-1,(size)/2-1),Vector2((size)/2-2,(size)/2-1)]
            # self.snake.direction = Vector2(1,0)
            # self.snake.game_over = False
            pygame.quit()
            sys.exit()

    def draw_grass(self):
        grass_color=(167,255,70)
        for row in range(size):
            for col in range(size):
                if (row+col)%2==0:
                    grass_rect=pygame.Rect(row*cell_size,col*cell_size,cell_size,cell_size)
                    pygame.draw.rect(screen,grass_color,grass_rect)

    def draw_score(self):
        score_txt="Score : "+str(len(self.snake.body)-3)
        score_surface=game_font.render(score_txt,True,(20,40,30))
        score_x = int(size*cell_size-80)
        score_y = int(size*cell_size-30)
        score_rect = score_surface.get_rect(center=(score_x,score_y))
        screen.blit(score_surface,score_rect)


pygame.init()
cell_size = 40
size = 16

#set max fps of game
clock = pygame.time.Clock()

#display surface of python
screen = pygame.display.set_mode((size*cell_size,size*cell_size))#width and height tuple


game_font = pygame.font.Font('assets/PoetsenOne-Regular.ttf',24)

#main object
game=MAIN_GAME()

#set timer
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,150)


#MAIN LOOP
while True:

    screen.fill((170,240,70))#(R  ,G  ,B  )

    game.draw_elements()
    

    #change the display
    pygame.display.update()

    for input in pygame.event.get():
        #set exit condition
        if input.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if input.type == SCREEN_UPDATE:
            game.update()
        if input.type == pygame.KEYDOWN:#if any key is pressed move accordingly
            if input.key == pygame.K_UP and game.snake.direction.y!=1 :
                game.snake.direction=Vector2(0,-1)
            if input.key == pygame.K_DOWN and game.snake.direction.y!=-1 :
                game.snake.direction=Vector2(0,1)
            if input.key == pygame.K_LEFT and game.snake.direction.x!=1 :
                game.snake.direction=Vector2(-1,0)
            if input.key == pygame.K_RIGHT and game.snake.direction.x!=-1 :
                game.snake.direction=Vector2(1,0)
            game.update()

    #step of fps
    clock.tick(60)
