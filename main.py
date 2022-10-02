import math
import random
import matplotlib
import pygame
import sys
from pygame.locals import *

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()
beam_length = 1
u = 0.002

BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCREEN_HEIGHT = 400
SCREEN_WIDTH = 600

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Balance")


def main():

    loop()


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("ball.png")
        self.rect = self.image.get_rect()
        self.rect.center = (300, 200)


def loop():
    g = 9.8
    m = 1
    x = 0
    v = 0
    a = 0
    ang = 0
    f_p = 0
    adj_pow = 1
    kp = 0.5  #0.5
    ki = 0.5  #0.5
    kd = 0.4  #0.4
    push_force = 5
    previous_err = 0
    integral = 0
    goal_options = [0, (beam_length/2)*0.5, -(beam_length/2)*0.5]
    goal_select = 0
    goal = goal_options[goal_select]
    P1 = Ball()

    all_sprites = pygame.sprite.Group()
    all_sprites.add(P1)
    # mode options manual = full player control
    mode = "manual"

    # Simulation Loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    mode = "manual"
                if event.key == pygame.K_p:
                    mode = "PID"
                if event.key == pygame.K_r:
                    x = 0
                    v = 1
                    a = 0
                    ang = 0.05
                    print("reset")

                if event.key == pygame.K_o:
                    goal_select += 1
                    if goal_select >= len(goal_options):
                        goal_select = 0

                    goal = goal_options[goal_select]

                    print(f"goal = {goal}")
                if event.key == pygame.K_1:
                    kp -= 0.01
                    print(f"kp = {kp}")
                if event.key == pygame.K_2:
                    kp += 0.01
                    print(f"kp = {kp}")
                if event.key == pygame.K_3:
                    kd -= 0.1
                    print(f"kd = {kd}")
                if event.key == pygame.K_4:
                    kd += 0.1
                    print(f"kd = {kd}")
                if event.key == pygame.K_5:
                    ki -= 0.01
                    print(f"ki = {ki}")
                if event.key == pygame.K_6:
                    ki += 0.01
                    print(f"ki = {ki}")

        # control switch
        if mode == "manual":
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[K_b]:
                ang = 0
            if pressed_keys[K_LEFT]:
                ang += adj_pow/FPS
            if pressed_keys[K_RIGHT]:
                ang -= adj_pow/FPS
            if pressed_keys[K_b]:
                ang = 0

        if mode == "PID":
            ang_set, previous_err, integral = PID_adj(kp, ki, kd,
                                                      x, goal, previous_err, integral)

            if abs(ang - ang_set) < adj_pow/100:
                ang = ang
            elif ang < ang_set:
                ang += adj_pow/FPS
            else:
                ang -= adj_pow/FPS

            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[K_LEFT]:
                f_p = - push_force
            if pressed_keys[K_RIGHT]:
                f_p = push_force

        if ang < -math.pi/2:
            ang = -math.pi/2
        elif ang > math.pi/2:
            ang = math.pi/2

        g, m, x, v, a, ang = simulation(g, m, x, v, a, ang, f_p)

        f_p = 0

        DISPLAYSURF.fill(WHITE)

        ball_x, ball_y = ball_pos(x, ang)
        beam_start, beam_end = beam_pos(ang)

        for entity in all_sprites:
            DISPLAYSURF.blit(entity.image, entity.rect)
            entity.rect.center = (ball_x, ball_y)

        pygame.draw.line(DISPLAYSURF, BLACK, beam_start, beam_end, 5)

        pygame.display.update()
        FramePerSec.tick(FPS)


def simulation(g, m, x, v, a, ang, f_p):

    # gravity acceleration
    a_g = -1 * (math.sin(ang) * g)

    # friction acceleration
    a_f = 0
    if v > 0:
        a_f = - u * math.cos(ang) * g
    elif v < 0:
        a_f = u * math.cos(ang) * g
    else:
        a_f = u * math.cos(ang) * g

    # acceleration from push force
    a_p = f_p / m

    v += a_p / FPS

    v_before_g = v

    # adjust velocity due to gravitational force
    v += a_g / FPS

    # save velocity before frictional acceleration is added
    v_before_f = v

    # adjust velocity due to frictional force
    v += a_f / FPS

    # see if grvitational force is sufficent to flip velocity sign, if so set velocity to zero
    if flipped_sign(v_before_f, v):
        v = 0

    # case where v=0 in last tick and small beam angle is insufficent to overcome gravity
    if v_before_g == 0 and abs(a_g) < abs(a_f) and flipped_sign(a_g, a_f):
        v = 0

    x += v / FPS

    # define beam length
    if x < -beam_length/2:
        x = -beam_length/2
        v = 0
        a = 0
        print("bump left")
    elif x > beam_length/2:
        x = beam_length/2
        v = 0
        a = 0
        print("bump right")

    return g, m, x, v, a, ang


def PID_adj(kp, ki, kd, x, goal, previous_err, integral):

    # define P
    err = x - goal
    p = err

    d = (err - previous_err) / (1/FPS)

    integral = integral + (err * (1/FPS))

    i = integral

    ang_set = kp * p + kd * d + ki * i

    previous_err = err

    return ang_set, previous_err, integral


def ball_pos(x, ang):

    if ang != 0:
        ball_x = (x/beam_length) * math.cos(ang) * 400 + SCREEN_WIDTH/2
        ball_y = - (x/beam_length) * math.sin(ang) * 400 + SCREEN_HEIGHT/2
    else:
        ball_x = x * 200 + SCREEN_WIDTH/2
        ball_y = SCREEN_HEIGHT/2

    ball_x -= 64/2 * math.sin(ang)
    ball_y -= 64/2 * math.cos(ang)

    return ball_x, ball_y


def beam_pos(ang):

    draw_beam_length = 200
    beam_start_x = SCREEN_WIDTH/2 - draw_beam_length*math.cos(-ang)
    beam_start_y = SCREEN_HEIGHT/2 - draw_beam_length*math.sin(-ang)
    beam_end_x = SCREEN_WIDTH/2 + draw_beam_length*math.cos(-ang)
    beam_end_y = SCREEN_HEIGHT/2 + draw_beam_length*math.sin(-ang)

    beam_start = (beam_start_x, beam_start_y)
    beam_end = (beam_end_x, beam_end_y)

    return beam_start, beam_end

# return 1 if sign is flipped between two elements


def flipped_sign(a, b):
    if ((a == b) & (a == 0)) | (a*b > 0):
        return 0
    return 1


def within_percent(a, b, percent):
    if a != 0 and b != 0:
        if abs(a / b) < percent and abs(a / b) > (1/percent):
            print("same")
            return 1

    return 0


if __name__ == "__main__":
    main()
