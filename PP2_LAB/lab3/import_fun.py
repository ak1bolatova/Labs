from lab3.functions import convert, convertf_c, solve, permutations, reverse, is_3, is_007, volume, un, pal, histogram
# Пример вызова функций
print(convert(100))  # Конвертация 100 граммов в унции
print(convertf_c(32))  # Конвертация 32°F в °C
print(solve(35, 94))  # Решение задачи о головах и ногах
print(permutations([1, 2, 3]))  # Перестановки списка [1, 2, 3]
print(reverse("Hello World"))  # Разворот строки
print(is_3([1, 3, 3, 4]))  # Проверка на две тройки подряд
print(is_007([0, 0, 7, 1]))  # Проверка на последовательность 0, 0, 7
print(volume(5))  # Объем сферы с радиусом 5
print(un([1, 2, 2, 3, 3, 3]))  # Уникальные элементы списка
print(pal("madam"))  # Проверка, является ли строка палиндромом
histogram([4, 9, 7])  # Гистограмма из звездочек