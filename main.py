import math
import random
import matplotlib
import pygame
import sys
from pygame.locals import *

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCREEN_HEIGHT = 400
SCREEN_WIDTH = 600

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")


def main():

    loop()


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("ball.png")
        self.rect = self.image.get_rect()
        self.rect.center = (300, 200)

    # def move(self):
    #     pressed_keys = pygame.key.get_pressed()
    #    # if pressed_keys[K_UP]:
    #     #self.rect.move_ip(0, -5)
    #    # if pressed_keys[K_DOWN]:
    #     # self.rect.move_ip(0,5)

    #     if self.rect.left > 0:
    #         if pressed_keys[K_LEFT]:
    #             self.rect.move_ip(-5, 0)
    #     if self.rect.right < SCREEN_WIDTH:
    #         if pressed_keys[K_RIGHT]:
    #             self.rect.move_ip(5, 0)

    # def pos(self,x):
    #     self.rect.center = (200, 300 + x)

# class Beam(pygame.sprite.Sprite):
#     def __init__(self):
#         super().__init__()
#         self.image = pygame.image.load("beam.png")
#         self.rect = self.image.get_rect()
#         self.rect.center = (200, 300)

def loop():

    g = 9.8
    m = 100
    x = 0
    v = 0
    a = 0
    ang = 0
    adj = 1

    P1 = Ball()
    # B1 = Beam()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(P1)
    # all_sprites.add(B1)

    # Simulation Loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT]:
            ang = ang + adj/FPS
        if pressed_keys[K_RIGHT]:
            ang = ang - adj/FPS
                
        if ang < -math.pi/2:
            ang = -math.pi/2
        elif ang > math.pi/2:
            ang = math.pi/2


        g, m, x, v, a, ang, adj = simulation(g, m, x, v, a, ang, adj)

        print(f"x = {x}, angle = {ang *180/math.pi}")

        DISPLAYSURF.fill(WHITE)

        ball_x, ball_y = ball_pos(x, ang)
        beam_start, beam_end = beam_pos(ang)

        for entity in all_sprites:
            DISPLAYSURF.blit(entity.image, entity.rect)
            entity.rect.center = (ball_x, ball_y)
        
        pygame.draw.line(DISPLAYSURF, BLACK, beam_start, beam_end, 5)
        
        # for entity in [B1]:
        #     DISPLAYSURF.blit(entity.image, entity.rect)
        #     entity.image = pygame.transform.rotate(entity.image, ang*180/math.pi)            

        pygame.display.update()
        FramePerSec.tick(FPS)


def simulation(g, m, x, v, a, ang, adj):
    
    # if x <= 0:
    #     ang = ang - adj/FPS
    # else:
    #     ang = ang + adj/FPS
    
    # if ang < -math.pi/4:
    #     ang = -math.pi/4
    # elif ang > math.pi/4:
    #     ang = math.pi/4

    a += -1 * ((math.sin(ang) * g) / m) / FPS
    # if a > 0:
    #     a -= 0.004 * math.cos(ang) * g * m
    # elif a < 0:
    #     a += 0.004 * math.cos(ang) * g * m

    v += a / FPS
    x += v / FPS
    if x < -10:
        x = -10
        v=0
        a=0
    elif x > 10:
        x = 10
        v=0
        a=0

    return g, m, x, v, a, ang, adj

def ball_pos(x, ang):
    if ang != 0:
        ball_x = x* math.cos(ang) *20 + SCREEN_WIDTH/2
        ball_y = - x*math.sin(ang) *20 + SCREEN_HEIGHT/2
    else:
        ball_x = x *20 + SCREEN_WIDTH/2
        ball_y = SCREEN_HEIGHT/2

    return ball_x, ball_y

def beam_pos(ang):
    
    beam_length = 200
    
    beam_start_x = SCREEN_WIDTH/2 - beam_length*math.cos(-ang)
    beam_start_y = SCREEN_HEIGHT/2 - beam_length*math.sin(-ang)
    beam_end_x = SCREEN_WIDTH/2 + beam_length*math.cos(-ang)
    beam_end_y = SCREEN_HEIGHT/2 + beam_length*math.sin(-ang)

    beam_start = (beam_start_x, beam_start_y)
    beam_end = (beam_end_x, beam_end_y)

    return beam_start, beam_end

if __name__ == "__main__":
    main()
