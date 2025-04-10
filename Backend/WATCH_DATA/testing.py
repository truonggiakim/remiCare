import requests
import json
from random import randint
from datetime import datetime

BASE_URL = "http://192.168.1.69:8000"

def test_send_location():
    #route = "/location"
    url = "http://192.168.1.69:8000/location"
    print(url)
    data = {
        "watch_id": "abc123",
        "lat": randint(0,1000000000),
        "lon": randint(0,100000000),
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

    
while True:
    action = int(input("1 to get a new location, 2 to see the latest location, 3 to clear locations anything else to quit: "))
    if action == 1:
        test_send_location()
    elif action == 2:
        test_get_location()
    elif action == 3:
        clear_locations()
    else: break

