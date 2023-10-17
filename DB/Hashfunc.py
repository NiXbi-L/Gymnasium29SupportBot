import hashlib
import random
import string
from DB import DBfunc
def passhashing(password):
    return hashlib.sha256(password.encode()).hexdigest()

async def generate_unique_key(length=8):
    while True:
        # Генерируем случайную строку указанной длины
        key = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

        # Проверяем, не был ли этот ключ уже использован
        if not(await DBfunc.IF('student', '*', f'`user key` = "{key}"')):
            return key