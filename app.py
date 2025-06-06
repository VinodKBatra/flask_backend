from flask import Flask, jsonify, request
from flask_cors import CORS
from database import Database
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
load_dotenv()
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

@app.route('/send_bug_report', methods=['POST'])
def send_bug_report():
    EMAIL_ADDRESS = os.environ.get('BUG_REPORT_EMAIL')
    EMAIL_PASSWORD = os.environ.get('BUG_REPORT_PASSWORD')
    SMTP_SERVER = os.environ.get('BUG_REPORT_SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.environ.get('BUG_REPORT_SMTP_PORT', 587))
    data = request.get_json()
    to_email = data.get('to')
    message = data.get('message')
    if not to_email or not message:
        return jsonify({'error': 'Missing to or message'}), 400
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to_email
        msg['Subject'] = 'Bug Report from Kivy App'
        msg.attach(MIMEText(message, 'plain'))
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

