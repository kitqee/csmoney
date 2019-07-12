import random
import string


def generate_code(length):
    code = [random.SystemRandom().choice(string.digits) for _ in range(length)]
    return ''.join(code)
