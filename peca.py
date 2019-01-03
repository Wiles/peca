from PIL import Image, ImageDraw
from typing import List
import random


def rule_60(a, b, c):
	if [a, b, c] == [1, 1, 1]:
		return 0
	if [a, b, c] == [1, 1, 0]:
		return 0
	if [a, b, c] == [1, 0, 1]:
		return 1
	if [a, b, c] == [1, 0, 0]:
		return 1
	if [a, b, c] == [0, 1, 1]:
		return 1
	if [a, b, c] == [0, 1, 0]:
		return 1
	if [a, b, c] == [0, 0, 1]:
		return 0
	if [a, b, c] == [0, 0, 0]:
		return 0


def rule_45(a, b, c):
	if [a, b, c] == [1, 1, 1]:
		return 0
	if [a, b, c] == [1, 1, 0]:
		return 0
	if [a, b, c] == [1, 0, 1]:
		return 1
	if [a, b, c] == [1, 0, 0]:
		return 0
	if [a, b, c] == [0, 1, 1]:
		return 1
	if [a, b, c] == [0, 1, 0]:
		return 1
	if [a, b, c] == [0, 0, 1]:
		return 0
	if [a, b, c] == [0, 0, 0]:
		return 1


def initiate_life(cell_count: int):
	row = []
	for x in range(0, cell_count):
		row.append(random.choice([1, 0]))
	return row


def iterate_life(cells:List[float], rule):
	next_gen = []
	for x in range(0, len(cells)):
		a = cells[x-1]
		b = cells[x]
		if (x + 1 == len(cells)):
			c = cells[-1]
		else:
			c = cells[x + 1]
		next_gen.append(rule(a, b, c))
	return next_gen


def generate_image(matrix, width: int, height: int, size: int):
	canvas_width = width * size
	canvas_height = height * size
	img = Image.new('RGB', (canvas_width, canvas_height), (255, 0, 0, 0))

	draw = ImageDraw.Draw(img)

	for x in range(0, width):
		for y in range(0, height):
			color = (0xff, 0xff, 0xff)
			if matrix[y][x] == 1:
				color = (0x00, 0x00, 0x00)

			pos_x = x * size
			pos_y = y * size
			location = (pos_x, pos_y, pos_x + size, pos_y + size)

			draw.rectangle(location, fill=color)

	img.save('test.jpg', 'JPEG')

if __name__ == "__main__":
	cell_size = 20
	cell_count = int(2900 / cell_size)
	iterations = int(4060 / cell_size) - 1
	matrix = []
	first_gen = initiate_life(cell_count)
	print(first_gen)
	matrix.append(first_gen)
	for x in range(0, iterations):
		matrix.append(iterate_life(matrix[-1], rule_60))

	generate_image(matrix, len(first_gen), len(matrix), cell_size)