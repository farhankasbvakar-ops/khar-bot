BUILDINGS = {
    "شهربازی": 10000,
    "کازینو": 25000,
    "مرکز خرید": 50000,
    "استادیوم": 100000,
    "فرودگاه": 250000
}


def building_cost(name):
    return BUILDINGS.get(name, 0)


def jail_job_income(job):
    jobs = {
        "معدنچی": 80,
        "کشاورز": 60,
        "کارگر": 100,
        "رفتگر": 40,
        "تعمیرکار": 120,
        "راننده": 90
    }

    return jobs.get(job, 40)


def rescue_cost(attempt):
    costs = {
        1: 200,
        2: 300,
        3: 400
    }

    return costs.get(attempt, 400)
