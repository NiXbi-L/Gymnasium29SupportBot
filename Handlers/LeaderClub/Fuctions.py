async def day(num):
    if num % 10 == 1 and num % 100 != 11:
        return f'{num} день'
    elif 2 <= num % 10 <= 4 and (num % 100 < 10 or num % 100 >= 20):
        return f'{num} дня'
    else:
        return f'{num} дней'