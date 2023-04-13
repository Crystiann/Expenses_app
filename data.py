from datetime import datetime
import calendar

DB_NAME = "db_expenses"
TABLE = "expenses"

DATE = datetime.now()
TODAY_TIME = DATE.strftime("%H:%M")
TODAY_DATE = DATE.strftime("%d-%m-%Y")
TODAY_NAME = DATE.strftime("%A")
TODAY_NUMBER = DATE.strftime("%-d")
MONTH = DATE.strftime("%-m")
MONTH_NAME = DATE.strftime("%B")
YEAR = DATE.strftime("%Y")

FIXED = {
    "RENT": 975,
    "GYM": 60,
    "HEALTH INSURANCE": 136,
    "PHONE": 44,
    "CLEANING": 0,
    "SUBSCRIPTIONS": 3
}

NOT_FIXED = ["FOOD", "HEALTH", "ACCESSORIES", "RELAXATION", "OTHERS"]

"""Use for test importing data from excel"""

expenses_list = []
for n in FIXED.items():
    expenses_list.append([n[1], n[0], "FIXED", "", TODAY_DATE, MONTH, MONTH_NAME, YEAR])

month_dict = {}
for n in range(1, 13):
    month_dict[n] = calendar.month_name[n]


if __name__ == "__main__":
    # print(TODAY_NUMBER)
    # print(TODAY_DATE)
    # print(TODAY_NAME)
    # print(MONTH)
    # print(MONTH_NAME)
    # print(fixed_categories[2][0])

    # print(TODAY_TIME)
    # print(TODAY_DATE)
    # print(MONTH)
    # print(TODAY_NUMBER)
    print(expenses_list)
    # print(not_fixed_expenses)
    print(datetime.strptime("7", "%m").strftime("%B"))
    print(TODAY_DATE)
    print(DATE.strftime("%B"))
    print("12-11-2022".split("-")[1])
    print(month_dict)
