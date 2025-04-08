from Lab3.LogicExtended import LogicExpressionExtended

def get_sknf_expression(table):
    variables = table[0][:-1]  # Получаем список переменных
    expression = []

    for row in table[1:]:  # Проходим по строкам таблицы истинности
        if not row[-1]:  # Если результат равен 0 (ложь)
            terms = []
            for i, value in enumerate(row[:-1]):  # Проходим по значениям переменных
                if value:
                    terms.append(f"!{variables[i]}")  # Если значение 1, добавляем инверсию
                else:
                    terms.append(variables[i])  # Если значение 0, добавляем переменную
            expression.append(" | ".join(terms))  # Объединяем термы в дизъюнкцию

    return " & ".join(f"({term})" for term in expression)  # Объединяем дизъюнкции в конъюнкцию

def get_sdnf_expression(table):
    variables = table[0][:-1]  # Получаем список переменных
    expression = []

    for row in table[1:]:  # Проходим по строкам таблицы истинности
        if row[-1]:  # Если результат равен 1 (истина)
            terms = []
            for i, value in enumerate(row[:-1]):  # Проходим по значениям переменных
                if value:
                    terms.append(variables[i])  # Если значение 1, добавляем переменную
                else:
                    terms.append(f"!{variables[i]}")  # Если значение 0, добавляем инверсию
            expression.append(" & ".join(terms))  # Объединяем термы в конъюнкцию

    return " | ".join(f"({term})" for term in expression)  # Объединяем конъюнкции в дизъюнкцию

# Таблица истинности
truth_table = [
    ["A", "B", "C", "D"],
    [0, 0, 0, 0],
    [0, 0, 1, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 1],
    [1, 0, 0, 0],
    [1, 0, 1, 1],
    [1, 1, 0, 1],
    [1, 1, 1, 1],
]

'''
[0, 0, 0, 0, 0],
[0, 0, 1, 1, 0],
[0, 1, 0, 1, 0],
[0, 1, 1, 0, 1],
[1, 0, 0, 1, 0],
[1, 0, 1, 0, 1],
[1, 1, 0, 0, 1],
[1, 1, 1, 1, 1],
'''

# Получаем СКНФ
sknf_expression = get_sknf_expression(truth_table)
print(f"Логическое выражение в СКНФ: {sknf_expression}")

# Получаем СДНФ
sdnf_expression = get_sdnf_expression(truth_table)
print(f"Логическое выражение в СДНФ: {sdnf_expression}")

# Преобразуем СДНФ с использованием метода dnfWithCarno
sdnf_minimized = LogicExpressionExtended.cnfWithCarno(sdnf_expression)
print(f"Минимизированное логическое выражение в СДНФ: {sdnf_minimized}")