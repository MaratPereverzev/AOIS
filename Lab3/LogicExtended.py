from Lab2.Logic import LogicExpression
from typing import List
from itertools import product
from Lab1.Binary import Binary
import math

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
    
    if len(nextConstituent) == 0 and not notFirstIteration:
      return constituents
    
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
        return [["0"], ["1"]]
    
    previous_gray_code = LogicExpressionExtended.generateGray(n - 1)
    
    gray_code = [ ["0"] + code for code in previous_gray_code ]
    gray_code += [ ["1"] + code for code in reversed(previous_gray_code) ]
    
    return gray_code
  
  @staticmethod
  def buildFormulaFromGroups(groups: List[List[str]], variables: List[str], isCNF = False):
    formulas = []
    similarVariables = []
    for group in groups:
      similarVariablesList = list(group[0])
    
      for value in group:
        for i in range(0, len(value)):
          if value[i] != similarVariablesList[i]: similarVariablesList[i] = "_"
         
      similarVariables.append(similarVariablesList)
      
    for variable in similarVariables:
      tempFormulaList = []
      for i in range(len(variable)):
        if variable[i] == '1': tempFormulaList.append(f'!{variables[i]}' if isCNF else variables[i])
        elif variable[i] == '0': tempFormulaList.append(variables[i] if isCNF else f'!{variables[i]}')
        
      formulas.append(f"({(LogicExpressionExtended.OR_SEPARATOR if isCNF else LogicExpressionExtended.AND_SEPARATOR).join(tempFormulaList)})")
      
    return (LogicExpressionExtended.AND_SEPARATOR if isCNF else LogicExpressionExtended.OR_SEPARATOR).join(formulas)
  
  @staticmethod
  def minimizeExpression(exp: str, isCNF=False):    
    variables = LogicExpressionExtended._variables(exp)
    
    carnoTable = LogicExpressionExtended.makeCarnoTable(exp)

    groups = LogicExpressionExtended.findGroups(exp, carnoTable, isCNF)
    
    formula = LogicExpressionExtended.buildFormulaFromGroups(groups, variables, isCNF)
    
    return formula
   
  @staticmethod
  def findRectangleGroups(carnoTable: List[List[int]], maxGroupSize: int, grayHorizontal: List[str], grayVertical: List[str], isCNF=False):
    groups = []
    visited = set()
    rows = len(carnoTable)
    cols = len(carnoTable[0]) if rows > 0 else 0
    
    # Все возможные размеры прямоугольников (2^n × 2^m)
    sizes = []
    size = maxGroupSize
    while size >= 1:
        sizes.append(size)
        size //= 2
    
    # Проверяем все возможные комбинации размеров
    for height in sizes:
        for width in sizes:
            # Пропускаем слишком большие размеры
            if height > rows or width > cols:
                continue
                
            # Проверяем все возможные позиции прямоугольника
            for i in range(rows - height + 1):
                for j in range(cols - width + 1):
                    # Проверяем, состоит ли прямоугольник из единиц
                    all_ones = True
                    current_group = []
                    
                    for x in range(i, i + height):
                        for y in range(j, j + width):
                            if carnoTable[x][y] != 1 and not isCNF or carnoTable[x][y] != 0 and isCNF:
                                all_ones = False
                                break
                            current_group.append(grayVertical[x] + grayHorizontal[y])
                        if not all_ones:
                            break
                    
                    # Если нашли прямоугольник и есть новые переменные
                    if all_ones:
                        new_vars = [var for var in current_group if var not in visited]
                        if new_vars:
                            groups.append(current_group)
                            visited.update(new_vars)
    
    return groups
  
  @staticmethod
  def findGroups(exp: str, carnoTable: str, isCNF=False):
    carnoTableExtended = [row * 2 for row in carnoTable]
    carnoTableExtended *= 2
    
    variables = LogicExpressionExtended._variables(exp)
    variablesCount = len(variables)
    
    grayHorizontal = LogicExpressionExtended.generateGray(variablesCount // 2 + (variablesCount % 2))
    grayHorizontal = ["".join(code) for code in grayHorizontal]
    
    grayVertical = LogicExpressionExtended.generateGray(variablesCount // 2)
    grayVertical = ["".join(code) for code in grayVertical]

    groups = []
    
    maxGroupSize = 2 ** (variablesCount - 1)
    
    groups.extend(LogicExpressionExtended.findRectangleGroups(carnoTable, maxGroupSize, grayHorizontal, grayVertical, isCNF))
    
    return groups
        
    
  @staticmethod
  def makeCarnoTable(exp: str):
    variables = LogicExpressionExtended._variables(exp)
    variablesCount = len(variables)
    
    grayHorizontal = LogicExpressionExtended.generateGray(variablesCount // 2 + (variablesCount % 2))
    grayHorizontal = ["".join(code) for code in grayHorizontal]
    
    grayVertical = LogicExpressionExtended.generateGray(variablesCount // 2)
    grayVertical = ["".join(code) for code in grayVertical]
    
    carnoTable = [0] * len(grayVertical)
    
    carnoTable = [[0] * len(grayHorizontal) for _ in carnoTable]
    
    for i in range(len(grayVertical)):
      for j in range(len(grayHorizontal)):
        carnoTable[i][j] = LogicExpressionExtended.result(exp, *grayVertical[i], *grayHorizontal[j])
        
    return carnoTable
    

  @staticmethod
  def cnfWithCarno(exp: str):
    return LogicExpressionExtended.minimizeExpression(exp, True)
  
  @staticmethod
  def dnfWithCarno(exp: str):
    return LogicExpressionExtended.minimizeExpression(exp)

print(LogicExpressionExtended.dnfWithCarno("(A | B) & C"))
#print("СКНФ и CДНФ\n")
#print("СКНФ:", LogicExpression.buildCNF("(!A & B) | (!(C | D))"))
#print("СДНФ:", LogicExpression.buildDNF("(!A & B) | (!(C | D))"))
#print("-"*40,"\nТаблица истинности\n\n")
#LogicExpression.printTruthTable("(A | B) & C")
#print("-"*40,"\nМинимизация СКНФ\n\n")
#print(LogicExpressionExtended.cnfWithQuine("(A | B) & C", "таблично-расчётный"))
#print(LogicExpressionExtended.cnfWithCarno("(A | B) & C"))
#print("-"*40,"\nМинимизация СДНФ\n\n")
#print(LogicExpressionExtended.dnfWithQuine("(A | B) & C", "таблично-расчётный"))
#print(LogicExpressionExtended.dnfWithQuine("(!A & B) | (!(C | D))", "расчётный"))
#print(LogicExpressionExtended.dnfWithCarno("(A | B) & C"))