import requests

token = "tk_2beec8a30c9030268d1e65a8954f919a475f9416"
vikunja_headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}
vikunja_done_task_data = {
    "done": True
}


while True:
    vikunja_task_id = input("ID:").strip()
    vikunja_done_task_url = f"http://192.168.178.122:3456/api/v1/tasks/{vikunja_task_id}"
    response = requests.post(vikunja_done_task_url, json=vikunja_done_task_data, headers=vikunja_headers)
