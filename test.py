input_numbers = input("Введите числа через пробел: ").split(" ")
number_list = []

for input_number in input_numbers:
    number_list.append(int(input_number))

numbers_sum = 0
for number in number_list:
    numbers_sum += number * number

print(numbers_sum)
