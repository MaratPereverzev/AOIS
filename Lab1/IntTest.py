import unittest
from Binary import Binary

class TestIntBinary(unittest.TestCase):
    def test_intToBinary(self):
        self.assertEqual(Binary.intToBinary(5), "00000101")
        self.assertEqual(Binary.intToBinary(-5), "10000101")
        self.assertEqual(Binary.intToBinary(0), "00000000")
        self.assertEqual(Binary.intToBinary(127), "01111111")
        self.assertEqual(Binary.intToBinary(-128), "110000000")

    def test_toBinaryForward(self):
        self.assertEqual(Binary.toBinaryForward(5), "00000101")
        self.assertEqual(Binary.toBinaryForward(-5), "10000101")
        self.assertEqual(Binary.toBinaryForward("101"), "00000101")

    def test_toBinaryReverse(self):
        self.assertEqual(Binary.toBinaryReverse(5), "00000101")
        self.assertEqual(Binary.toBinaryReverse(-5), "11111010")

    def test_toBinaryComplement(self):
        self.assertEqual(Binary.toBinaryComplement(5), "00000101")
        self.assertEqual(Binary.toBinaryComplement(-5), "11111011")

    def test_binaryToInt(self):
        self.assertEqual(Binary.binaryToInt("00000101"), 5)
        self.assertEqual(Binary.binaryToInt("10000101"), -5)
        self.assertEqual(Binary.binaryToInt("00000000"), 0)

    def test_sum(self):
        self.assertEqual(Binary.sum(4, -5), "11111111")
        self.assertEqual(Binary.sum("00000100", "11111011", signed=False), "11111111")
        self.assertEqual(Binary.sum(10, 20), "00011110")

    def test_subtract(self):
        self.assertEqual(Binary.subtract(10, 5), "00000101")
        self.assertEqual(Binary.subtract(5, 10), "11111011")
        self.assertEqual(Binary.subtract("00001010", "00000101"), "00000101")

    def test_multiply(self):
        self.assertEqual(Binary.multiply(5, 3), "00001111")
        self.assertEqual(Binary.multiply(-5, 3), "10001111")
        self.assertEqual(Binary.multiply("00000101", "00000011"), "00001111")

    def test_divide(self):
        self.assertEqual(Binary.divide(10, 2), "00000101.00000000000000000000")
        self.assertEqual(Binary.divide(10, 3), "00000011.01010101010101010101")
        self.assertEqual(Binary.divide(-10, 2), "00000101.00000000000000000000")

    def test_binaryToDecimal(self):
        self.assertEqual(Binary.binaryToDecimal("101.101"), 5.625)
        self.assertEqual(Binary.binaryToDecimal("0.1"), 0.5)
        self.assertEqual(Binary.binaryToDecimal("1.1"), 1.5)

    def test_toIEEE754(self):
        self.assertEqual(Binary.toIEEE754(13.625), "01000001010110100000000000000000")
        self.assertEqual(Binary.toIEEE754(-13.625), "11000001010110100000000000000000")
        self.assertEqual(Binary.toIEEE754(0), "00000000000000000000000000000000")

    def test_IEEE754toDecimal(self):
        self.assertEqual(Binary.IEEEtoDecimal("01000001010110100000000000000000"), 13.625)
        self.assertEqual(Binary.IEEEtoDecimal("11000001010110100000000000000000"), -13.625)
        self.assertEqual(Binary.IEEEtoDecimal("00000000000000000000000000000000"), 0.0)

    def test_sumIEEE754(self):
        self.assertEqual(Binary.sumIEEE754(13.625, 5.25), "01000001100101110000000000000000")
        self.assertEqual(Binary.sumIEEE754("01000001010110100000000000000000", "01000000101010000000000000000000"), "01000001100101110000000000000000")

if __name__ == "__main__":
    unittest.main()