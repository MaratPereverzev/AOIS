from typing import List
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

def get_truth_table(table, results: List[int]):
    for i in range(len(results)):
        table[i+1][-1] = results[i]
        
    return table
        
truth_table = [
    ["A", "B", "C", "D", "R"],
    [0, 0, 0, 0, 1],
    [0, 0, 0, 1, 1],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 1, 0],
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 1, 1, 0, 1],
    [0, 1, 1, 1, 1],
    [1, 0, 0, 0, 0],
    [1, 0, 0, 1, 0],
    [1, 0, 1, 0, 1],
    [1, 0, 1, 1, 1],
    [1, 1, 0, 0, 0],
    [1, 1, 0, 1, 0],
    [1, 1, 1, 0, 0],
    [1, 1, 1, 1, 0],
]
        
result_columns = [[0, 0,1,1,0,0,0,0,0,0,0,0,1,1,0,0], 
                  [1,1,0,0,0,0,0,0,1,1,1,1,0,0,0,0], 
                  [1,1,0,0,0,0,1,1,0,0,1,1,0,0,0,0],
                  [0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1]]


for i in range(len(result_columns)):
    iteration_truth_table = get_truth_table(truth_table, result_columns[i])
    bit_sdnf = LogicExpressionExtended.dnfWithCarno(get_sknf_expression(iteration_truth_table))
    print(f"Логическое выражение СДНФ для {i+1}-го бита: {bit_sdnf}")
