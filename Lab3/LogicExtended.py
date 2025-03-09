from Lab2.Logic import LogicExpression
from typing import List
from itertools import product

class LogicExpressionExtended (LogicExpression):
  @staticmethod
  def _isBondable(firstConstituent: str, secondConstituent: str, forCNF: bool) -> bool:
    notEqualCount = 0
    hasOpposite = False
    
    firstConstituent = LogicExpressionExtended._parseForCNF(firstConstituent, not forCNF)
    secondConstituent = LogicExpressionExtended._parseForCNF(secondConstituent, not forCNF)
    
    for i in range(min(len(firstConstituent), len(secondConstituent))):
      if firstConstituent[i] == f"!{secondConstituent[i]}" or f"!{firstConstituent[i]}" == secondConstituent[i]:
        hasOpposite = True
        notEqualCount += 1
      elif firstConstituent[i] != secondConstituent[i]:
        notEqualCount += 1
      
    return True if notEqualCount == 1 and hasOpposite == True else False
  
  @staticmethod
  def _getSimilarVariables(firstConstituent: str, secondConstituent: str, forCNF: bool) -> bool:
    similar = []
    
    firstConstituent = LogicExpressionExtended._parseForCNF(firstConstituent, not forCNF)
    secondConstituent = LogicExpressionExtended._parseForCNF(secondConstituent, not forCNF)
    
    for i in range(min(len(firstConstituent), len(secondConstituent))):
      if firstConstituent[i] == secondConstituent[i]:
        similar.append(firstConstituent[i])
    
    return similar
  
  @staticmethod
  def _removeSimilarConstituents(constituents: List[List[str]]):
    result = []
    
    for constituent in constituents:
      if not constituent in result:
        result.append(constituent)
    
    return result   
  
  @staticmethod
  def _parseForCNF(constituent: str, forCNF: bool):    
    return constituent.split(LogicExpressionExtended.AND_SEPARATOR) if forCNF else constituent.split(LogicExpressionExtended.OR_SEPARATOR)
    
  @staticmethod
  def _QuineAlgorithm(constituents: List[List[str]], notFirstIteration: bool, forCNF: bool) -> str:
    nextConstituent = []
    callRecursive = False
    bondableIteration = False
    
    for i in range(len(constituents) - 1):
      bondableIteration = False
      for j in range(len(constituents)):
        if LogicExpressionExtended._isBondable(constituents[i], constituents[j], forCNF):
          bondableIteration = True
          if i < j: 
            callRecursive = True
            nextConstituent.append(f"{LogicExpression.OR_SEPARATOR if forCNF else LogicExpression.AND_SEPARATOR}".join(LogicExpressionExtended._getSimilarVariables(constituents[i], constituents[j], forCNF)))
      if not bondableIteration and notFirstIteration:
        nextConstituent.append(constituents[i])
        
    if not bondableIteration and not callRecursive and notFirstIteration:
      nextConstituent.append(constituents[-1])
    
    if callRecursive: 
      nextConstituent = LogicExpressionExtended._QuineAlgorithm(nextConstituent, True, forCNF)
      
    return nextConstituent
  
  @staticmethod
  def cnfWithQuine(exp: str, variant: str = "расчётный", isAlradyKNF = False) -> str:
    if not isAlradyKNF:
      exp = LogicExpression.buildCNF(exp)
    formulas = exp.replace("(","").replace(")","").split(LogicExpressionExtended.AND_SEPARATOR)
    
    constituents = LogicExpressionExtended._QuineAlgorithm(formulas, False, True)
    constituents = LogicExpressionExtended._removeSimilarConstituents(constituents)
    
    for i in range(len(constituents)):
      if len(constituents[i]) > 1:
        constituents[i] = f"({constituents[i]})"
    
    tempResult = LogicExpressionExtended.AND_SEPARATOR.join(constituents)
    
    constituents = LogicExpressionExtended._withCalculativeTable(formulas, constituents, True) if variant == "таблично-расчётный" else LogicExpressionExtended._withCalculative(constituents, tempResult, True)

    return LogicExpressionExtended.AND_SEPARATOR.join(LogicExpressionExtended._removeSimilarConstituents(constituents)) if len(constituents) else tempResult
  
  @staticmethod
  def dnfWithQuine(exp: str, variant: str = "расчётный") -> str:
    formulas = LogicExpression.buildDNF(exp).replace("(","").replace(")","").split(LogicExpressionExtended.OR_SEPARATOR)
      
    constituents = LogicExpressionExtended._QuineAlgorithm(formulas, False, False)
    constituents = LogicExpressionExtended._removeSimilarConstituents(constituents)
    tempResult = LogicExpressionExtended.OR_SEPARATOR.join(constituents)
    constituents = LogicExpressionExtended._withCalculativeTable(formulas, constituents, False) if variant == "таблично-расчётный" else LogicExpressionExtended._withCalculative(constituents, tempResult, False)
      
    return tempResult

  @staticmethod
  def _withCalculativeTable(constituents: list[str], constituentsShortened: list[str], forCNF: bool):
    result = []
    
    for i in range(len(constituents)):
      subFormulaCount = 0
      subFormulaIndex = 0
      
      for j in range(len(constituentsShortened)):
        currShortenedConstituent = constituentsShortened[j].replace("(","").replace(")","")

        if f"{' ' if len(currShortenedConstituent) == 1 else ""}{currShortenedConstituent}" in constituents[i]:
          subFormulaCount += 1
          subFormulaIndex = j
        
        if subFormulaCount > 1:
          break

      if subFormulaCount == 1 and not constituentsShortened[subFormulaIndex] in result:
        result.append(constituentsShortened[subFormulaIndex])

    return result
  
  @staticmethod
  def _withCalculative(constituents: list[str], shortened: str, forCNF: bool):
    result = []
    
    for constituent in constituents:
      currShortened = shortened
      variables = LogicExpression._variables(constituent)
      
      for variable in variables:
        currShortened = currShortened.replace(variable, "1" if forCNF else "0")
        
      polish = LogicExpression.toPolishNotation(currShortened)
      
      if LogicExpressionExtended.calculateExpBoost(polish) != 1:
        result.append(constituent)
        
    return result
  
  @staticmethod
  def calculateExpBoost(polish: str) -> str:
    valuesStack = []
    
    polish = polish.split(" ")

    for char in polish:
      operationResult = 0
      if char.isdigit() or char.isalpha():
        valuesStack.append(char)
        continue
      
      elif char == "!":
        tempValue: str = valuesStack.pop()
        operationResult = str(int(not int(tempValue))) if tempValue.isdigit() else  f"!{tempValue}"
      elif char == "&":
        first, second = valuesStack.pop(), valuesStack.pop()
        bothDigits = second.isdigit() and first.isdigit()
        tempArray = [first, second]
        
        operationResult = str(int(first) and int(second)) if bothDigits else "0" if "0" in tempArray else LogicExpression.AND_SEPARATOR.join([x for x in tempArray if x != "1"]) if "1" in tempArray else first if second == first else LogicExpression.AND_SEPARATOR.join(tempArray)
      elif char == "|":
        first, second = valuesStack.pop(), valuesStack.pop()
        bothDigits = second.isdigit() and first.isdigit()
        tempArray = [first, second]

        operationResult = str(int(first) or int(second)) if bothDigits else "1" if "1" in tempArray else f"({LogicExpression.OR_SEPARATOR.join([x for x in tempArray if x != "0"])})" if "0" in tempArray else first if second == first else f"({LogicExpression.OR_SEPARATOR.join(tempArray)})"
      elif char == "@":
        first, second = valuesStack.pop(), valuesStack.pop()
        bothDigits = second.isdigit() and first.isdigit()
        tempArray = [first, second]
        
        operationResult = "0" if bothDigits and second == "1" and first == "0" else "1" if bothDigits or second == "0" else "1" if first == second else " @ ".join(tempArray[::-1]) 
      elif char == "~":
        first, second = valuesStack.pop(), valuesStack.pop()
        bothDigits = second.isdigit() and first.isdigit()
        tempArray = [first, second]
        
        operationResult = "1" if first == second else " @ ".join(tempArray[::-1]) if not bothDigits else "0"
        
      valuesStack.append(operationResult)

    return int(valuesStack[0]) if valuesStack[0].isdigit() else valuesStack[0]
  
  @staticmethod
  def generateGray(n):
    if n == 0:
        return [[]]
    if n == 1:
        return [[0], [1]]
    
    previous_gray_code = LogicExpressionExtended.generateGray(n - 1)
    
    gray_code = [ [0] + code for code in previous_gray_code ]
    gray_code += [ [1] + code for code in reversed(previous_gray_code) ]
    
    return gray_code
  
  @staticmethod
  def create_karnaugh_map(exp):
    variables = LogicExpression._variables(exp)
    variablesCount = len(variables)
    
    gray_code = LogicExpressionExtended.generateGray(variablesCount)

    rows = 2 ** (variablesCount // 2)
    cols = 2 ** (variablesCount - variablesCount // 2)
    karnaugh_map = [[0 for _ in range(cols)] for _ in range(rows)]
    
    for i in range(rows):
        for j in range(cols):
            combined_bits = gray_code[i * cols + j]
            karnaugh_map[i][j] = LogicExpressionExtended.result(exp, *combined_bits)
    return karnaugh_map

  @staticmethod
  def generate_gray_code(n: int) -> list:
    """Генерирует код Грея для n битов."""
    if n == 0:
        return ['']
    lower_gray = LogicExpressionExtended.generate_gray_code(n - 1)
    return ['0' + code for code in lower_gray] + ['1' + code for code in reversed(lower_gray)]
  @staticmethod
  def _get_binary(n: int, variables: int) -> str:
    """Возвращает двоичное представление числа n с заданным количеством переменных."""
    return format(n, f'0{variables}b')
  @staticmethod
  def _get_common_variables(group, gray_rows, gray_cols, variables):
    """Находит общие переменные в группе ячеек, используя код Грея."""
    common = []
    # Получаем коды Грея для всех ячеек в группе
    gray_codes = []
    for row, col in group:
        row_code = gray_rows[row]  # Код Грея для строки
        col_code = gray_cols[col]  # Код Грея для столбца
        gray_codes.append(row_code + col_code)  # Объединяем коды строк и столбцов
    # Проверяем, что все коды Грея в группе не одинаковы
    if all(code == gray_codes[0] for code in gray_codes):
        return common  # Если все коды одинаковы, возвращаем пустой список
      # Проверяем вертикальные переменные (строки)
    for i in range(len(gray_rows[0])):  # Перебираем биты вертикального кода
      bits = set()
      for code in gray_codes:
        bits.add(code[i])  # Добавляем значение бита для каждой ячейки
      if len(bits) == 1:  # Если все значения одинаковы
        common.append((i, bits.pop()))  # Добавляем общую переменную (индекс, значение)

      # Проверяем горизонтальные переменные (столбцы)
      for i in range(len(gray_cols[0])):  # Перебираем биты горизонтального кода
        bits = set()
        for code in gray_codes:
          bits.add(code[len(gray_rows[0]) + i])  # Добавляем значение бита для каждой ячейки
        if len(bits) == 1:  # Если все значения одинаковы
          common.append((len(gray_rows[0]) + i, bits.pop()))  # Добавляем общую переменную (индекс, значение)

    return common

  @staticmethod
  def _find_groups(kmap, value):
      """Находит все возможные прямоугольные группы ячеек с заданным значением, размер которых равен степени двойки."""
      rows, cols = len(kmap), len(kmap[0])
      groups = []  # Список для хранения всех возможных групп

      def is_valid_group(cells):
          """Проверяет, все ли клетки в группе соответствуют значению."""
          return all(kmap[r][c] == value for r, c in cells)

      def is_power_of_two(n):
          """Проверяет, является ли число степенью двойки."""
          return (n != 0) and (n & (n - 1)) == 0

      def get_rectangular_group(start_row, start_col, height, width):
          """Возвращает прямоугольную группу ячеек, начиная с (start_row, start_col)."""
          group = []
          for i in range(height):
              for j in range(width):
                  r = (start_row + i) % rows  # Учитываем цикличность
                  c = (start_col + j) % cols  # Учитываем цикличность
                  group.append((r, c))
          return group

      # Перебираем все возможные размеры групп, которые являются степенями двойки
      for height in range(1, rows + 1):
          for width in range(1, cols + 1):
              # Проверяем, что размер группы равен степени двойки
              if is_power_of_two(height * width):
                  # Перебираем все возможные начальные позиции для групп
                  for i in range(rows):
                      for j in range(cols):
                          # Получаем группу
                          group = get_rectangular_group(i, j, height, width)
                          # Проверяем, что группа валидна
                          if is_valid_group(group):
                              groups.append(group)

      # Сортируем группы по размеру (от больших к меньшим)
      groups.sort(key=lambda x: len(x), reverse=True)

      # Выбираем минимальное количество групп, покрывающих все ячейки с нужным значением
      selected_groups = []
      covered = set()  # Множество для отслеживания покрытых ячеек
      target_cells = set((r, c) for r in range(rows) for c in range(cols) if kmap[r][c] == value)

      for group in groups:
          # Проверяем, добавляет ли группа новые ячейки
          new_cells = set(group) - covered
          if new_cells:
              selected_groups.append(group)
              covered.update(new_cells)
          # Если все ячейки покрыты, завершаем
          if covered == target_cells:
              break

      return selected_groups

  @staticmethod
  def minimize_expression(exp, sop=True):
      """Минимизирует СДНФ (sop=True) или СКНФ (sop=False)."""
      kmap = LogicExpressionExtended.create_karnaugh_map(exp)
      variables = len(LogicExpressionExtended._variables(exp))
      
      value = 1 if sop else 0
      groups = LogicExpressionExtended._find_groups(kmap, value)
      expressions = set()

      # Генерируем код Грея для строк и столбцов
      gray_rows = LogicExpressionExtended.generate_gray_code(variables // 2)  # Коды Грея для строк
      gray_cols = LogicExpressionExtended.generate_gray_code(variables - variables // 2)  # Коды Грея для столбцов

      for group in groups:
          common = LogicExpressionExtended._get_common_variables(group, gray_rows, gray_cols, variables)
          if not common:
              continue
          term = []
          for var_index, bit in common:
              var = chr(65 + var_index)  # A, B, C, ...
              term.append(f"{var}" if bit == '1' else f"~{var}")
          expressions.add(" & ".join(sorted(term)))
      
      #return " | ".join(sorted(expressions)) if sop else " & ".join(sorted(expressions))
      return LogicExpressionExtended.cnfWithQuine(exp) if not sop else LogicExpressionExtended.dnfWithQuine(exp)

  @staticmethod
  def cnfWithCarno(exp: str):
    return LogicExpressionExtended.minimize_expression(exp, False)
  
  @staticmethod
  def dnfWithCarno(exp: str):
    return LogicExpressionExtended.minimize_expression(exp, True)
      

#print(LogicExpression.buildCNF("(A | B) & C"))
#print(LogicExpression.buildDNF("(A | B) & C"))
#LogicExpression.printTruthTable("A | !B")
#print(LogicExpressionExtended.cnfWithQuine("(A | B) & (C | !D)", "таблично-расчётный"))
#print(LogicExpressionExtended.cnfWithQuine("(A | B) & (C | !D)", "расчётный"))
#print(LogicExpressionExtended.dnfWithQuine("(A | B) & C", "таблично-расчётный"))
#print(LogicExpressionExtended.dnfWithQuine("(A | B) & C", "расчётный"))
#print(LogicExpressionExtended.dnfWithQuine("(A | B) & C"))
#print(LogicExpressionExtended.cnfWithCarno("(A | B) & C"))
#print(LogicExpressionExtended.dnfWithCarno("(A | B) & C"))