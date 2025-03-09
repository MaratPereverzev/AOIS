def find_groups(grid, forCnf: bool):
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    groups = []
    used = [[False] * cols for _ in range(rows)]  # Отмечаем уже покрытые ячейки
    
    def can_form_group(start_i, start_j, height, width, direction):
        """Проверяет, можно ли сформировать группу размера height x width, начиная с (start_i, start_j) в направлении direction."""
        for x in range(height):
            for y in range(width):
                # Определяем координаты ячейки в зависимости от направления
                if direction == "top_left":
                    row = (start_i + x) % rows
                    col = (start_j + y) % cols
                elif direction == "top_right":
                    row = (start_i + x) % rows
                    col = (start_j - y) % cols
                elif direction == "bottom_left":
                    row = (start_i - x) % rows
                    col = (start_j + y) % cols
                elif direction == "bottom_right":
                    row = (start_i - x) % rows
                    col = (start_j - y) % cols
                # Проверяем значение ячейки
                if forCnf:
                    # Для СКНФ ищем группы из 0
                    if grid[row][col] != 0 or used[row][col]:
                        return False
                else:
                    # Для СДНФ ищем группы из 1
                    if grid[row][col] != 1 or used[row][col]:
                        return False
        return True
    
    def mark_used(start_i, start_j, height, width, direction):
        """Помечает ячейки в группе как использованные."""
        for x in range(height):
            for y in range(width):
                # Определяем координаты ячейки в зависимости от направления
                if direction == "top_left":
                    row = (start_i + x) % rows
                    col = (start_j + y) % cols
                elif direction == "top_right":
                    row = (start_i + x) % rows
                    col = (start_j - y) % cols
                elif direction == "bottom_left":
                    row = (start_i - x) % rows
                    col = (start_j + y) % cols
                elif direction == "bottom_right":
                    row = (start_i - x) % rows
                    col = (start_j - y) % cols
                used[row][col] = True
    
    def get_possible_sizes(max_height, max_width):
        """Возвращает возможные размеры групп, отсортированные по убыванию площади."""
        sizes = set()
        size = 1
        while size <= max(max_height, max_width):
            if size <= max_height and size <= max_width:
                sizes.add((size, size))  # Квадратные группы
            if size <= max_height:
                sizes.add((size, 1))  # Вертикальные группы
            if size <= max_width:
                sizes.add((1, size))  # Горизонтальные группы
            size *= 2
        return sorted(sizes, key=lambda x: x[0] * x[1], reverse=True)  # Сортируем по убыванию площади
    
    possible_sizes = get_possible_sizes(rows, cols)
    
    # Проходим по каждой ячейке
    for i in range(rows):
        for j in range(cols):
            if forCnf:
                # Для СКНФ ищем группы из 0
                if grid[i][j] == 0 and not used[i][j]:
                    # Ищем наибольшую группу для этой ячейки
                    best_group = None
                    best_size = 0
                    # Проверяем все возможные направления
                    for direction in ["top_left", "top_right", "bottom_left", "bottom_right"]:
                        for height, width in possible_sizes:
                            if can_form_group(i, j, height, width, direction):
                                group_size = height * width
                                if group_size > best_size:
                                    best_size = group_size
                                    best_group = (i, j, height, width, direction)
                    # Если группа найдена, добавляем её и помечаем ячейки как использованные
                    if best_group:
                        i_, j_, height, width, direction = best_group
                        groups.append((i_, j_, height, width))
                        mark_used(i_, j_, height, width, direction)
            else:
                # Для СДНФ ищем группы из 1
                if grid[i][j] == 1 and not used[i][j]:
                    # Ищем наибольшую группу для этой ячейки
                    best_group = None
                    best_size = 0
                    # Проверяем все возможные направления
                    for direction in ["top_left", "top_right", "bottom_left", "bottom_right"]:
                        for height, width in possible_sizes:
                            if can_form_group(i, j, height, width, direction):
                                group_size = height * width
                                if group_size > best_size:
                                    best_size = group_size
                                    best_group = (i, j, height, width, direction)
                    # Если группа найдена, добавляем её и помечаем ячейки как использованные
                    if best_group:
                        i_, j_, height, width, direction = best_group
                        groups.append((i_, j_, height, width))
                        mark_used(i_, j_, height, width, direction)
    
    return groups

def get_variable_name(row, col, rows, cols):
    """Возвращает имя переменной для данной ячейки."""
    variables = []
    if rows > 1:
        variables.append(f"x{row}")
    if cols > 1:
        variables.append(f"y{col}")
    return "".join(variables)

def build_sdnf(groups, grid):
    """Строит минимизированную СДНФ на основе групп."""
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    sdnf_terms = []
    
    for group in groups:
        i, j, height, width = group
        terms = []
        # Определяем, какие переменные постоянны в группе
        for x in range(i, i + height):
            for y in range(j, j + width):
                row = x % rows
                col = y % cols
                if grid[row][col] == 1:
                    var_name = get_variable_name(row, col, rows, cols)
                    terms.append(var_name)
        # Убираем дубликаты и сортируем
        terms = sorted(set(terms))
        sdnf_terms.append(" & ".join(terms))
    
    return " | ".join(f"({term})" for term in sdnf_terms)

def build_sknf(groups, grid):
    """Строит минимизированную СКНФ на основе групп."""
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    sknf_terms = []
    
    for group in groups:
        i, j, height, width = group
        terms = []
        # Определяем, какие переменные постоянны в группе
        for x in range(i, i + height):
            for y in range(j, j + width):
                row = x % rows
                col = y % cols
                if grid[row][col] == 0:
                    var_name = get_variable_name(row, col, rows, cols)
                    terms.append(f"!{var_name}")
        # Убираем дубликаты и сортируем
        terms = sorted(set(terms))
        sknf_terms.append(" | ".join(terms))
    
    return " & ".join(f"({term})" for term in sknf_terms)

# Пример сетки
grid = [
    [0, 0, 1, 0],
    [0, 1, 1, 0],
]

# Поиск групп для СДНФ (группы из 1)
groups_sdnf = find_groups(grid, forCnf=False)
print("Группы для СДНФ:", groups_sdnf)

# Поиск групп для СКНФ (группы из 0)
groups_sknf = find_groups(grid, forCnf=True)
print("Группы для СКНФ:", groups_sknf)