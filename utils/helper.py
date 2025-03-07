import random
import string

def generate_random_username(initial=None):
    return f"{initial}" + "".join(random.choices(string.ascii_lowercase + string.digits, k=12))
