import pygame
from pygame.locals import *
import time
import random

SIZE= 40

class Apple:
    def __init__(self,parent_screen):
        self.parent_screen= parent_screen
        self.image=pygame.image.load("resources/apple.jpg").convert()
        self.x= SIZE * 3
        self.y= SIZE * 3
    
    def draw(self):
        self.parent_screen.blit(self.image, (self.x,self.y))
        pygame.display.flip()

    def move(self):
        self.x= random.randint(1,24)*SIZE
        self.y=random.randint(1,19)*SIZE

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.play_bg_music()
        self.surface=pygame.display.set_mode((1000,800))
        self.snakes=Snakes(self.surface,1)
        self.snakes.draw()
        self.apple=Apple(self.surface)
        self.apple.draw()

    def render_bg(self):
        bg=pygame.image.load("resources/background.jpg")
        self.surface.blit(bg,(0,0))

    def display_score(self):
        font= pygame.font.SysFont('arial', 30)
        score=font.render(f"Score: {self.snakes.length}", True, (255,255,255))
        self.surface.blit(score,(850,10))

    def play_bg_music(self):
        pygame.mixer.music.load("resources/bg_music_1.mp3")
        pygame.mixer.music.play(-1,0)

    def show_game_over(self):
        self.render_bg()
        font= pygame.font.SysFont('arial', 30)
        line1=font.render(f"Game is over! Your score is {self.snakes.length}", True, (255,255,255))
        self.surface.blit(line1,(200,300))
        line2=font.render(f"To play again press Enter. To exit press Escape!", True, (255,255,255))
        self.surface.blit(line2,(200,350))
        pygame.display.flip()
        pygame.mixer.music.pause()

    def play(self):
        self.render_bg()
        self.snakes.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        #snake colliding with apple
        if self.is_collision(self.snakes.x[0], self.snakes.y[0], self.apple.x, self.apple.y):
            sound= pygame.mixer.Sound("resources/ding.mp3")
            pygame.mixer.Sound.play(sound)
            self.snakes.increase_length()  
            self.apple.move() 

        #snake colliding with itself
        for i in range(2, self.snakes.length):
             if self.is_collision(self.snakes.x[0], self.snakes.y[0], self.snakes.x[i], self.snakes.y[i]):
                sound= pygame.mixer.Sound("resources/crash.mp3")
                pygame.mixer.Sound.play(sound)
                raise "Game Over!"

    def is_collision(self,x1,y1,x2,y2):
        if x1>=x2 and x1<=x2 +SIZE:
            if y1>=y2 and y1<=y2+SIZE:
                return True
        return False

    def reset(self):
        self.snakes=Snakes(self.surface,1)
        self.apple=Apple(self.surface)

    def run(self):
        running=True
        pause= False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key== K_ESCAPE:
                        running= False
                    if event.key== K_RETURN:
                        pygame.mixer.music.unpause()
                        pause=False
                    if not pause:
                        if event.key== K_UP:
                            self.snakes.move_up()
                        if event.key == K_DOWN:
                            self.snakes.move_down()
                        if event.key== K_RIGHT:
                            self.snakes.move_right()
                        if event.key== K_LEFT:
                            self.snakes.move_left()
                if event.type == QUIT:
                    running= False
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                time.sleep(5)
                pause=True
                self.reset()
            time.sleep(0.2)


class Snakes:
    def __init__(self, parent_screen,length):
        self.parent_screen= parent_screen
        self.block= pygame.image.load("resources/block.jpg").convert()
        self.length= length
        self.x=[SIZE]*length
        self.y=[SIZE]*length
        self.direction="up"


    def increase_length(self):
        self.length+=1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):
        
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i],self.y[i]))
        pygame.display.flip()

    def move_up(self):
        self.direction="up"
    def move_down(self):
        self.direction="down"
    def move_right(self):
        self.direction="right"
    def move_left(self):
        self.direction="left"
    def walk(self):
        for i in range(self.length-1, 0,-1):
            self.x[i]=self.x[i-1]
            self.y[i]=self.y[i-1]
        if self.direction=="left":
            self.x[0]-=SIZE
        elif self.direction=="right":
            self.x[0]+=SIZE
        elif self.direction=="up":
            self.y[0]-=SIZE
        elif self.direction=="down":
            self.y[0]+=SIZE
        self.draw()
    


if __name__=="__main__":
    
    game=Game()
    game.run()

    
    