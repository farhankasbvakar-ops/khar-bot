import random


def carrot_game(hook_level=1):
    roll = random.randint(1, 100)

    bonus = min(hook_level - 1, 5)

    if roll <= 1 + bonus:
        return "افسانه‌ای", 3

    if roll <= 7 + bonus:
        return "طلایی", 2

    if roll <= 25 + bonus:
        return "بزرگ", 1.5

    return "معمولی", 1


def smuggle():
    chance = random.randint(1, 100)

    if chance <= 65:
        reward = random.randint(1000, 5000)
        return "موفق", reward

    if chance <= 85:
        reward = random.randint(200, 1000)
        return "نیمه‌موفق", reward

    return "دستگیر", 0


def rescue():
    chance = random.randint(1, 100)

    if chance <= 60:
        return "موفق"

    if chance <= 85:
        return "فرار کرد"

    return "مرد"
