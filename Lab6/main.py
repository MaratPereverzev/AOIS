from Lab6.Hashtable import HashTable

ht = HashTable(size=5)

ht.insert("apple", 10)
ht.insert("banana", 20)
ht.insert("orange", 30)
ht.insert("grape", 40)
ht.insert("melon", 50)
ht.insert("kiwi", 60)  # Вызовет resize

print("Таблица после вставки:")
print(ht)

print("\nПоиск 'banana':", ht.search("banana"))
print("Поиск 'mango':", ht.search("mango"))

ht.delete("banana")
print("\nТаблица после удаления 'banana':")
print(ht)

print("\nПопытка поиска удаленного 'banana':", ht.search("banana"))