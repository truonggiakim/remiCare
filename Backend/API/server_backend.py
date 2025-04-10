from flask import Flask, jsonify, request
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from flask_sqlalchemy import SQLAlchemy
import json 


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Location(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    watch_id = db.Column(db.String(50), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def __init__(self, watch_id, lat, lon):
        self.watch_id = watch_id
        self.lat = lat
        self.lon = lon
        self.created_at = datetime.now(timezone.utc)

with app.app_context():
    db.create_all()

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
    '''
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

    
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="8000")

