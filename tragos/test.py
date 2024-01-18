import re

message = "10.12.1990"
pattern = r"(\d{2}\.\d{2}\.\d{4})\s*(\d{1,2})?"

match = re.search(pattern, message)

if match:
    birth_date = match.group(1)
    birth_time = match.group(2) if match.group(2) else None

    print(f"Дата рождения: {birth_date}")
    print(f"Время рождения: {birth_time}" if birth_time else "Время рождения не указано")
else:
    print("Дата рождения не найдена в сообщении.")
