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
    constituents = LogicExpressionExtended._withCalculativeTable(formulas, constituents, tempResult) if variant == "таблично-расчётный" else LogicExpressionExtended._withCalculative(constituents, tempResult, True)
    
    return LogicExpressionExtended.AND_SEPARATOR.join(LogicExpressionExtended._removeSimilarConstituents(constituents))
  
  @staticmethod
  def dnfWithQuine(exp: str, variant: str = "расчётный") -> str:
    formulas = LogicExpression.buildDNF(exp).replace("(","").replace(")","").split(LogicExpressionExtended.OR_SEPARATOR)
      
    constituents = LogicExpressionExtended._QuineAlgorithm(formulas, False, False)
    constituents = LogicExpressionExtended._removeSimilarConstituents(constituents)
    tempResult = LogicExpressionExtended.OR_SEPARATOR.join(constituents)
    constituents = LogicExpressionExtended._withCalculativeTable(formulas, constituents, tempResult) if variant == "таблично-расчётный" else LogicExpressionExtended._withCalculative(constituents, tempResult, False)
      
    return tempResult

  @staticmethod
  def _withCalculativeTable(constituents: list[str], constituentsShortened: list[str], shortenedFormula: str):
    result = []
    
    for i in range(len(constituents)):
      subFormulaCount = 0
      subFormulaIndex = 0
      
      for j in range(len(constituentsShortened)):
        currShortenedConstituent = constituentsShortened[j].replace("(","").replace(")","")
        
        if currShortenedConstituent in constituents[i]:
          subFormulaCount += 1
          subFormulaIndex = j
          
      
      if subFormulaCount == 1:
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

      for char in currShortened:
        if char.isalpha():
          currShortened = currShortened.replace(char, "0" if forCNF else "1")
        
      polish = LogicExpression.toPolishNotation(currShortened)
      
      if LogicExpression.calculateExp(polish) == 0:
        result.append(constituent)
        
    return result
    
    

#print(LogicExpression.buildCNF("(A | B) & C"))
#print(LogicExpression.buildDNF("(A | B) & C"))
#LogicExpression.printTruthTable("A | !B")
#print(LogicExpressionExtended.cnfWithQuine("(A | B) & (C | !D)", "таблично-расчётный"))
#print(LogicExpressionExtended.dnfWithQuine("(A | B) & C"))