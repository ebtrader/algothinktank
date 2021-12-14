from datetime import date, timedelta

# https://stackoverflow.com/questions/6558535/find-the-date-for-the-first-monday-after-a-given-date

def next_weekday(weekday):
    d = date.today()
    days_ahead = weekday - d.weekday()

    if days_ahead < 0:  # target day already happened this week also try <=
        days_ahead += 7

    return d + timedelta(days_ahead)

next_monday = next_weekday(0)  # 0=Mon, 1=Tues, 2=Wed, 3=Thu, 4=Fri
year = next_monday.year
month = next_monday.month
day = next_monday.day
print(next_monday)
print(year)
print(month)
print(day)

