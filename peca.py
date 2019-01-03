from PIL import Image, ImageDraw

def generate_image():
	img = Image.new('RGBA', (2900, 4060), (255, 0, 0, 0))

	draw = ImageDraw.Draw(img)
	draw.rectangle((0, 0, 20, 20), fill=(255, 0, 0))

	color = 255
	for x in range(0, 2900, 20):
		for y in range(0, 4060, 20):
			draw.rectangle((x, y, x + 20, y + 20), fill=(color, color, color))
			if color == 255:
				color = 0
			else:
				color = 255


	img.save('test.png', 'PNG')

if __name__ == "__main__":
	generate_image()