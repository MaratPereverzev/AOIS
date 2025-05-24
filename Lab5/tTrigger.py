from typing import List
from Lab3.LogicExtended import LogicExpressionExtended

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

def get_truth_table(table, results: List[int]):
    for i in range(len(results)):
        table[i+1][-1] = results[i]
        
    return table
        
# Таблица истинности
truth_table = [
    ["A", "B", "C", "D", "R"],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 1, 0],
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 1, 1, 0, 0],
    [0, 1, 1, 1, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 0, 1, 1],
    [1, 0, 1, 0, 1],
    [1, 0, 1, 1, 1],
    [1, 1, 0, 0, 1],
    [1, 1, 0, 1, 1],
    [1, 1, 1, 0, 1],
    [1, 1, 1, 1, 0]
]

result_columns = [[0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0], 
                  [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0], 
                  [0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0],
                  [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
]

for i in range(len(result_columns)):
    iteration_truth_table = get_truth_table(truth_table, result_columns[i])
    bit_sdnf = LogicExpressionExtended.dnfWithCarno(get_sdnf_expression(iteration_truth_table))
    #print(get_sdnf_expression(iteration_truth_table))
    print(f"Логическое выражение СДНФ для {i+1}-го бита: {bit_sdnf}")