import argparse
from peca import generate_seed, elementary_cellular_automaton, generate_image, generate_unicode, generate_rule


def handle_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--width", "-w", help="set output width", type=int, required=True)
    parser.add_argument(
        "--length", "-l", help="set output height", type=int, required=True)
    parser.add_argument("--cell-size", "-c",
                        help="set cell size", type=int, default=1)
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
