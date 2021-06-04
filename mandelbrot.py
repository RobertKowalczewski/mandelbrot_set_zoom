from PIL import Image
from numba import jit, cuda
from variables import *


@jit(nopython=True)
def compute_coordinates(x: float, y: float, iterations: int) -> float:
    c = complex(x, y)
    z = 0.0j
    for i in range(iterations):
        z = z * z + c
        if (z.real * z.real + z.imag * z.imag) >= 4:
            return i
    return 255


@jit(nopython=True)
def mandel(res, min_x, max_x, min_y, max_y, iterations):
    image = np.zeros(res, dtype=np.int8)
    pixel_size_x = (max_x - min_x) / resolution[0]
    pixel_size_y = (max_y - min_y) / resolution[1]
    for y in range(res[0]):
        imaginary = min_y + y * pixel_size_y
        for x in range(res[1]):
            real = min_x + x * pixel_size_x
            image[x, y] = int(compute_coordinates(real, imaginary, iterations))
    return image


@cuda.jit
def mandel(min_x, min_y, iterations, pixel_size_x, pixel_size_y, out):
    x, y = cuda.grid(2)
    c = complex(min_x + x * pixel_size_x, min_y + y * pixel_size_y)
    z = 0.0j
    out[x, y] = 255
    for i in range(iterations):
        z = z * z + c
        if (z.real * z.real + z.imag * z.imag) >= 4:
            out[x, y] = i
            break

# chnage 2
def make_array_cuda(x_min, x_max, y_min, y_max, iterations):
    out = np.zeros(resolution, dtype=np.int8)
    pixel_size_x = (x_max - x_min) / resolution[0]
    pixel_size_y = (y_max - y_min) / resolution[1]
    mandel[(resolution[0] // 10, resolution[1] // 10), (10, 10)](x_min, y_min, iterations, pixel_size_x, pixel_size_y,
                                                                 out)
    return Image.fromarray(out)
