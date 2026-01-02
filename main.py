from escpos.printer import *
from escpos.image import *
import escpos
import requests
import datetime
import locale
from flask import Flask, render_template, request
from dotenv import load_dotenv
import os

load_dotenv()

#printer vars
#printer = Network("127.0.0.1")
printer = Usb(0x04b8, 0x0202, 0, profile="TM-T88V")
#printer = Dummy(profile="TM-T88V")

#vikunja api vars
token = os.getenv('vikunja_api_token')
vikunja_headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}
vikunja_project_id = os.getenv('vikunja_project_id')
vikunja_instance = os.getenv('vikunja_instance')
vikunja_task_url = f"{vikunja_instance}/api/v1/projects/{vikunja_project_id}/tasks"
vikunja_label_id_url = f"{vikunja_instance}/api/v1/labels"

#time vars:
today = datetime.date.today()
today_weekday = today.weekday()
calendar_week = today.isocalendar()[1]
due_date_time = "07:00:00" #school start

#timetable
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


#misc vars
#locale
locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')
#optional task info
task_info = None

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    global due_date_str, subject, task_title, task_info
    if request.method == 'GET':
        return render_template('index.html')


    subject = request.form.get('subject')
    next_lesson = request.form.get('next_date')
    if next_lesson == "on":
        for i in range(1, 8):
            day_index = (today_weekday + i) % 7

            if day_index > 4: #skip weekends
                continue

            timetable_on_target_day = timetable[day_index]

            if subject in timetable_on_target_day:
                due_date = today + datetime.timedelta(days=i)
                due_date_str = datetime.date.strftime(due_date, "%Y-%m-%d")
                break
    else: 
        due_date_str = request.form.get('date')
    task_title = request.form.get('task')
    task_info = request.form.get('info')
    #add time for Vikunja
    due_date_vikunja = f"{due_date_str}T{due_date_time}Z"
    #convert date string to datetime format:
    due_date = datetime.datetime.strptime(due_date_str, "%Y-%m-%d")
    #convert datetime to human readable
    due_date_hr = datetime.date.strftime(due_date, "%A, %d. %B")

    #set data for task
    vikunja_task_data = {
        "title": task_title,
        "due_date": due_date_vikunja,
        "description": task_info
    }


    label_params = {'s': subject}
    vikunja_task_response = requests.put(vikunja_task_url, json=vikunja_task_data, headers=vikunja_headers)
    vikunja_label_id = requests.get(vikunja_label_id_url, params=label_params, headers=vikunja_headers).json()[0]['id']

    #get task ID from task request response
    vikunja_task_id = vikunja_task_response.json()['id']
    vikunja_task_label_url = f"{vikunja_instance}/api/v1/tasks/{vikunja_task_id}/labels"

    #add label to task
    vikunja_label_data = {
        "label_id": vikunja_label_id,
        "task": vikunja_task_id
   #     if 
    }
    requests.put(vikunja_task_label_url, json=vikunja_label_data, headers=vikunja_headers)

    printer.set(custom_size=True, width=2, height=2)
    printer.text(f"{subject}")
    printer.ln()
    printer.ln()

    printer.set(custom_size=False, bold=True)
    printer.text("Aufgabe: ")
    printer.set(bold=False)
    printer.text(task_title)
    printer.ln()
    printer.ln()

    if task_info != "":
        printer.set(bold=True)
        printer.text(f"Notizen: ")
        printer.set(bold=False)
        printer.text(task_info)
        printer.ln()
        printer.ln()

    printer.set(bold=True)
    printer.text("Bis: ")
    printer.set(bold=False)
    printer.text(due_date_hr)
    printer.ln()
    printer.ln()

    code128_prefix = "{B"
    printer.barcode(f"{code128_prefix}{vikunja_task_id}", "CODE128", pos="OFF")
    printer.cut()

    return render_template('index.html')




if __name__ == '__main__':
    app.run(host="0.0.0.0")

