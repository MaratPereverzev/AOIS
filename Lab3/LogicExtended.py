from Lab2.Logic import LogicExpression
from typing import List, Set, Dict
from itertools import product
from Lab1.Binary import Binary
import math


class LogicExpressionExtended(LogicExpression):
    @staticmethod
    def _isBondable(first: str, second: str, forCNF: bool) -> bool:
        first_vars = set(LogicExpressionExtended._parseForCNF(first, not forCNF))
        second_vars = set(LogicExpressionExtended._parseForCNF(second, not forCNF))

        # Find symmetric difference
        diff = first_vars.symmetric_difference(second_vars)

        # Should differ by exactly one complementary pair
        if len(diff) != 2:
            return False

        # Check if the differing literals are complements
        a, b = diff.pop(), diff.pop()
        return (a == f"!{b}") or (b == f"!{a}")

    @staticmethod
    def _getSimilarVariables(
        firstConstituent: str, secondConstituent: str, forCNF: bool
    ) -> bool:
        similar = []

        firstConstituent = LogicExpressionExtended._parseForCNF(
            firstConstituent, not forCNF
        )
        secondConstituent = LogicExpressionExtended._parseForCNF(
            secondConstituent, not forCNF
        )

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
        return (
            constituent.split(LogicExpressionExtended.AND_SEPARATOR)
            if forCNF
            else constituent.split(LogicExpressionExtended.OR_SEPARATOR)
        )

    @staticmethod
    def _QuineAlgorithm(terms: List[str], forCNF: bool) -> List[str]:
        def split_term(term: str) -> Set[str]:
            separator = " | " if forCNF else " & "
            return set(term.strip("()").split(separator))

        def join_term(literals: Set[str]) -> str:
            separator = " | " if forCNF else " & "
            literals = sorted(literals, key=lambda x: (x.replace("!", ""), x))
            return separator.join(literals)

        # Преобразуем все термы к единому формату
        terms = [term.strip("()") for term in terms]
        prime_implicants = set()
        current_terms = terms.copy()

        # Фаза склеивания
        while True:
            next_terms = set()
            used_indices = set()

            # Сортируем по количеству литералов
            current_terms.sort(key=lambda x: len(split_term(x)))

            for i in range(len(current_terms)):
                for j in range(i + 1, len(current_terms)):
                    term1 = current_terms[i]
                    term2 = current_terms[j]

                    # Проверяем возможность склеивания
                    literals1 = split_term(term1)
                    literals2 = split_term(term2)
                    diff = literals1.symmetric_difference(literals2)

                    if len(diff) == 2:
                        a, b = diff.pop(), diff.pop()
                        if (a == f"!{b}") or (b == f"!{a}"):
                            common = literals1 & literals2
                            new_term = join_term(common)
                            next_terms.add(new_term)
                            used_indices.update({i, j})

            # Добавляем неиспользованные термы в простые импликанты
            for i, term in enumerate(current_terms):
                if i not in used_indices:
                    prime_implicants.add(term)

            if not next_terms:
                break

            current_terms = list(next_terms)

        # Фаза построения таблицы покрытия (специально для ДНФ)
        if not forCNF:
            # Преобразуем исходные термы в бинарный формат для анализа
            all_vars = sorted(
                {lit.replace("!", "") for term in terms for lit in split_term(term)}
            )
            term_masks = []

            for term in terms:
                mask = []
                for var in all_vars:
                    if f"!{var}" in split_term(term):
                        mask.append(0)
                    elif var in split_term(term):
                        mask.append(1)
                    else:
                        mask.append(None)  # означает "безразлично"
                term_masks.append(mask)

            # Анализируем простые импликанты
            essential = []
            covered = set()

            for pi in prime_implicants:
                pi_literals = split_term(pi)
                pi_mask = []
                for var in all_vars:
                    if f"!{var}" in pi_literals:
                        pi_mask.append(0)
                    elif var in pi_literals:
                        pi_mask.append(1)
                    else:
                        pi_mask.append(None)

                # Находим какие термы покрывает этот импликант
                covers = []
                for i, term_mask in enumerate(term_masks):
                    match = True
                    for v in range(len(all_vars)):
                        if pi_mask[v] is not None and term_mask[v] != pi_mask[v]:
                            match = False
                            break
                    if match:
                        covers.append(i)

                # Если импликант покрывает хотя бы один непокрытый терм
                if any(i not in covered for i in covers):
                    essential.append(pi)
                    covered.update(covers)

            return essential

        # Оригинальная логика для CNF
        essential = []
        remaining_terms = set(terms)

        for pi in prime_implicants:
            pi_literals = split_term(pi)
            covered = set()

            for term in remaining_terms:
                term_literals = split_term(term)
                if pi_literals.issubset(term_literals):
                    covered.add(term)

            if covered:
                essential.append(pi)
                remaining_terms -= covered

        return essential

    @staticmethod
    def _removeRedundant(
        primes: List[str], original: List[str], forCNF: bool
    ) -> List[str]:
        essential = []
        remaining_terms = original.copy()

        # Находим импликанты, покрывающие уникальные термы
        for pi in primes:
            pi_vars = set(pi.split(" | "))
            covered = []

            for term in remaining_terms:
                term_vars = set(term.split(" | "))
                if forCNF:
                    if pi_vars.issubset(term_vars):
                        covered.append(term)
                else:
                    if term_vars.issubset(pi_vars):
                        covered.append(term)

            if covered:
                essential.append(pi)
                remaining_terms = [t for t in remaining_terms if t not in covered]

        return essential

    @staticmethod
    def cnfWithQuine(exp: str, variant: str = "расчётный", isAlradyKNF=False) -> str:
        if not isAlradyKNF:
            exp = LogicExpression.buildCNF(exp)
        formulas = (
            exp.replace("(", "")
            .replace(")", "")
            .split(LogicExpressionExtended.AND_SEPARATOR)
        )
        constituents = LogicExpressionExtended._QuineAlgorithm(formulas, True)
        constituents = LogicExpressionExtended._removeSimilarConstituents(constituents)

        for i in range(len(constituents)):
            if len(constituents[i]) > 1:
                constituents[i] = f"({constituents[i]})"

        tempResult = LogicExpressionExtended.AND_SEPARATOR.join(constituents)

        constituents = (
            LogicExpressionExtended._withCalculativeTable(formulas, constituents, True)
            if variant == "таблично-расчётный"
            else LogicExpressionExtended._withCalculative(
                constituents, tempResult, True
            )
        )

        return (
            LogicExpressionExtended.AND_SEPARATOR.join(
                LogicExpressionExtended._removeSimilarConstituents(constituents)
            )
            if len(constituents)
            else tempResult
        )

    @staticmethod
    def dnfWithQuine(exp: str, variant: str = "расчётный", isAlradyDNF=False) -> str:
        if not isAlradyDNF:
            exp = LogicExpression.buildDNF(exp)
        formulas = (
            LogicExpression.buildDNF(exp)
            .replace("(", "")
            .replace(")", "")
            .split(LogicExpressionExtended.OR_SEPARATOR)
        )
        constituents = LogicExpressionExtended._QuineAlgorithm(formulas, False)
        constituents = LogicExpressionExtended._removeSimilarConstituents(constituents)
        tempResult = LogicExpressionExtended.OR_SEPARATOR.join(constituents)

        constituents = (
            LogicExpressionExtended._withCalculativeTable(formulas, constituents, False)
            if variant == "таблично-расчётный"
            else LogicExpressionExtended._withCalculative(
                constituents, tempResult, False
            )
        )

        return tempResult

    @staticmethod
    def _withCalculativeTable(
        original: List[str], reduced: List[str], forCNF: bool
    ) -> List[str]:
        essential_implicants = []
        original_terms = [set(LogicExpression._variables(t)) for t in original]

        for impl in reduced:
            impl_vars = set(LogicExpression._variables(impl))
            covers = False

            for orig in original_terms:
                if forCNF:
                    # For CNF, impl should be subset of original
                    if impl_vars.issubset(orig):
                        covers = True
                        break
                else:
                    # For DNF, original should be subset of impl
                    if orig.issubset(impl_vars):
                        covers = True
                        break

            if covers:
                essential_implicants.append(impl)

        return essential_implicants

    @staticmethod
    def _withCalculative(constituents: list[str], shortened: str, forCNF: bool):
        result = []

        for constituent in constituents:
            currShortened = shortened
            variables = LogicExpression._variables(constituent)

            for variable in variables:
                currShortened = currShortened.replace(variable, "1" if forCNF else "0")

            polish = LogicExpression.toPolishNotation(currShortened)

            if (
                LogicExpressionExtended.calculateExpBoost(polish) != 1 and not forCNF
            ) or (
                LogicExpressionExtended.calculateExpBoost(polish) != 0 and not forCNF
            ):
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
                operationResult = (
                    str(int(not int(tempValue)))
                    if tempValue.isdigit()
                    else f"!{tempValue}"
                )
            elif char == "&":
                first, second = valuesStack.pop(), valuesStack.pop()
                bothDigits = second.isdigit() and first.isdigit()
                tempArray = [first, second]

                operationResult = (
                    str(int(first) and int(second))
                    if bothDigits
                    else (
                        "0"
                        if "0" in tempArray
                        else (
                            LogicExpression.AND_SEPARATOR.join(
                                [x for x in tempArray if x != "1"]
                            )
                            if "1" in tempArray
                            else (
                                first
                                if second == first
                                else LogicExpression.AND_SEPARATOR.join(tempArray)
                            )
                        )
                    )
                )
            elif char == "|":
                first, second = valuesStack.pop(), valuesStack.pop()
                bothDigits = second.isdigit() and first.isdigit()
                tempArray = [first, second]

                operationResult = (
                    str(int(first) or int(second))
                    if bothDigits
                    else (
                        "1"
                        if "1" in tempArray
                        else (
                            f"({LogicExpression.OR_SEPARATOR.join([x for x in tempArray if x != "0"])})"
                            if "0" in tempArray
                            else (
                                first
                                if second == first
                                else f"({LogicExpression.OR_SEPARATOR.join(tempArray)})"
                            )
                        )
                    )
                )
            elif char == "@":
                first, second = valuesStack.pop(), valuesStack.pop()
                bothDigits = second.isdigit() and first.isdigit()
                tempArray = [first, second]

                operationResult = (
                    "0"
                    if bothDigits and second == "1" and first == "0"
                    else (
                        "1"
                        if bothDigits or second == "0"
                        else "1" if first == second else " @ ".join(tempArray[::-1])
                    )
                )
            elif char == "~":
                first, second = valuesStack.pop(), valuesStack.pop()
                bothDigits = second.isdigit() and first.isdigit()
                tempArray = [first, second]

                operationResult = (
                    "1"
                    if first == second
                    else " @ ".join(tempArray[::-1]) if not bothDigits else "0"
                )

            valuesStack.append(operationResult)

        return (
            valuesStack[0]
            if isinstance(valuesStack[0], int)
            else int(valuesStack[0]) if valuesStack[0].isdigit() else valuesStack[0]
        )

    @staticmethod
    def generateGray(n):
        if n == 0:
            return [[]]
        if n == 1:
            return [["0"], ["1"]]

        previous_gray_code = LogicExpressionExtended.generateGray(n - 1)

        gray_code = [["0"] + code for code in previous_gray_code]
        gray_code += [["1"] + code for code in reversed(previous_gray_code)]

        return gray_code

    @staticmethod
    def buildFormulaFromGroups(
        groups: List[List[str]], variables: List[str], isCNF=False
    ):
        formulas = []
        similarVariables = []
        for group in groups:
            similarVariablesList = list(group[0])

            for value in group:
                for i in range(0, len(value)):
                    if value[i] != similarVariablesList[i]:
                        similarVariablesList[i] = "_"

            similarVariables.append(similarVariablesList)

        for variable in similarVariables:
            tempFormulaList = []
            for i in range(len(variable)):
                if variable[i] == "1":
                    tempFormulaList.append(
                        f"!{variables[i]}" if isCNF else variables[i]
                    )
                elif variable[i] == "0":
                    tempFormulaList.append(
                        variables[i] if isCNF else f"!{variables[i]}"
                    )

            formulas.append(
                f"({(LogicExpressionExtended.OR_SEPARATOR if isCNF else LogicExpressionExtended.AND_SEPARATOR).join(tempFormulaList)})"
            )

        return (
            LogicExpressionExtended.AND_SEPARATOR
            if isCNF
            else LogicExpressionExtended.OR_SEPARATOR
        ).join(formulas)

    @staticmethod
    def minimizeExpression(exp: str, isCNF=False):
        variables = LogicExpressionExtended._variables(exp)

        carnoTable = LogicExpressionExtended.makeCarnoTable(exp)

        groups = LogicExpressionExtended.findGroups(exp, carnoTable, isCNF)

        formula = LogicExpressionExtended.buildFormulaFromGroups(
            groups, variables, isCNF
        )

        result = (
            LogicExpressionExtended.cnfWithQuine(exp, False)
            if isCNF
            else LogicExpressionExtended.dnfWithQuine(exp)
        )

        if isCNF:
            result = LogicExpressionExtended.AND_SEPARATOR.join(
                set(result.split(LogicExpressionExtended.AND_SEPARATOR))
            )
        else:
            result = LogicExpressionExtended.OR_SEPARATOR.join(
                set(result.split(LogicExpressionExtended.OR_SEPARATOR))
            )

        return result

    @staticmethod
    def findRectangleGroups(
        carnoTable: List[List[int]],
        maxGroupSize: int,
        grayHorizontal: List[str],
        grayVertical: List[str],
        isCNF=False,
    ):
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
                if height > rows or width > cols:
                    continue

                # Проверяем все возможные позиции с учётом тороидальности
                for i in range(rows):
                    for j in range(cols):
                        all_correct = True
                        current_group = []

                        # Проверяем каждый пиксель в прямоугольнике
                        for di in range(height):
                            for dj in range(width):
                                # Тороидальные координаты
                                x = (i + di) % rows
                                y = (j + dj) % cols

                                # Проверка значения
                                if (carnoTable[x][y] != 1 and not isCNF) or (
                                    carnoTable[x][y] != 0 and isCNF
                                ):
                                    all_correct = False
                                    break

                                # Добавляем переменную
                                var = grayVertical[x] + grayHorizontal[y]
                                current_group.append(var)

                            if not all_correct:
                                break

                        # Добавляем группу, если она валидна и содержит новые переменные
                        if all_correct:
                            new_vars = [
                                var for var in current_group if var not in visited
                            ]
                            if new_vars:
                                groups.append(current_group)
                                visited.update(new_vars)

        # Оптимизация: объединяем смежные группы
        merged_groups = []
        for group in groups:
            merged = False
            for i, merged_group in enumerate(merged_groups):
                if set(group).issubset(set(merged_group)):
                    merged = True
                    break
                if set(merged_group).issubset(set(group)):
                    merged_groups[i] = group
                    merged = True
                    break
            if not merged:
                merged_groups.append(group)

        return merged_groups

    @staticmethod
    def findGroups(exp: str, carnoTable: str, isCNF=False):
        carnoTableExtended = [row * 2 for row in carnoTable]
        carnoTableExtended *= 2

        variables = LogicExpressionExtended._variables(exp)
        variablesCount = len(variables)

        grayHorizontal = LogicExpressionExtended.generateGray(
            variablesCount // 2 + (variablesCount % 2)
        )
        grayHorizontal = ["".join(code) for code in grayHorizontal]

        grayVertical = LogicExpressionExtended.generateGray(variablesCount // 2)
        grayVertical = ["".join(code) for code in grayVertical]

        groups = []

        maxGroupSize = 2 ** (variablesCount - 1)

        groups.extend(
            LogicExpressionExtended.findRectangleGroups(
                carnoTable, maxGroupSize, grayHorizontal, grayVertical, isCNF
            )
        )

        return groups

    @staticmethod
    def makeCarnoTable(exp: str):
        variables = LogicExpressionExtended._variables(exp)
        variablesCount = len(variables)

        grayHorizontal = LogicExpressionExtended.generateGray(
            variablesCount // 2 + (variablesCount % 2)
        )
        grayHorizontal = ["".join(code) for code in grayHorizontal]

        grayVertical = LogicExpressionExtended.generateGray(variablesCount // 2)
        grayVertical = ["".join(code) for code in grayVertical]

        carnoTable = [0] * len(grayVertical)

        carnoTable = [[0] * len(grayHorizontal) for _ in carnoTable]

        for i in range(len(grayVertical)):
            for j in range(len(grayHorizontal)):
                carnoTable[i][j] = LogicExpressionExtended.result(
                    exp, *grayVertical[i], *grayHorizontal[j]
                )

        return carnoTable

    @staticmethod
    def cnfWithCarno(exp: str):
        return LogicExpressionExtended.minimizeExpression(exp, True)

    @staticmethod
    def dnfWithCarno(exp: str):
        return LogicExpressionExtended.minimizeExpression(exp)


# formula = input("Введи формулу: ")
# print("СКНФ:", LogicExpression.buildCNF(formula))
# print("СДНФ:", LogicExpression.buildDNF(formula))
# print("-" * 40, "\nМинимизация СДНФ по квейну (рассчётный)")
# print(LogicExpressionExtended.dnfWithQuine(formula, "расчётный"))
# print("-" * 40, "\nМинимизация СКНФ по квейну (рассчётный)")
# print(LogicExpressionExtended.cnfWithQuine(formula, "расчётный"))
# print("-" * 40, "\nМинимизация СДНФ по квейну (табл-рассчётный)")
# print(LogicExpressionExtended.dnfWithQuine(formula, "таблично-расчётный"))
# print("-" * 40, "\nМинимизация СКНФ по квейну (табл-рассчётный)")
# print(LogicExpressionExtended.cnfWithQuine(formula, "таблично-расчётный"))
# print("-" * 40, "\nМинимизация СДНФ по карно")
# print(LogicExpressionExtended.dnfWithCarno(formula))
# print("-" * 40, "\nМинимизация СКНФ по карно")
# print(LogicExpressionExtended.cnfWithCarno(formula))
