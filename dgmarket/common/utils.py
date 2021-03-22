import random
import string

def generate_random_key(length=10):
    result = ""
    for i in range(length):
        result += random.choice(string.ascii_letters + string.digits)
    return result