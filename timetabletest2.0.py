import datetime

subject = "Mathe"


today = datetime.date.today()
today_weekday = today.weekday()
calendar_week = today.isocalendar()[1]

if calendar_week % 2 == 0:
    timetable = [
        ["Deutsch", "Mathe", "Chemie"],
        ["Erdkunde", "Geschichte", "Englisch"],
        ["Französisch", "Religion", "Kunst"],
        ["Sport", "Englisch", "Politik"],
        ["Biologie", "Mathe", "Physik"]
    ]
else:
    timetable = [
        ["Deutsch", "Mathe", "Chemie"],
        ["Erdkunde", "Geschichte", "Französisch"],
        ["Französisch", "Religion", "Kunst"],
        ["Sport", "Englisch", "Politik", "Deutsch"],
        ["Biologie", "Mathe", "Physik"]
    ]


for i in range(1, 8):
    day_index = (today_weekday + i) % 7

    if day_index > 4:
        continue

    timetable_on_target_day = timetable[day_index]

    if subject in timetable_on_target_day:
        due_date = today + datetime.timedelta(days=i)
        break

print(due_date)