import unittest
from Binary import Binary

class TestIEEE754Binary(unittest.TestCase):
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