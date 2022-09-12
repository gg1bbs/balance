import math
import random
import matplotlib
# import pygame

g = 9.8
m = 10
f = 30
s = 10

def main():
    x = 0
    v = 0
    a = 0
    ang = 0

    simulation(x,v,a,ang)

def simulation(x,v,a,ang):
    second_counter = 0
    tick_counter = 0
    adj = 1.1
    while True:
        if x <= 0:
            ang = ang - adj
        else:
            ang = ang + adj

        a += -1 * ((math.sin(ang) * g) / m) / f
        v += a / f
        x += v / f
        second_counter += 1
        tick_counter += 1
        if x <= -10 or x >= 10:
            break

        if second_counter == f:
            print(x)
            second_counter = 0

if __name__ == "__main__":
    main()