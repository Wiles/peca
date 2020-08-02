from PIL import Image, ImageDraw
from typing import List
from math import ceil
from os import linesep
import random

black = (0x00, 0x00, 0x00, 0xff)
white = (0xff, 0xff, 0xff, 0xff)
transparent = (0xff, 0xff, 0xff, 0x00)


def generate_rule(n):
    def rule(a, b, c):
        next = None
        if [a, b, c] == ["1", "1", "1"]:
            next = n >> 7 & 1
        if [a, b, c] == ["1", "1", "0"]:
            next = n >> 6 & 1
        if [a, b, c] == ["1", "0", "1"]:
            next = n >> 5 & 1
        if [a, b, c] == ["1", "0", "0"]:
            next = n >> 4 & 1
        if [a, b, c] == ["0", "1", "1"]:
            next = n >> 3 & 1
        if [a, b, c] == ["0", "1", "0"]:
            next = n >> 2 & 1
        if [a, b, c] == ["0", "0", "1"]:
            next = n >> 1 & 1
        if [a, b, c] == ["0", "0", "0"]:
            next = n & 1

        return str(next)

    return rule


def generate_seed(cell_count: int):
    seed = ""
    for x in range(0, ceil(cell_count / 4)):
        seed += random.choice("0123456789ABCDEF")

    return seed


def initiate_life(cell_count: int, seed: str):
    row = bin(int(seed, 16))[2:].zfill(len(seed) * 4)

    row = row[:cell_count]

    row = row.ljust(cell_count, "0")
    return row


def iterate_life(cells: List[float], rule):
    next_gen = ""
    for x in range(0, len(cells)):
        a = cells[x-1]
        b = cells[x]
        if (x + 1 == len(cells)):
            c = cells[0]
        else:
            c = cells[x + 1]
        next_gen += rule(a, b, c)
    return next_gen


def generate_image(matrix, size: int, is_transparent: bool):

    width = len(matrix[0])
    height = len(matrix)
    canvas_width = width * size
    canvas_height = height * size

    foreground = black
    background = white

    if is_transparent:
        background = transparent

    img = Image.new('RGBA', (canvas_width, canvas_height), background)

    draw = ImageDraw.Draw(img)

    for x in range(0, width):
        for y in range(0, height):
            if matrix[y][x] == "1":

                pos_x = x * size
                pos_y = y * size
                location = (pos_x, pos_y, pos_x + size - 1, pos_y + size - 1)

                draw.rectangle(location, fill=foreground)

    return img


def generate_unicode(matrix):
    
    lines = []
    
    count = len(matrix)

    if count % 2 == 1:
        count += 1

    for x in range(0, count, 2):
        top = matrix[x]
        if (x + 1) >= len(matrix):
            bottom = "".rjust(len(top), "0")
        else:
            bottom = matrix[x + 1]

        line = "".join([" ▄▀█"[int(a + b, 2)] for a, b in zip(top, bottom)])
        lines.append("".join(line))

    return linesep.join(lines)


def elementary_cellular_automaton(width: int, height: int, rule: callable, seed: str):
    matrix = []
    first_gen = initiate_life(width, seed)
    matrix.append(first_gen)
    for x in range(0, height - 1):
        next_gen = iterate_life(matrix[-1], rule)
        matrix.append(next_gen)

    return matrix
