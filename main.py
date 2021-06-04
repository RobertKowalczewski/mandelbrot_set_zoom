from mandelbrot import make_array_cuda
from variables import *
from dataclasses import dataclass
from pygame import gfxdraw
from PIL import Image


@dataclass()
class Mandel:
    min_x: float
    max_x: float
    min_y: float
    max_y: float
    iterations: float


def draw_image(img: Image.Image):
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            c = img.getpixel((x, y))
            gfxdraw.pixel(s, x, y, (c, c, c))


mandel = Mandel(-2, 2, -2 * aspect_ratio, 2 * aspect_ratio, iterations)
a = make_array_cuda(mandel.min_x, mandel.max_x, mandel.min_y, mandel.max_y, iterations)
# hello test
s.blit(p.surfarray.make_surface(np.array(a.resize(a.size, Image.ANTIALIAS))), (0, 0))
p.display.update()
surf = p.surfarray.make_surface(np.array(a))
p1 = None

running = True
while running:
    for e in p.event.get():
        if e.type == p.QUIT:
            running = False
        elif e.type == p.MOUSEBUTTONDOWN and e.button == p.BUTTON_LEFT:
            p1 = p.mouse.get_pos()
        elif e.type == p.MOUSEBUTTONUP and e.button == p.BUTTON_LEFT:
            m = p.mouse.get_pos()
            p2 = (m[0], m[1])

            d_x = abs(mandel.max_x - mandel.min_x)
            mandel.min_x += d_x * p1[0] / resolution[0]
            mandel.max_x -= d_x * (1 - p2[0] / resolution[0])
            d_y = abs(mandel.max_y - mandel.min_y)
            mandel.min_y += d_y * p1[1] / resolution[1]
            mandel.max_y -= d_y * (1 - p2[1] / resolution[1])

            a = make_array_cuda(mandel.min_x, mandel.max_x, mandel.min_y, mandel.max_y, iterations)
            surf = p.surfarray.make_surface(np.array(a))
            s.blit(surf, (0, 0))
            p.display.update()

            p1 = None
            p2 = None

        elif e.type == p.KEYDOWN:
            if e.key == p.K_SPACE:
                mandel = Mandel(-2, 2, -2, 2, iterations)
                a = make_array_cuda(mandel.min_x, mandel.max_x, mandel.min_y, mandel.max_y, iterations)
                surf = p.surfarray.make_surface(np.array(a)), (0, 0)
                s.blit(surf, (0, 0))
                p.display.update()
            if e.key == p.K_ESCAPE:
                running = False

    if p1 is not None:
        s.blit(surf, (0, 0))

        m = p.mouse.get_pos()
        p.draw.rect(s, (255, 0, 0), (p1[0], p1[1], m[0] - p1[0], (m[0] - p1[0]) * aspect_ratio), 1)
        p.display.update()
        p.mouse.set_pos((m[0], p1[1] + (m[0] - p1[0]) * aspect_ratio))
