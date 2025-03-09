from Lab3.LogicExtended import LogicExpressionExtended

def get_sknf_expression(table):
    variables = table[0][:-1]  # Получаем список переменных (последний элемент - это значение функции)
    expression = []

    for row in table[1:]:
        if not row[-1]:  # Если значение функции равно False
            terms = []
            for i, value in enumerate(row[:-1]):
                if value:
                    terms.append(f"!{variables[i]}")  # Отрицание, если значение 1
                else:
                    terms.append(variables[i])  # Без отрицания, если значение 0
            expression.append(" | ".join(terms))

    return " & ".join(f"({term})" for term in expression)

# Пример таблицы истинности
# Переменные: A, B
# Значения функции: F(A, B)
truth_table = [
    ["A", "B", "C", "D", "R"],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 1, 1],
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 1],
    [0, 1, 1, 0, 0],
    [0, 1, 1, 1, 1],
    [1, 0, 0, 0, 0],
    [1, 0, 0, 1, 1],
    [1, 0, 1, 0, 0],
    [1, 0, 1, 1, 1],
    [1, 1, 0, 0, 0],
    [1, 1, 0, 1, 1],
    [1, 1, 1, 0, 0],
    [1, 1, 1, 1, 1],
]

sknf_expression = LogicExpressionExtended.cnfWithQuine(get_sknf_expression(truth_table), isAlradyKNF=True)
print(f"Логическое выражение в СКНФ: {sknf_expression}")

'''
    ["x1", "x2", "x3", "x4", "y1", "y2", "y3", "y4"],
    [0, 0, 0, 0, 0, 1, 1, 0],
    [0, 0, 0, 1, 0, 1, 1, 1],
    [0, 0, 1, 0, 1, 0, 0, 0],
    [0, 0, 1, 1, 1, 0, 0, 1],
    [0, 1, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 0, 0, 0, 1],
    [0, 1, 1, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 0, 0, 1, 1],
    [1, 0, 0, 0, 0, 1, 0, 0],
    [1, 0, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 1, 1, 0],
    [1, 0, 1, 1, 0, 1, 1, 1],
    [1, 1, 0, 0, 1, 0, 0, 0],
    [1, 1, 0, 1, 1, 0, 0, 1],
    [1, 1, 1, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 0, 0, 0, 1],
'''