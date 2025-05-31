import unittest
from Lab3.LogicExtended import LogicExpressionExtended  # Замените 'your_module' на имя вашего модуля

class TestLogicExpressionExtended(unittest.TestCase):

    def test_cnfWithQuine(self):
        # Тест для метода cnfWithQuine
        exp = "(A | B) & C"
        expected_result = "(A | B) & C".split(" & ")
        expected_result.sort()  # Ожидаемый результат может отличаться в зависимости от реализации
        result = LogicExpressionExtended.cnfWithQuine(exp).split(" & ")
        result.sort()
        self.assertEqual(result, expected_result)

    def test_dnfWithQuine(self):
        # Тест для метода dnfWithQuine
        exp = "(A | B) & C"
        expected_result = "A & C | B & C".split(" | ")
        expected_result.sort()  # Ожидаемый результат может отличаться в зависимости от реализации
        result = LogicExpressionExtended.dnfWithQuine(exp).split(" | ")
        result.sort()
        self.assertListEqual(result, expected_result)

    def test_cnfWithCarno(self):
        # Тест для метода cnfWithCarno
        exp = "(A | B) & C"
        expected_result = "(A | B) & C".split(" & ")
        expected_result.sort()  # Ожидаемый результат может отличаться в зависимости от реализации
        result = LogicExpressionExtended.cnfWithCarno(exp).split(" & ")
        result.sort()
        self.assertListEqual(result, expected_result)

    def test_dnfWithCarno(self):
        # Тест для метода dnfWithCarno
        exp = "(A | B) & C"
        expected_result = "A & C | B & C".split(" | ")
        expected_result.sort()  # Ожидаемый результат может отличаться в зависимости от реализации
        result = LogicExpressionExtended.dnfWithCarno(exp).split(" | ")
        result.sort()
        self.assertEqual(result, expected_result)

    def test_isBondable(self):
        # Тест для метода _isBondable
        self.assertTrue(LogicExpressionExtended._isBondable("A | B", "A | !B", True))
        self.assertFalse(LogicExpressionExtended._isBondable("A | B", "A | B", True))

    def test_getSimilarVariables(self):
        # Тест для метода _getSimilarVariables
        similar_vars = LogicExpressionExtended._getSimilarVariables("A | B", "A | !B", True)
        self.assertEqual(similar_vars, ["A"])

    def test_removeSimilarConstituents(self):
        # Тест для метода _removeSimilarConstituents
        constituents = [["A", "B"], ["A", "B"], ["C", "D"]]
        unique_constituents = LogicExpressionExtended._removeSimilarConstituents(constituents)
        self.assertEqual(unique_constituents, [["A", "B"], ["C", "D"]])

    def test_calculateExpBoost(self):
        # Тест для метода calculateExpBoost
        polish_notation = "0 1 &"
        result = LogicExpressionExtended.calculateExpBoost(polish_notation)
        self.assertEqual(result, 0)

if __name__ == '__main__':
    unittest.main()