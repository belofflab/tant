def lizard_existence_days_seconds(start, end):
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    year1, month1, day1, hour1, min1, sec1 = map(int, start.split())
    year2, month2, day2, hour2, min2, sec2 = map(int, end.split())

    # Коррекция индексов для массива дней в месяце
    month1 -= 1
    month2 -= 1

    full_years = year2 - year1 - 1

    # Рассчитываем количество полных дней в первом и последнем году
    days_first_year = sum(days_in_month[month1:]) - day1
    days_last_year = sum(days_in_month[:month2]) + day2

    total_days = full_years * 365 + days_first_year + days_last_year

    seconds_in_partial_day = (hour2 * 3600 + min2 * 60 + sec2) - (hour1 * 3600 + min1 * 60 + sec1)

    return total_days, seconds_in_partial_day

start_date = input()
end_date = input()

result = lizard_existence_days_seconds(start_date, end_date)
print(result[0], result[1])
