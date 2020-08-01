from PIL import Image, ImageDraw
from typing import List
import random
import argparse

black = (0x00, 0x00, 0x00, 0xff)
white = (0xff, 0xff, 0xff, 0xff)
transparent = (0xff, 0xff, 0xff, 0x00)

def generate_rule(n):
    def rule(a, b, c):
        if [a, b, c] == [1, 1, 1]:
            return n >> 7 & 1
        if [a, b, c] == [1, 1, 0]:
            return n >> 6 & 1
        if [a, b, c] == [1, 0, 1]:
            return n >> 5 & 1
        if [a, b, c] == [1, 0, 0]:
            return n >> 4 & 1
        if [a, b, c] == [0, 1, 1]:
            return n >> 3 & 1
        if [a, b, c] == [0, 1, 0]:
            return n >> 2 & 1
        if [a, b, c] == [0, 0, 1]:
            return n >> 1 & 1
        if [a, b, c] == [0, 0, 0]:
            return n & 1

    return rule


def initiate_life(cell_count: int):
    row = []
    for x in range(0, cell_count):
        row.append(random.choice([1, 0]))
    return row


def iterate_life(cells: List[float], rule):
    next_gen = []
    for x in range(0, len(cells)):
        a = cells[x-1]
        b = cells[x]
        if (x + 1 == len(cells)):
            c = cells[0]
        else:
            c = cells[x + 1]
        next_gen.append(rule(a, b, c))
    return next_gen


def generate_image(matrix, width: int, height: int, size: int, is_transparent: bool, filename: str):
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
            if matrix[y][x] == 1:

                pos_x = x * size
                pos_y = y * size
                location = (pos_x, pos_y, pos_x + size - 1, pos_y + size - 1)

                draw.rectangle(location, fill=foreground)

    img.save(filename, 'png')


def elementary_cellular_automaton(width: int, height: int, rule: callable):
    matrix = []
    first_gen = initiate_life(width)
    matrix.append(first_gen)
    for x in range(0, height - 1):
        matrix.append(iterate_life(matrix[-1], rule))

    return matrix


def handle_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--width", "-w", help="set output width", type=int, required=True)
    parser.add_argument("--length", "-l", help="set output height", type=int, required=True)
    parser.add_argument("--cell-size", "-c", help="set cell size", type=int, required=True)
    parser.add_argument("--rule", "-r", help="rule number for eca", type=int, default=110)
    parser.add_argument("--algorithm", "-a", help="algorithm for image generation", type=str, default="eca")
    parser.add_argument("--output", "-o", help="output filename", type=str, default="out.png")
    parser.add_argument("--transparent", "-t", help="output transparent background", action="store_true")

    return parser.parse_args()


if __name__ == "__main__":
    args = handle_args()

    cell_size = args.cell_size
    width = args.width
    height = args.length
    rule = generate_rule(args.rule)
    algo = args.algorithm
    transparent = args.transparent
    filename = args.output

    matrix = None

    if algo == "eca":
        matrix = elementary_cellular_automaton(width, height, rule)
    else:
        raise Exception("unknown algorithm")

    generate_image(matrix, width, height, cell_size, transparent, filename)
