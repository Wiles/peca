import unittest
from peca import generate_unicode, generate_seed, initiate_life, generate_rule, iterate_life, elementary_cellular_automaton
from os import linesep


class Tests(unittest.TestCase):

    def test_block_generation(self):
        expected = """ ▄▀█"""

        input = ["0011", "0101"]

        actual = generate_unicode(input)

        self.assertEqual(expected, actual)

    def test_block_generation_odd_lines(self):
        expected = """ ▄▀█""" + linesep + "▀ ▀ "

        input = ["0011", "0101", "1010"]

        actual = generate_unicode(input)

        self.assertEqual(expected, actual)

    def test_seed_generation(self):
        expected = 4

        input = 16

        actual = len(generate_seed(input))

        self.assertEqual(expected, actual)

    def test_seed_generation_undersized(self):
        expected = 4

        input = 13

        actual = len(generate_seed(input))

        self.assertEqual(expected, actual)

    def test_initiate_life(self):
        expected = "10101000"

        seed = "A8"

        actual = initiate_life(len(seed) * 4, seed)

        self.assertEqual(expected, actual)

    def test_initiate_life_truncate(self):
        expected = "101010"

        seed = "A8"

        actual = initiate_life(len(seed) * 4 - 2, seed)

        self.assertEqual(expected, actual)

    def test_initiate_life_pad(self):
        expected = "1010100000"

        seed = "A8"

        actual = initiate_life(len(seed) * 4 + 2, seed)

        self.assertEqual(expected, actual)

    def test_generate_rule_90(self):

        rule = generate_rule(90)

        self.assertEqual(rule("0", "0", "0",), "0")
        self.assertEqual(rule("0", "0", "1",), "1")
        self.assertEqual(rule("0", "1", "0",), "0")
        self.assertEqual(rule("0", "1", "1",), "1")
        self.assertEqual(rule("1", "0", "0",), "1")
        self.assertEqual(rule("1", "0", "1",), "0")
        self.assertEqual(rule("1", "1", "0",), "1")
        self.assertEqual(rule("1", "1", "1",), "0")

    def test_generate_rule_110(self):

        rule = generate_rule(110)

        self.assertEqual(rule("0", "0", "0",), "0")
        self.assertEqual(rule("0", "0", "1",), "1")
        self.assertEqual(rule("0", "1", "0",), "1")
        self.assertEqual(rule("0", "1", "1",), "1")
        self.assertEqual(rule("1", "0", "0",), "0")
        self.assertEqual(rule("1", "0", "1",), "1")
        self.assertEqual(rule("1", "1", "0",), "1")
        self.assertEqual(rule("1", "1", "1",), "0")

    def test_iterate_life(self):
        rule = generate_rule(90)

        expected = "01000001"

        input = "00101010"

        actual = iterate_life(input, rule)

        self.assertEqual(expected, actual)

    def test_eca_sierpinski(self):
        rule = generate_rule(90)

        input = "01"

        actual = elementary_cellular_automaton(15, 8, rule, input)

        expected = [
            "000000010000000",
            "000000101000000",
            "000001000100000",
            "000010101010000",
            "000100000001000",
            "001010000010100",
            "010001000100010",
            "101010101010101",
        ]

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
