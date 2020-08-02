from PIL import Image, ImageDraw
from typing import List
from math import ceil
from os import linesep
import random
import argparse

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
    output = ""
    for x in range(0, ceil(len(matrix) / 2)):
        top = matrix[x * 2]
        if ((x * 2) + 1) >= len(matrix):
            bottom = "".rjust(len(top), "0")
        else:
            bottom = matrix[((x * 2) + 1)]

        line = ""
        for a, b in zip(top, bottom):
            if a == "1" and b == "1":
                line += "█"
            elif a == "1" and b == "0":
                line += "▀"
            elif a == "0" and b == "1":
                line += "▄"
            else:
                line += " "

        output += line + linesep

    return output


def elementary_cellular_automaton(width: int, height: int, rule: callable, seed: str):
    matrix = []
    first_gen = initiate_life(width, seed)
    matrix.append(first_gen)
    for x in range(0, height - 1):
        next_gen = iterate_life(matrix[-1], rule)
        matrix.append(next_gen)

    return matrix


def handle_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--width", "-w", help="set output width", type=int, required=True)
    parser.add_argument(
        "--length", "-l", help="set output height", type=int, required=True)
    parser.add_argument("--cell-size", "-c",
                        help="set cell size", type=int, required=True)
    parser.add_argument(
        "--rule", "-r", help="rule number for eca", type=int, default=110)
    parser.add_argument(
        "--algorithm", "-a", help="algorithm for image generation", type=str, default="eca")
    parser.add_argument(
        "--output", "-o", help="output filename", type=str)
    parser.add_argument("--transparent", "-t",
                        help="output transparent background", action="store_true")
    parser.add_argument(
        "--seed", "-s", help="hexadecimal seed used to initiate life instead of randomness", type=str)

    return parser.parse_args()


if __name__ == "__main__":
    args = handle_args()

    cell_size = args.cell_size
    width = args.width
    height = args.length
    rule = generate_rule(args.rule)
    algo = args.algorithm
    is_transparent = args.transparent
    filename = args.output
    seed = args.seed

    matrix = None

    if not seed:
        seed = generate_seed(width)

        print("Seed:", seed)

    if algo == "eca":
        matrix = elementary_cellular_automaton(width, height, rule, seed)
    else:
        raise Exception("unknown algorithm")

    if filename:
        image = generate_image(matrix, cell_size, is_transparent)
        image.save(filename, 'png')
    else:
        unicode = generate_unicode(matrix)
        print(unicode)
