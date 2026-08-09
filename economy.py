LEVEL_REQUIREMENTS = {
    1: 0,
    2: 50,
    3: 100,
    4: 175,
    5: 275,
    6: 400,
    7: 525,
    8: 650,
    9: 700,
    10: 750,
    11: 800,

    12: 900,
    13: 1050,
    14: 1250,
    15: 1500,
    16: 1800,
    17: 2150,
    18: 2550,
    19: 3000,
    20: 3500,

    21: 4100,
    22: 4800,
    23: 5600,
    24: 6500,
    25: 7500,
    26: 8600,
    27: 9800,
    28: 11100,
    29: 12500,
    30: 14000,

    31: 15750,
    32: 17500,
    33: 19500,
    34: 21750,
    35: 24000,
    36: 26500,
    37: 29250,
    38: 32000,
    39: 35000,
    40: 38500,

    41: 42500,
    42: 47000,
    43: 52000,
    44: 57500,
    45: 63500,
    46: 70000,
    47: 77000,
    48: 84500,
    49: 92500,
    50: 101000
}


def calculate_level(total_aar):
    level = 1

    for current_level, required in LEVEL_REQUIREMENTS.items():
        if total_aar >= required:
            level = current_level
        else:
            break

    return level


def level_progress(total_aar):
    level = calculate_level(total_aar)

    if level >= max(LEVEL_REQUIREMENTS):
        return level, total_aar, total_aar

    current_required = LEVEL_REQUIREMENTS[level]
    next_required = LEVEL_REQUIREMENTS[level + 1]

    current_progress = total_aar - current_required
    required_progress = next_required - current_required

    return level, current_progress, required_progress


def level_text(total_aar):
    level = calculate_level(total_aar)

    if level >= max(LEVEL_REQUIREMENTS):
        return f"سطح {level}🌟: MAX"

    _, current, required = level_progress(total_aar)

    return f"سطح {level}🌟: {current}/{required}"


def get_level_requirement(level):
    return LEVEL_REQUIREMENTS.get(level)


def get_next_level_requirement(total_aar):
    level = calculate_level(total_aar)

    if level >= max(LEVEL_REQUIREMENTS):
        return None

    return LEVEL_REQUIREMENTS[level + 1]


def aar_reward(level):
    return 10 + (level * 3)


def pet_hourly_income(pet_level):
    return min(1 + (pet_level * 2), 100)


def transfer_allowed(level):
    return level >= 2


def get_level_reward(level):
    rewards = {
        2: "💸 انتقال عر کوین",
        3: "🪝 قلاب هویج سطح 2",
        4: "💼 شغل‌های بیشتر",
        5: "🏴 قاچاق خر",
        6: "🏭 کارخانه",
        7: "🫏 کره‌خر خیابانی",
        8: "🏭 ارتقای کارخانه",
        9: "🎮 بازی‌های ویژه",
        10: "🏙️ امکانات شهر",
        11: "🔓 قابلیت‌های پیشرفته",
        12: "🪙 درآمد بیشتر",
        13: "🫏 قابلیت‌های پیشرفته کره‌خر",
        14: "🏭 کارخانه پیشرفته",
        15: "🏙️ امکانات ویژه شهر",
        20: "👑 امکانات ویژه",
        30: "🔥 قابلیت‌های بسیار ویژه",
        40: "💎 قابلیت‌های نادر",
        50: "👑 سطح افسانه‌ای"
    }

    return rewards.get(level, "🔓 قابلیت جدید")
