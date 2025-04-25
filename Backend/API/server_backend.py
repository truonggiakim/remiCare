from flask import Flask, jsonify, request
from datetime import datetime, timezone
#from zoneinfo import ZoneInfo
from flask_sqlalchemy import SQLAlchemy
#import json 


app = Flask(__name__)
#intializes the database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Location(db.Model):
    #this is the class for storing the locations
    id = db.Column(db.Integer, primary_key=True)
    watch_id = db.Column(db.String(50), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def __init__(self, watch_id, lat, lon):
        self.watch_id = watch_id
        self.lat = lat
        self.lon = lon
        #needed because it wouldn't update the location without it. do not delete the first one
        #it will cry like a bitch
        self.created_at = datetime.now(timezone.utc)

class Reminder(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    reminder = db.Column(db.String(120), nullable=False)
    time = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

with app.app_context():
    db.create_all()

def reminder_to_dict(r):
    return {
        "id": r.id,
        "reminder": r.reminder,
        "time": r.time,
        "created_at": r.created_at.isoformat(),
    }

###################################################################
####################location#######################################
##################################################################

@app.route('/location', methods=['POST'])
def recieve_location():
    '''
    takes the location from the watch and stores it for later

    body expected = {
        "watch_id": "abc123",
        "lat": 37.3353533,
        "lon": 96.343443,
    }
    '''
    location_data = request.json
    watch_id = location_data.get("watch_id")
    latitude = location_data.get("lat")
    longitude = location_data.get("lon")

    new_location = Location(watch_id,latitude, longitude)
    db.session.add(new_location)
    db.session.commit()

    all_locations = Location.query.all()
    ##this is for debugging delete before the final version
    print("Current locations in the database:")
    for loc in all_locations:
        print(f"ID: {loc.id}, Watch ID: {loc.watch_id}, Latitude: {loc.lat}, Longitude: {loc.lon}, Created At: {loc.created_at}")

    if Location.query.count() > 5:
        oldest_location = Location.query.order_by(Location.created_at).first()
        db.session.delete(oldest_location)
        db.session.commit()

    return jsonify({
        "status": "location recieved"
    }), 200

@app.route('/location', methods=['GET'])
def get_location():
    '''
    receives the location from the database
    
    no body expected
    '''
    #gets the newest location
    newest_location = Location.query.order_by(Location.created_at.desc()).first()

    if newest_location:
        return jsonify({
            "watch_id": newest_location.watch_id,
            "lat": newest_location.lat,
            "lon": newest_location.lon,
            "created_at": newest_location.created_at.isoformat()
        })
    else:
        return jsonify({
            "message": "No locations found"
        }), 404
    
    
@app.route('/clear_locations', methods=['POST'])
def clear_locations():
    #pretty much just for testing. not needed in the final project becaue it only stores the last few locations
    #can delete once we feel confident once the api is done, but no reason to. its not harming anyting
    '''
    Clears all the current locations from the database
    '''
    try:
        # Delete all entries in the Location table
        db.session.query(Location).delete()
        db.session.commit()
        return jsonify({
            "status": "all locations cleared"
        }), 200
    except Exception as e:
        # Rollback if there was an error
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    

###################################################################
####################reminder#######################################
##################################################################
@app.route("/reminders", methods=["POST"])
def add_reminder():
    data = request.json or {}
    reminder = data.get("reminder", "").strip()
    time = data.get("time", "").strip()
    if not reminder or not time:
        return jsonify({
            "error": "reminder and time required",
        })

    r = Reminder(reminder=reminder, time=time)
    db.session.add(r)
    db.session.commit()
    return jsonify(reminder_to_dict(r)), 200

@app.route("/reminders/<int:rem_id>", methods=["PUT"])
def update_reminder(rem_id):
    r = Reminder.query.get_or_404(rem_id)
    data = request.json or {}
    reminder = data.get("reminder", r.reminder).strip()
    time = data.get("time", r.time).strip()
    print(f"Put /reminders/{rem_id} payload: {request.json}")
    if not reminder or not time:
        return jsonify({
            "error": "reminder and time required",
        })
    
    r.reminder, r.time = reminder, time
    db.session.commit()
    return jsonify(reminder_to_dict(r), 200)

@app.route("/reminders/<int:rem_id>", methods=["DELETE"])
def delete_reminder(rem_id):
    r = Reminder.query.get_or_404(rem_id)
    db.session.delete(r)
    db.session.commit()
    return "", 204

@app.route("/reminders", methods=["GET"])
def list_reminders():
    data = Reminder.query.order_by(Reminder.created_at).all()
    return jsonify([reminder_to_dict(r) for r in data]), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="8000")

