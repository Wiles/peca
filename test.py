import unittest
from peca import generate_unicode
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


if __name__ == "__main__":
    unittest.main()
