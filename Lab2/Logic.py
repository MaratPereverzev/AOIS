from Lab1.Binary import Binary
from typing import List

class LogicExpression:
  tokens = {
    "(" : -1,
    ")": -2,
    "!": 5,
    "&": 4,
    "|": 3,
    "@": 2,
    "~": 1
  }
  acceptedTokens = ["(", ")", "!", "&", "|", "@", "~"]
  
  @staticmethod
  def toPolishNotation(exp: str) -> str:
    exp = exp.replace("->","@")
    
    stackTokens = []
    result = ""
    
    for i in range(len(exp)):
      if exp[i].isalpha():
        result += exp[i]
        continue
      elif exp[i] == " ":
        continue
      elif exp[i] not in LogicExpression.acceptedTokens:
        raise SyntaxError(f"Incorrect operator {exp[i]}")
      elif LogicExpression.tokens[exp[i]] == -2:
        if not len(stackTokens):
          raise SyntaxError("Added an extra )")
        
        while len(stackTokens) and LogicExpression.tokens[stackTokens[-1]] != -1:
          result += str(stackTokens.pop())
          
        stackTokens.pop()
      else:
        while len(stackTokens) and LogicExpression.tokens[stackTokens[-1]] > LogicExpression.tokens[exp[i]] and LogicExpression.tokens[exp[i]] > 0:
          result += stackTokens.pop()
        
        stackTokens.append(exp[i])
        
    for token in reversed(stackTokens):
      if LogicExpression.tokens[token] == -1:
        raise SyntaxError("Added an extra (")
      elif LogicExpression.tokens[token] == -2:
        raise SyntaxError("Added an extra )")
      else:
        result += str(token)
      
    return " ".join(result)
  
  @staticmethod
  def result(exp: str, *values: List[str]) -> str:
    polish = LogicExpression.toPolishNotation(exp)
    
    variables = LogicExpression._variables(exp)
    
    values = values[:len(variables)]
    
    if len(values) < len(variables):
      raise ValueError("You forgot to pass all the values for the variables")

    variables = sorted(variables)

    for i in range(len(values)):
      polish = polish.replace(variables[i], str(values[i]))
      
    return LogicExpression.calculateExp(polish)
  
  @staticmethod
  def _variables(polish: str) -> List[int]:
    variables = []
    
    for char in polish:
      if char.isalpha() and not char in variables:
        variables.append(char)
        
    return variables
    
  @staticmethod
  def calculateExp(polish: str) -> int:
    valuesStack = []
    
    polish = polish.split(" ")

    for char in polish:
      operationResult = 0
      if char.isdigit():
        valuesStack.append(int(char))
        continue
        
      elif char == "!":
        tempValue = valuesStack.pop()
        operationResult = int(not tempValue)
      elif char == "&":
        first, second = valuesStack.pop(), valuesStack.pop()
        operationResult = int(first and second)
      elif char == "|":
        first, second = valuesStack.pop(), valuesStack.pop()
        operationResult = int(first or second)
      elif char == "@":
        first, second = valuesStack.pop(), valuesStack.pop()
        operationResult = 0 if second == 1 and first == 0 else 1
      elif char == "~":
        first, second = valuesStack.pop(), valuesStack.pop()
        operationResult = 1 if first == second else 0
        
      valuesStack.append(operationResult)

    return valuesStack[0]
  
  @staticmethod
  def buildDNF(exp: str) -> str:
    polish = LogicExpression.toPolishNotation(exp)
    variables = LogicExpression._variables(polish)
    variablesCount = len(variables)
    binary = "0" * variablesCount
    
    cnfExpressions = []
    
    while len(binary) <= variablesCount:
      expResult = LogicExpression.result(exp, *binary)
      
      if expResult == 0:
        binary = Binary._sum(binary, "1").zfill(variablesCount)
        continue
      
      binaryList = list(binary)
      currValues = []
      
      for i in range(variablesCount):
        currValues.append(f"!{variables[i]}" if binaryList[i] == "0" else variables[i])
          
      cnfExpressions.append(f"({' & '.join(currValues)})")
      
      binary = Binary._sum(binary, "1").zfill(variablesCount)
      
    return " | ".join(cnfExpressions)
  
  @staticmethod
  def buildCNF(exp: str) -> str:
    polish = LogicExpression.toPolishNotation(exp)
    variables = LogicExpression._variables(polish)
    variablesCount = len(variables)
    binary = "0" * variablesCount
    
    cnfExpressions = []
    
    while len(binary) <= variablesCount:
      expResult = LogicExpression.result(exp, *binary)
      
      if expResult == 1:
        binary = Binary._sum(binary, "1").zfill(variablesCount)
        continue
      
      binaryList = list(binary)
      currValues = []
      
      for i in range(variablesCount):
        currValues.append(f"!{variables[i]}" if binaryList[i] == "1" else variables[i])
          
      cnfExpressions.append(f"({' | '.join(currValues)})")
      
      binary = Binary._sum(binary, "1").zfill(variablesCount)
      
    return " & ".join(cnfExpressions)
  
  @staticmethod
  def getForms(exp: str):
    polish = LogicExpression.toPolishNotation(exp)
    variablesCount = len(LogicExpression._variables(polish))
    binary = "0" * variablesCount
    
    conj = []
    disj = []

    indexForm = ""
    
    while len(binary) <= variablesCount:
      expResult = LogicExpression.result(exp, *binary)
      
      indexForm += str(expResult)
      if expResult == 0:
        disj.append(str(Binary.binaryToInt(binary)))
      else:
        conj.append(str(Binary.binaryToInt(binary)))
      
      binary = Binary._sum(binary, "1").zfill(variablesCount)
      
    return {"indexForm": indexForm, "numberForm" : {"conj": f"({", ".join(conj)}) &", "disj": f"({", ".join(disj)}) |"}}
  
  @staticmethod
  def printTruthTable(exp: str):
    polish = LogicExpression.toPolishNotation(exp)
    variables = LogicExpression._variables(polish)
    variablesCount = len(variables)
    binary = "0" * variablesCount
    
    operations = LogicExpression.getPossibleOperations(exp)
    for operation in operations:
      variables.append(operation)
      
    header = " | ".join(variables)
    
    print(header)
    print("-"*len(header))
    while len(binary) <= variablesCount:
      row = " | ".join(binary)
      operationResults = []
      
      for operation in operations:
        currExpResult = LogicExpression.result(operation, *binary)
        operationResults.append(str(currExpResult))
        row += " | " + str(currExpResult) + " " * (len(operation) - 1)

      print(row)
      
      binary = Binary._sum(binary, "1").zfill(variablesCount)
  
  @staticmethod
  def getPossibleOperations(exp: str) -> List[str]:
    valuesStack = []
    operations = []
    polish = LogicExpression.toPolishNotation(exp)
    
    for char in polish:
      operation = ""
      if char == " ":
        continue
      if char.isalpha():
        valuesStack.append(char)
        continue
        
      elif char == "!":
        tempValue = valuesStack.pop()
        operation = f"!{tempValue}"
      elif char == "&":
        first, second = valuesStack.pop(), valuesStack.pop()
        operation = f"{second} & {first}"
      elif char == "|":
        first, second = valuesStack.pop(), valuesStack.pop()
        operation = f"({second} | {first})"
      elif char == "@":
        first, second = valuesStack.pop(), valuesStack.pop()
        operation = f"({second} -> {first})"
      elif char == "~":
        first, second = valuesStack.pop(), valuesStack.pop()
        operation = f"({second} ~ {first})"
      operations.append(operation)
      valuesStack.append(operation)

    return operations
  
#print(LogicExpression.toPolishNotation("(A | B) & !C"))
#print(LogicExpression.buildCNF("(A | B) & !C"))
#print(LogicExpression.buildDNF("(A | B) & !C"))
#print(LogicExpression.getForms("(A | B) & !C"))
#LogicExpression.printTruthTable("(A | B) & !C")
#print(LogicExpression.getPossibleOperations("A | B"))
#print(LogicExpression.toPolishNotation("(A | B"))
#print(LogicExpression.getForms("A & B"))
#print(LogicExpression.printTruthTable(" A & B"))