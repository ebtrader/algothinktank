from datetime import date, timedelta

# https://stackoverflow.com/questions/6558535/find-the-date-for-the-first-monday-after-a-given-date

def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()

    if days_ahead <= 0:  # target day already happened this week
        days_ahead += 7

    return d + timedelta(days_ahead)


d = date.today()
next_monday = next_weekday(d, 0)  # 0 = Mon, 1 = Tues, etc.
print(next_monday)
