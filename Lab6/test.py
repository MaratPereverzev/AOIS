import unittest
from unittest import TestCase
from Lab6.Hashtable import HashTable

class TestHashTable(TestCase):
    def setUp(self):
        self.ht = HashTable(size=5)  # Используем небольшой размер для тестирования коллизий

    def test_insert_and_search(self):
        # Проверка вставки и поиска
        self.ht.insert("key1", "value1")
        self.ht.insert("key2", "value2")
        self.assertEqual(self.ht.search("key1"), "value1")
        self.assertEqual(self.ht.search("key2"), "value2")
        self.assertIsNone(self.ht.search("nonexistent"))

    def test_delete(self):
        # Проверка удаления
        self.ht.insert("key1", "value1")
        self.ht.insert("key2", "value2")
        self.ht.delete("key1")
        self.assertIsNone(self.ht.search("key1"))
        self.assertEqual(self.ht.search("key2"), "value2")

    def test_collision_handling(self):
        # Проверка обработки коллизий
        # Подберем ключи, которые дают одинаковый hash1, но разные hash2
        # Для этого нужно знать реализацию hash1 и hash2
        # В данном случае используем фиксированные ключи, которые могут вызвать коллизию
        self.ht.insert("key1", "value1")
        self.ht.insert("key6", "value6")  # Предположим, что hash1("key1") == hash1("key6")
        self.assertEqual(self.ht.search("key1"), "value1")
        self.assertEqual(self.ht.search("key6"), "value6")

    def test_resize(self):
        # Проверка увеличения размера таблицы
        initial_size = self.ht.size
        for i in range(initial_size + 1):  # Вставляем на один элемент больше, чем размер таблицы
            self.ht.insert(f"key{i}", f"value{i}")
        self.assertGreater(self.ht.size, initial_size)
        for i in range(initial_size + 1):
            self.assertEqual(self.ht.search(f"key{i}"), f"value{i}")

    def test_delete_nonexistent(self):
        # Проверка удаления несуществующего ключа
        self.ht.insert("key1", "value1")
        self.ht.delete("nonexistent")  # Не должно вызывать ошибок
        self.assertEqual(self.ht.search("key1"), "value1")

    def test_reinsert_after_delete(self):
        # Проверка повторной вставки после удаления
        self.ht.insert("key1", "value1")
        self.ht.delete("key1")
        self.ht.insert("key1", "new_value1")
        self.assertEqual(self.ht.search("key1"), "new_value1")

    def test_str_representation(self):
        # Проверка строкового представления
        self.ht.insert("key1", "value1")
        self.ht.insert("key2", "value2")
        self.ht.delete("key1")
        str_repr = str(self.ht)
        self.assertIn("key2 -> value2", str_repr)
        self.assertIn("<deleted>", str_repr)

if __name__ == '__main__':
    unittest.main()