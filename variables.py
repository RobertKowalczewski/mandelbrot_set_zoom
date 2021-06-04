import pygame as p
import numpy as np

while i := input('fullscreen: (Yes/No)'):
    if i == 'Yes' or i == 'No':
        break
if i == 'Yes':
    resolution = (1920, 1080)
    s = p.display.set_mode(resolution, p.FULLSCREEN)
else:
    x = int(input('res_x: (number)'))
    y = int(input('res_y: (number)'))
    resolution = (x, y)
    s = p.display.set_mode(resolution)

p.init()
v = p.math.Vector2

aspect_ratio = resolution[1] / resolution[0]
iterations = 1000
