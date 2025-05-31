import unittest
from DiagonalMatrix import DiagonalMatrix


class TestDiagonalMatrix(unittest.TestCase):

    def setUp(self):
        self.matrix = [[0 for _ in range(DiagonalMatrix.SIZE)] for _ in range(DiagonalMatrix.SIZE)]
        for i in range(DiagonalMatrix.SIZE):
            self.matrix[i][i] = 1
        self.dm = DiagonalMatrix(self.matrix)

    def test_get_word(self):
        word = self.dm.get_word(0)
        expected = [1 if i == i else 0 for i in range(DiagonalMatrix.SIZE)]
        self.assertEqual(word, expected)

    def test_get_column(self):
        column = self.dm.get_column(1)
        expected = [0] * DiagonalMatrix.SIZE
        expected[1] = 1
        self.assertEqual(column, expected)

    def test_logical_f1(self):
        w1 = [1, 0, 1, 1]
        w2 = [1, 1, 0, 1]
        self.assertEqual(self.dm.logical_f1(w1, w2), [1, 0, 0, 1])

    def test_logical_f3(self):
        w1 = [1, 0, 1, 1]
        w2 = [1, 1, 0, 1]
        self.assertEqual(self.dm.logical_f3(w1, w2), [0, 1, 1, 0])

    def test_logical_f12(self):
        w1 = [1, 0, 1, 1]
        w2 = [1, 1, 0, 1]
        self.assertEqual(self.dm.logical_f12(w1, w2), [0, 1, 0, 0])

    def test_logical_f14(self):
        w1 = [1, 0, 1, 0]
        self.assertEqual(self.dm.logical_f14(w1, w1), [0, 1, 0, 1])

    def test_add_fields(self):
        test_word = [1, 1, 1] + [1, 1, 0, 0] + [0, 0, 1, 1] + [0] * 5
        self.dm.write_word(0, test_word)
        self.dm.add_fields("111")
        word = self.dm.get_word(0)
        self.assertEqual(word[11:16], [0, 1, 1, 1, 1])  # 12+3 = 15 → 01111

    def test_find_nearest_up_down(self):
        target = [0] * DiagonalMatrix.SIZE
        target[0] = 1
        up = self.dm.find_nearest_up(target)
        down = self.dm.find_nearest_down(target)
        self.assertTrue(up == -1 or 0 <= up < DiagonalMatrix.SIZE)
        self.assertTrue(down == -1 or 0 <= down < DiagonalMatrix.SIZE)


if __name__ == '__main__':
    unittest.main()
