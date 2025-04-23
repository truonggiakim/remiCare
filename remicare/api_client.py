import requests, threading, functools
BASE_URL = "http://127.0.0.1:8000"
class ApiClient:

    @staticmethod
    def _call(method, path, **kw):
        url = BASE_URL + path
        r = requests.request(method, url, timeout=5, **kw)
        r.raise_for_status()
        if r.status_code != 204:
            return r.json()
        
    
    @classmethod
    def list_reminders(cls):
        return cls._call("GET", "/reminders")
    
    @classmethod
    def add_reminder(cls, reminder, time):
        return cls._call("POST", "/reminders", json={
            "reminder": reminder, 
            "time": time,
            })
    
    @classmethod
    def update_reminder(cls, rem_id, reminder, time):
        return cls._call("PUT", f"/reminders/{rem_id}", json={
            "reminder": reminder,
            "time": time,
        })
    
    @classmethod
    def delete_reminder(cls, rem_id):
        cls._call("DELETE", f"/reminders/{rem_id}")
    
    @staticmethod
    def background(fn):
        @functools.wraps(fn)
        def _inner(*a, **k):
            threading.Thread(target=lambda: fn(*a, **k), daemon=True).start()
        return _inner
                         