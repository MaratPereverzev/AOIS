import unittest
from Logic import LogicExpression

class TestLogicExpression(unittest.TestCase):

    def test_toPolishNotation(self):
        # Тест преобразования в польскую нотацию
        self.assertEqual(LogicExpression.toPolishNotation("A & B"), "A B &")
        self.assertEqual(LogicExpression.toPolishNotation("A | B"), "A B |")
        self.assertEqual(LogicExpression.toPolishNotation("!A"), "A !")
        self.assertEqual(LogicExpression.toPolishNotation("(A | B) & C"), "A B | C &")
        self.assertEqual(LogicExpression.toPolishNotation("A -> B"), "A B @")
        self.assertEqual(LogicExpression.toPolishNotation("A ~ B"), "A B ~")

        # Тест на некорректные операторы
        with self.assertRaises(SyntaxError):
            LogicExpression.toPolishNotation("A ^ B")

        # Тест на лишние скобки
        with self.assertRaises(SyntaxError):
            LogicExpression.toPolishNotation("(A | B")

    def test_result(self):
        # Тест вычисления результата
        self.assertEqual(LogicExpression.result("A & B", 1, 1), 1)
        self.assertEqual(LogicExpression.result("A | B", 0, 1), 1)
        self.assertEqual(LogicExpression.result("!A", 1), 0)
        self.assertEqual(LogicExpression.result("A -> B", 1, 0), 0)
        self.assertEqual(LogicExpression.result("A ~ B", 1, 1), 1)

        # Тест на недостаточное количество значений
        with self.assertRaises(ValueError):
            LogicExpression.result("A & B", "1")

    def test_buildCNF(self):
        # Тест построения КНФ
        self.assertEqual(LogicExpression.buildCNF("A & B"), "(A | B) & (A | !B) & (!A | B)")
        self.assertEqual(LogicExpression.buildCNF("A | B"), "(A | B)")
        self.assertEqual(LogicExpression.buildCNF("!A"), "(!A)")

    def test_buildDNF(self):
        # Тест построения ДНФ
        self.assertEqual(LogicExpression.buildDNF("A & B"), "(A & B)")
        self.assertEqual(LogicExpression.buildDNF("A | B"), "(!A & B) | (A & !B) | (A & B)")
        self.assertEqual(LogicExpression.buildDNF("!A"), "(!A)")

    def test_getForms(self):
        # Тест получения индексной и числовой форм
        result = LogicExpression.getForms("A & B")
        self.assertEqual(result["indexForm"], 1)
        self.assertEqual(result["numberForm"]["conj"], "(3) &")
        self.assertEqual(result["numberForm"]["disj"], "(0, 1, 2) |")

    def test_printTruthTable(self):
        # Тест вывода таблицы истинности
        # Этот тест проверяет, что метод выполняется без ошибок
        # Для проверки вывода можно использовать перенаправление stdout
        import io
        import sys

        captured_output = io.StringIO()
        sys.stdout = captured_output
        LogicExpression.printTruthTable("A & B")
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue()
        self.assertIn("A | B | A & B\n-------------\n0 | 0 | 0    \n0 | 1 | 0    \n1 | 0 | 0    \n1 | 1 | 1    \n", output)
        self.assertIn("0 | 0 | 0", output)
        self.assertIn("1 | 1 | 1", output)

    def test_getPossibleOperations(self):
        # Тест получения возможных операций
        self.assertEqual(LogicExpression.getPossibleOperations("A & B"), ['A & B'])
        self.assertEqual(LogicExpression.getPossibleOperations("A | B"), ['(A | B)'])
        self.assertEqual(LogicExpression.getPossibleOperations("!A"), ["!A"])

if __name__ == "__main__":
    unittest.main()