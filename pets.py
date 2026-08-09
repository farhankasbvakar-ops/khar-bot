import random
import time

CARROTS = {
    "معمولی": {
        "value": 1,
        "chance": 75
    },
    "بزرگ": {
        "value": 1.5,
        "chance": 18
    },
    "طلایی": {
        "value": 2,
        "chance": 6
    },
    "افسانه‌ای": {
        "value": 3,
        "chance": 1
    }
}


def find_carrot(hook_level=1):
    roll = random.uniform(0, 100)

    bonus = min((hook_level - 1) * 0.5, 5)

    if roll <= 1 + bonus:
        return "افسانه‌ای"

    if roll <= 7 + bonus:
        return "طلایی"

    if roll <= 25 + bonus:
        return "بزرگ"

    return "معمولی"


def carrot_value(name):
    return CARROTS[name]["value"]


def pet_income(pet_level, food):
    if food <= 0:
        return 0

    return min(1 + pet_level * 2, 100)


def pet_upgrade_cost(level):
    return 500 * level


def rename_cost(level):
    return 1000 + (level * 500)
