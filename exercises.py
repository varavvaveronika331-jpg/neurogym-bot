import random

def sequence(level):
    length = 4 + level
    return [random.randint(1, 9) for _ in range(length)]
