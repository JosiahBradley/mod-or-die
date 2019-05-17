from random import random
import math


def frange(start: float = 0.0, stop: float = 2.0, step: float = 1.0):
    while start < stop:
        yield start
        start += step


def rand_range(start: float = 0.0, stop: float = 2.0, smoothing: int = 3, scale: float=1.0):
    while start < stop:
        yield start
        start += round(random(), smoothing) * scale


def scale_generator(x: float = 0.0, offset: float = 0.5, step: float = 0.00001):
    while True:
        yield abs(math.sin(x)) + offset
        x += step
