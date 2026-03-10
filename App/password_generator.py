import random
import string


def generate_password(length=12, numbers=True, symbols=True, uppercase=True):
    chars = string.ascii_lowercase
    if uppercase:
        chars += string.ascii_uppercase
    if numbers:
        chars += string.digits
    if symbols:
        chars += string.punctuation

    if not chars:
        chars = string.ascii_lowercase

    return ''.join(random.choice(chars) for _ in range(length))
