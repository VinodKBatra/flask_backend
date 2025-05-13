from flask import Flask, jsonify, request
from flask_cors import CORS
from database import Database

app = Flask(__name__)
CORS(app)

db = Database()

@app.route('/divisions', methods=['GET'])
def get_divisions():
    divisions = db.get_divisions_dict()
    return jsonify(divisions)

@app.route('/grounds', methods=['GET'])
def get_grounds():
    grounds = db.get_grounds_list()
    return jsonify(grounds)

@app.route('/available_slots', methods=['GET'])
def get_slots():
    slots = db.get_available_slots()
    return jsonify(slots)

@app.route('/teams', methods=['GET'])
def get_teams():
    league = request.args.get('league')
    division = request.args.get('division')
    teams = db.get_teams_list(league, division)
    return jsonify(teams)

@app.route('/captain', methods=['GET'])
def get_captain():
    league = request.args.get('league')
    team = request.args.get('team')
    result = db.update_captain_name_email(league, team)
    return jsonify({'name': result[0], 'email': result[1]}) if result else ('', 404)



@app.route('/umpires', methods=['GET'])
def get_umpires():
    umpires = db.get_umpire_list()
    return jsonify(umpires)

@app.route('/umpire_contact', methods=['GET'])
def get_umpire_contact():
    name = request.args.get('name')
    result = db.update_umpire_email_phone(name)
    return jsonify({'email': result[0], 'phone': result[1]}) if result else ('', 404)

@app.route('/submit_request', methods=['POST'])
def submit_request():
    vals = request.json.get("vals")
    db.submit_request(vals)
    return jsonify({'message': 'Request submitted.'}), 201

@app.route('/accept_request', methods=['POST'])
def accept_request():
    vals = request.json.get("vals")
    db.accept_request(vals)
    return jsonify({'message': 'Request accepted.'}), 201

@app.route('/update_availability', methods=['POST'])
def update_availability():
    request_no = request.json.get("request_no")
    db.update_availability(request_no)
    return jsonify({'message': 'Availability updated.'})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

