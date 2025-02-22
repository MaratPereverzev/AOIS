import unittest
from Binary import Binary

class TestFloatBinary(unittest.TestCase):
  def test_divide(self):
    self.assertEqual(Binary.divide(10, 2), "00000101.00000000000000000000")
    self.assertEqual(Binary.divide(10, 3), "00000011.01010101010101010101")
    self.assertEqual(Binary.divide(-10, 2), "00000101.00000000000000000000")

  def test_binaryToDecimal(self):
      self.assertEqual(Binary.binaryToDecimal("101.101"), 5.625)
      self.assertEqual(Binary.binaryToDecimal("0.1"), 0.5)
      self.assertEqual(Binary.binaryToDecimal("1.1"), 1.5)
      
if __name__ == "__main__":
    unittest.main()