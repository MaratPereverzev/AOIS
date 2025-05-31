from typing import List


from typing import List


class DiagonalMatrix:
    SIZE: int = 16        
    V_LEN: int = 3        
    A_LEN: int = 4        
    B_LEN: int = 4        
    S_LEN: int = 5        
    WORD_LEN: int = V_LEN + A_LEN + B_LEN + S_LEN

    def __init__(self, matrix: List[List[int]]):
        if len(matrix) != self.SIZE or any(len(row) != self.SIZE for row in matrix):
            raise ValueError(f"Матрица должна быть размером {self.SIZE}x{self.SIZE}")
        self.matrix = matrix

    def get_word(self, index: int) -> List[int]:
        return [self.matrix[(i + index) % self.SIZE][i] for i in range(self.SIZE)]

    def get_column(self, index: int) -> List[int]:
        return [row[index] for row in self.matrix]

    def write_word(self, index: int, word: List[int]):
        for i in range(self.SIZE):
            self.matrix[(i + index) % self.SIZE][i] = word[i]

    def logical_f1(self, w1: List[int], w2: List[int]) -> List[int]:
        return [a & b for a, b in zip(w1, w2)]

    def logical_f3(self, w1: List[int], w2: List[int]) -> List[int]:
        return [a ^ b for a, b in zip(w1, w2)]

    def logical_f12(self, w1: List[int], w2: List[int]) -> List[int]:
        return [(~a & b) & 1 for a, b in zip(w1, w2)]

    def logical_f14(self, w1: List[int], w2: List[int]) -> List[int]:
        return [~a & 1 for a in w1]

    def add_fields(self, v_key: str):
        for j in range(self.SIZE):
            word = self.get_word(j)
            v = ''.join(map(str, word[:self.V_LEN]))
            if v == v_key:
                a_start = self.V_LEN
                b_start = self.V_LEN + self.A_LEN
                s_start = self.V_LEN + self.A_LEN + self.B_LEN

                a = int(''.join(map(str, word[a_start:b_start])), 2)
                b = int(''.join(map(str, word[b_start:s_start])), 2)
                s = a + b
                s_bits = list(map(int, format(s % (1 << self.S_LEN), f'0{self.S_LEN}b')))
                word[s_start:s_start + self.S_LEN] = s_bits
                self.write_word(j, word)

    def print_matrix(self):
        print("matrix")
        print(self.matrix)
        for row in self.matrix:
            print(''.join(str(bit) for bit in row))

    def compare_bits_gl(self, word_bits: List[int], target_bits: List[int]) -> str:
        g = [int(tb > wb) for tb, wb in zip(target_bits, word_bits)]
        l = [int(tb < wb) for tb, wb in zip(target_bits, word_bits)]

        g_and_not_l = [gi & (1 - li) for gi, li in zip(g, l)]
        l_and_not_g = [li & (1 - gi) for gi, li in zip(g, l)]

        if any(g_and_not_l):
            return "target_greater"
        elif any(l_and_not_g):
            return "target_less"
        else:
            return "equal"

    def find_nearest_down(self, target: List[int]) -> int:
        best_index = -1
        best_value = None
        for i in range(self.SIZE):
            word = self.get_word(i)
            cmp = self.compare_bits_gl(word, target)
            if cmp == "target_greater":
                if best_value is None or word > best_value:
                    best_value = word
                    best_index = i
        return best_index

    def find_nearest_up(self, target: List[int]) -> int:
        best_index = -1
        best_value = None
        for i in range(self.SIZE):
            word = self.get_word(i)
            cmp = self.compare_bits_gl(word, target)
            if cmp == "target_less":
                if best_value is None or word < best_value:
                    best_value = word
                    best_index = i
        return best_index




# Пример использования
if __name__ == "__main__":
    import copy

    matrix_16x16 = [
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

    dm = DiagonalMatrix(copy.deepcopy(matrix_16x16))
    print("Слово #2:", ''.join(map(str, dm.get_word(2))))
    print("Адресный столбец #3:", ''.join(map(str, dm.get_column(3))))
    w2 = dm.get_word(2)
    w3 = dm.get_word(3)
    f1_result = dm.logical_f1(w2, w3)
    dm.write_word(15, f1_result)
    print("Результат F1 записан в слово #15")
    dm.add_fields("111")
    print("После сложения полей A и B (если V = 111):")
    dm.print_matrix()

    target_word = [0,0,1,1,1,0,0,0,0,0,0,1,0,0,0,0]
    index_down = dm.find_nearest_down(target_word)
    index_up = dm.find_nearest_up(target_word)

    print(f"Ближайшее снизу: слово #{index_down} -> {''.join(map(str, dm.get_word(index_down)))}")
    print(f"Ближайшее сверху: слово #{index_up} -> {''.join(map(str, dm.get_word(index_up)))}")
