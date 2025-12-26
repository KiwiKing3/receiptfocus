import requests

token = "redacted"
vikunja_headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}
vikunja_done_task_data = {
    "done": True
}
vikunja_instance = "redacted"

while True:
    vikunja_task_id = input("ID:").strip()
    vikunja_done_task_url = f"{vikunja_instance}/api/v1/tasks/{vikunja_task_id}"
    response = requests.post(vikunja_done_task_url, json=vikunja_done_task_data, headers=vikunja_headers)
