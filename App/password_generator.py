import random
import string


def generate_password(length=12, numbers=True, symbols=True, uppercase=True):
    lower_case = "abcdefghijklmnopqrstuvwxyz"
    upper_case = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    digits = "0123456789"
    punctuation = "!@#$%^&*()_+-=[]{}|;:,.<>?/"
    
    characters = lower_case
    if uppercase:
        characters += upper_case
    if numbers:
        characters += digits
    if symbols:
        characters += punctuation  
    
    password = ""
    for i in range(length):
        password += random.choice(characters)
    
    return password










