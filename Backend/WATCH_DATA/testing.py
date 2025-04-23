import requests
import json
from random import uniform
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

def test_send_location():
    route = "/location"
    url = BASE_URL + route
    print(url)
    data = {
        "watch_id": "abc123",
        "lat": uniform(-85,85),
        "lon": uniform(-100,100),
    }

    headers = {
        "ContentType": "application/json"
    }

    response = requests.post(url=url, json=data, headers=headers)

    if response.status_code == 200:
        print("location recieved!")
    else:
        print(f"Failed to send location, {response.status_code}")
        print(response.text)

def test_get_location():
    route = "/location"
    url = BASE_URL + route

    response = requests.get(url)

    if response.status_code == 200:
        print("most Recent location:")
        print(json.dumps(response.json(), indent=4))
    else:
        print(f"failed to retrieve location. status code: {response.status_code}")
        print(response.json())

def clear_locations():
    route = "/clear_locations"
    url = BASE_URL + route
    print(url)
    response = requests.post(url=url)
    if response.status_code == 200:
        print(response.json())
    else: print(response.text)

def create_reminders():
    route = "/reminders"
    reminder = input("reminder text: ").strip()
    time = input("Time: ").strip()
    if not reminder or not time:
        print("both are required")
        return
    response = requests.post(BASE_URL + route, json={"reminder": reminder, "time": time})
    print("created:", response.json() if response.ok else response.txt)

def print_reminders():
    route = "/reminders"
    response = requests.get(BASE_URL + route)
    if response.ok:
        if response.json():
            print(json.dumps(response.json(), indent=4))
        else:
            print("no reminders")
    
def clear_reminders():
    route = "/reminders"
    response = requests.get(BASE_URL + route)
    if not response.ok:
        print(response.text)
        return
    for rem in response.json():
        del_resp = requests.delete(BASE_URL+route+"/" + str(rem['id']))
        if del_resp.ok:
            print(f"deleted id {rem['id']}")
        else:
            print(f"failed to delete reminder f{rem['id']}")





    
while True:
    action = int(input("1 to get a new location, 2 to see the latest location, 3 to clear locations, 4 to make a new reminders, and 5 print reminders, 6 to delete all reminders: "))
    if action == 1:
        test_send_location()
    elif action == 2:
        test_get_location()
    elif action == 3:
        clear_locations()
    elif action == 4:
        create_reminders()
    elif action == 5:
        print_reminders()
    elif action == 6:
        clear_reminders()
    else: break

