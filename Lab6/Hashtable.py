class HashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [None] * self.size
        self.deleted = object()  # Маркер для удаленных элементов

    def hash1(self, key):
        # Первая хеш-функция (простое хеширование)
        return hash(key) % self.size

    def hash2(self, key):
        # Вторая хеш-функция (должна возвращать значение, взаимно простое с size)
        # Используем простое число меньше размера таблицы
        return 1 + (hash(key) % (self.size - 1))

    def insert(self, key, value):
        index = self.hash1(key)
        step = self.hash2(key)
        
        # Поиск свободного места
        for _ in range(self.size):
            if self.table[index] is None or self.table[index] is self.deleted:
                self.table[index] = (key, value)
                return
            index = (index + step) % self.size
        
        # Если таблица заполнена, увеличиваем ее размер
        self.resize()
        self.insert(key, value)

    def search(self, key):
        index = self.hash1(key)
        step = self.hash2(key)
        
        for _ in range(self.size):
            item = self.table[index]
            if item is None:
                return None
            elif item is not self.deleted and item[0] == key:
                return item[1]
            index = (index + step) % self.size
        
        return None

    def delete(self, key):
        index = self.hash1(key)
        step = self.hash2(key)
        
        for _ in range(self.size):
            item = self.table[index]
            if item is None:
                return
            elif item is not self.deleted and item[0] == key:
                self.table[index] = self.deleted
                return
            index = (index + step) % self.size

    def resize(self):
        # Увеличиваем размер таблицы и перехешируем все элементы
        old_table = self.table
        self.size *= 2
        self.table = [None] * self.size
        
        for item in old_table:
            if item is not None and item is not self.deleted:
                self.insert(item[0], item[1])

    def __str__(self):
        result = []
        for i, item in enumerate(self.table):
            if item is None:
                result.append(f"{i}: None")
            elif item is self.deleted:
                result.append(f"{i}: <deleted>")
            else:
                result.append(f"{i}: {item[0]} -> {item[1]}")
        return "\n".join(result)