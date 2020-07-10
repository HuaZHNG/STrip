import unittest

from run.Monitor import intersection


class TestIntersection(unittest.TestCase):
    def test_empty(self):
        out = intersection([], [])
        self.assertEqual(out[0], 0)
        self.assertTrue(isinstance(out[1], tuple))
        self.assertEqual(out[1], ())

    def test_case1(self):
        a = [[0, 1], [3, 4], [5, 10], [11, 12]]
        b = [[1, 2], [4, 6], [7, 9], [11, 12]]
        out = intersection(a, b)
        self.assertEqual(out[0], 2)
        self.assertEqual(out[1], (7, 9))


if __name__ == "__main__":
    unittest.main()