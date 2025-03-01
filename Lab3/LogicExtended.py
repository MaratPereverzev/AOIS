from Lab2.Logic import LogicExpression
from typing import List

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
  def cnfWithQuine(exp: str, variant: str = "расчётный") -> str:
    formulas = LogicExpression.buildCNF(exp).replace("(","").replace(")","").split(LogicExpressionExtended.AND_SEPARATOR)
      
    constituents = LogicExpressionExtended._QuineAlgorithm(formulas, False, True)
    constituents = LogicExpressionExtended._removeSimilarConstituents(constituents)
    
    for i in range(len(constituents)):
      if len(constituents[i]) > 1:
        constituents[i] = f"({constituents[i]})"
        
    tempResult = LogicExpressionExtended.AND_SEPARATOR.join(constituents)
    
    constituents = LogicExpressionExtended._withCalculativeTable(formulas, constituents, True) if variant == "таблично-расчётный" else LogicExpressionExtended._withCalculative(constituents, tempResult, True)
    
    return LogicExpressionExtended.AND_SEPARATOR.join(LogicExpressionExtended._removeSimilarConstituents(constituents))
  
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
      
      if LogicExpressionExtended._hypoteticCalculateExp(polish) != 1:
        result.append(constituent)
        
    return result
  
  @staticmethod
  def _hypoteticCalculateExp(polish: str) -> str:
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
        
        operationResult = str(int(first) and int(second)) if bothDigits else "0" if "0" in tempArray else LogicExpression.AND_SEPARATOR.join([x for x in tempArray if x != "1"]) if "1" in tempArray else LogicExpression.AND_SEPARATOR.join(tempArray)
      elif char == "|":
        first, second = valuesStack.pop(), valuesStack.pop()
        bothDigits = second.isdigit() and first.isdigit()
        tempArray = [first, second]

        operationResult = str(int(first) or int(second)) if bothDigits else "1" if "1" in tempArray else f"({LogicExpression.OR_SEPARATOR.join([x for x in tempArray if x != "0"])})" if "0" in tempArray else f"({LogicExpression.OR_SEPARATOR.join(tempArray)})"
      elif char == "@":
        first, second = valuesStack.pop(), valuesStack.pop()
        bothDigits = second.isdigit() and first.isdigit()
        tempArray = [first, second]
        
        operationResult = "0" if bothDigits and second == "1" and first == "0" else "1" if bothDigits or second == "0" else " @ ".join(tempArray) 
      elif char == "~":
        first, second = valuesStack.pop(), valuesStack.pop()
        operationResult = "1" if first == second else "0"
        
      valuesStack.append(operationResult)

    return int(valuesStack[0]) if valuesStack[0].isdigit() else valuesStack[0]
    
    

#print(LogicExpression.buildCNF("(A | B) & C"))
#print(LogicExpression.buildDNF("(A | B) & C"))
#LogicExpression.printTruthTable("A | !B")
#print(LogicExpressionExtended.cnfWithQuine("(A | B) & (C | !D)", "таблично-расчётный"))
#print(LogicExpressionExtended.cnfWithQuine("(A | B) & (C | !D)", "расчётный"))
#print(LogicExpressionExtended.dnfWithQuine("(A | B) & C", "таблично-расчётный"))
#print(LogicExpressionExtended.dnfWithQuine("(A | B) & C", "расчётный"))
#print(LogicExpressionExtended.dnfWithQuine("(A | B) & C"))