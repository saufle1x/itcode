#Задача Калькулятор 1

# Виводимо меню для користувача

print("Калькулятор:")
print("Оберіть операцію: +, -, *, /")

# Отримуємо операцію від користувача

operation = input("Введіть операцію: ")

# Запитуємо в користувача перше та друге число

num1 = float(input("Введіть перше число: "))
num2 = float(input("Введіть друге число: "))

# Виконуємо відповідну операцію на основі введення користувача

if operation == "+":
    result = num1 + num2
    print(f"Результат: {num1} + {num2} = {result}")
    
elif operation == '-':
    result = num1 + num2
    print(f"Результат: {num1} - {num2} = {result}")

elif operation == '*':
    result = num1 * num2
    print(f"Результат: {num1} * {num2} = {result}")
    
elif operation == "/":
    if num2 == 0:
            print("Помилка: ділення на нуль неможливе!")
    else:
        result = num1 / num2
        print(f"Результат: {num1} / {num2} = {result}")
else:
    # Якщо введено невірний символ операції
    print("Невірний вибір операції. Спробуйте ще раз!")
    
    

#Задача "Дискримінант" 2

# Введення коефіцієнтів квадратного рівняння
a = float(input("Введіть коефіцієнт a: "))
b = float(input("Введіть коефіцієнт b: "))
c = float(input("Введіть коефіцієнт c: "))

# Обчислення дискримінанту

D = b**2 - 4 * a * c

# Перевірка значень дискримінанту

if D > 0:
    x1 = (-b + D**0.5) / (2*a)
    x2 = (-b - D**0.5) / (2*a)
    print(f"Дискрімінант: {D}")
    print(f"Рівняння має два корені: x1 = {x1} і x2 = {x2}")
        
elif D == 0:
    x = -b / (2*a)
    print(f"Дискрімінант: {D}")
    print(f"Рівняння має один корінь: x = {x}")
        
else:
    print(f"Дискрімінант: {D}")
    print("Рівняння не має дійсних коренів")


#Задача "Сума квадратів числа" 3

# Введення двох чисел

num1 = float(input("Введіть перше число: "))
num2 = float(input("Введіть друге число: "))

# Обчислення суми квадратів та суми чисел

sum_of_squares = num1**2 + num2**2
sum_of_numbers = num1 + num2

# Порівняння та виведення результату
if sum_of_squares > sum_of_numbers:
    print("Сума квадратів більша за суму чисел")
elif sum_of_squares < sum_of_numbers:
    print("Сума чисел більша за суму квадратів")
else:
    print("Сума квадратів дорівнює сумі чисел")

#Задача "Максимальне число" 4

# Введення трьох чисел

num1 = float(input("Введіть перше число: "))
num2 = float(input("Введіть друге число: "))
num3 = float(input("Введіть третє число: "))

# Пошук найбільшого числа
if num1 >= num2 and num1 >= num3:
    maximum = num1
elif num2 >= num1 and num2 >= num3:
    maximum = num2
else:
    maximum = num3

# Виведення результатів
print(f"Найбільше число: {maximum}")

#Задача "Успішність студента" 5

# Запитуємо оцінки у студента

mark1 = int(input("Введіть оцінку за перший предмет: "))
mark2 = int(input("Введіть оцінку за другий предмет: "))
mark3 = int(input("Введіть оцінку за третій предмет: "))
mark4 = int(input("Введіть оцінку за четвертий предмет: "))
mark5 = int(input("Введіть оцінку за п'ятий предмет: "))

# Обчислюємо середній бал студента

average = (mark1 + mark2 + mark3 + mark4 + mark5) / 5

# Визначаємо успішність

if average >= 10:
    print("Відмінно!")
elif 7 <= average <= 9:
    print("Добре!")
elif 4 <= average <= 6:
    print("Задовільно!")
else:
    print("Незадовільно!")
    
#Задача "Знак зодіаку" 6

# Запитуємо місяць і день народження у користувача

month = int(input("Введіть місяць Вашого народження (1-12): "))
day = int(input("Введіть день Вашого народження: "))

if (month == 3 and day >= 21) or (month == 4 and day <= 19):
    zodiac = "Овен"
elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
    zodiac = "Телець"
elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
    zodiac = "Близнюки"
elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
    zodiac = "Рак"
elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
    zodiac = "Лев"
elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
    zodiac = "Діва"
elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
        zodiac = "Терези"
elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
    zodiac = "Скорпіон"
elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
    zodiac = "Стрілець"
elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
    zodiac = "Козеріг"
elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
    zodiac = "Водолій"
elif (month == 2 and day >= 19) or (month == 3 and day <= 20):
    zodiac = "Риби"
else:
    zodiac = None

# Виводимо результат

if zodiac:
    print(f"Ваш знак зодіаку: {zodiac}")
else:
    print("Невірно введена дата народження. Будь ласка, спробуйте ще раз.")
