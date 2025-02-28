from Lab2.Logic import LogicExpression
from typing import List

class LogicExpressionExtended (LogicExpression):
  @staticmethod
  def _isBondable(firstConstituent: List[str], secondConstituent) -> bool:
    notEqualCount = 0
    hasOpposite = False
    for i in range(min(len(firstConstituent), len(secondConstituent))):
      if firstConstituent[i] == f"!{secondConstituent[i]}" or f"!{firstConstituent[i]}" == secondConstituent[i]:
        hasOpposite = True
        notEqualCount += 1
      elif firstConstituent[i] != secondConstituent[i]:
        notEqualCount += 1
      
    return True if notEqualCount == 1 and hasOpposite == True else False
  
  @staticmethod
  def _getSimilarVariables(firstConstituent: List[str], secondConstituent) -> bool:
    similar = []
    
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
  def _QuineAlgorithm(constituents: List[List[str]], notFirstIteration: bool) -> str:
    nextConstituent = []
    callRecursive = False
    bondableIteration = False
    
    for i in range(len(constituents) - 1):
      bondableIteration = False
      for j in range(len(constituents)):
        if LogicExpressionExtended._isBondable(constituents[i], constituents[j]):
          bondableIteration = True
          if i < j: 
            callRecursive = True
            nextConstituent.append(LogicExpressionExtended._getSimilarVariables(constituents[i], constituents[j]))
      if not bondableIteration and notFirstIteration:
        nextConstituent.append(constituents[i])
        
    if not bondableIteration and not callRecursive and notFirstIteration:
      nextConstituent.append(constituents[-1])
    
    if callRecursive: 
      nextConstituent = LogicExpressionExtended._QuineAlgorithm(nextConstituent, True)
      
    return nextConstituent
  
  @staticmethod
  def cnfWithQuine(exp: str) -> str:
    formulas = LogicExpression.buildCNF(exp).replace("(","").replace(")","").split(" & ")
    
    for i in range(len(formulas)):
      formulas[i] = formulas[i].split(" | ")
      
    constituents = LogicExpressionExtended._QuineAlgorithm(formulas, False)
    constituents = LogicExpressionExtended._removeSimilarConstituents(constituents)
    
    result = []
    
    for constituent in constituents:
      currConstituent = " | ".join(constituent)
      if len(constituent) > 1:
        currConstituent = f"( {currConstituent} )"
      
      result.append(currConstituent)
      
          
    return " & ".join(result)
  
  @staticmethod
  def dnfWithQuine(exp: str) -> str:
    formulas = LogicExpression.buildDNF(exp).replace("(","").replace(")","").split(" | ")
    
    for i in range(len(formulas)):
      formulas[i] = formulas[i].split(" & ")
      
    constituents = LogicExpressionExtended._QuineAlgorithm(formulas, False)
    constituents = LogicExpressionExtended._removeSimilarConstituents(constituents)
    
    result = []
    
    for constituent in constituents:
      currConstituent = " & ".join(constituent)
      
      result.append(currConstituent)
       
    return " | ".join(result)
    

#print(LogicExpression.buildCNF("(A | B) & C"))
#print(LogicExpression.buildDNF("(A | B) & C"))
#LogicExpression.printTruthTable("A | !B")
print(LogicExpressionExtended.cnfWithQuine("(A | B) & C"))
print(LogicExpressionExtended.dnfWithQuine("(A | B) & C"))