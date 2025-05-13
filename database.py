
import psycopg2
from datetime import date, datetime, timedelta
import logging
logging.basicConfig(level=logging.INFO)

class Database:
    def __init__(self):

        try:
            self.conn =  psycopg2.connect(host='tcl-1.cp4csoyksuuv.us-east-2.rds.amazonaws.com',database='umpiring_request',user='postgres', password='cricket##4me', port='5432')
            logging.info("Opened database successfully")
            self.cursor = self.conn.cursor()
        except psycopg2.OperationalError as e:
            logging.error(e)

    def get_divisions_dict(self):
        query = "SELECT Division from Master"
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        division_dict = {}

        if results:
            divisions = [row[0] for row in results]

            divisions_list = [div.split("-")[0] for div in divisions]
            unique_league = sorted(set(divisions_list))

            for item in unique_league:
                division_dict[item] = []

            for div in divisions:
                groups = div.split("-")
                if groups[0] in division_dict:
                    if div not in division_dict[groups[0]]:
                        division_dict[groups[0]].append(div)

        # print(division_dict)
        return division_dict

    def get_grounds_list(self):
        grounds_list = []
        query = "SELECT Ground_Name from Grounds"
        try:
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            grounds_list = [row[0] for row in results]

        except psycopg2.OperationalError as e:
            logging.error(e)

        return sorted(set(grounds_list))

    def get_available_slots(self):

       # available_slots = []
        query = ("SELECT * FROM Submitted_Requests WHERE Available = 'Yes' ")

        try:
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            #available_slots = [row for row in results]
            return results

        except psycopg2.OperationalError as e:
            logging.error(e)


        return None

    def get_teams_list(self, league, division):
        query = "SELECT Team_Name from Master  WHERE League = %s AND Division = %s;"
        teams_list = []
        try:
            self.cursor.execute(query,(league, division,))
            results = self.cursor.fetchall()

            teams_list = [row[0] for row in results]

        except psycopg2.OperationalError as e:
            logging.error(e)

        return sorted(set(teams_list))

    def update_captain_name_email(self, league, team):
        query = 'SELECT Captain_Name, Captain_Email FROM Master WHERE League = %s AND Team_Name = %s';
        try:
            self.cursor.execute(query, (league, team,))
            result = self.cursor.fetchone()
            if result:
                return (result[0], result[1])
            else:
                print(f"Captain {team} not found")
                return None
        except psycopg2.OperationalError as e:
            logging.error(e)

    def get_umpire_list(self):
        umpires_list = []
        query = 'SELECT full_Name FROM Umpires_list'
        try:
            #self.cursor.execute(query)

            self.cursor.execute(query)
            results = self.cursor.fetchall()

            umpires_list=[row[0] for row in results]

        except psycopg2.OperationalError as e:
            logging.error(e)

        return sorted(set(umpires_list))

    def update_umpire_email_phone(self, name):
        query = 'SELECT umpire_Email, umpire_Phone FROM Umpires_list WHERE Full_Name = %s'
        try:
            self.cursor.execute(query,(name,))
            result = self.cursor.fetchone()
            if result:
                return result[0], result[1]
            else:
                print(f"Umpire {name} not found")

        except psycopg2.OperationalError as e:
            logging.error(e)

        return None
    def submit_request(self, vals):
        query = "INSERT INTO Submitted_Requests (Requesting_Team, Captain_Name, Captain_Email, Division, Team1, Team2, Match_Date, Match_Time, Ground, Available,processed) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        try:
            self.cursor.execute(query, (vals[0],vals[1],vals[2],vals[3], vals[4], vals[5], vals[6], vals[7], vals[8], vals[9],"No"))
            self.conn.commit()
            logging.info("Request Submitted.")

        except psycopg2.OperationalError as e:
            logging.error(e)

    # (TimeStamp,Umpire_Name,Umpire_Email,Umpire_Phone,Request_No)

    def accept_request(self, vals):
        query = "INSERT INTO Accepted_Requests (TimeStamp, Umpire_Name, Umpire_Email, Umpire_Phone, Request_No,processed) VALUES (%s,%s,%s,%s,%s,%s);"
        #vals = (str(datetime.now()),'Vinod,Batra', 'batravk@hotmail.com','919-457-8570', 65)
        try:
            self.cursor.execute(query, (vals[0], vals[1], vals[2], vals[3], vals[4],"No"))
            self.conn.commit()
            logging.info("Request Accepted.")
        except psycopg2.OperationalError as e:
            logging.error(e)

    def update_availability(self, request_No):

        query = "Update Submitted_Requests set Available = 'No' where Request_No = %s;"
        try:
            self.cursor.execute(query, (request_No,))
            self.conn.commit()
            logging.info("Request Updated.")
        except psycopg2.OperationalError as e:
            logging.error(e)


def main(data_to_append=None):

    db = Database()

    # self.conn = sqlite3.connect(self.db_file)
    unique_divisions = db.get_divisions_dict()
    grounds_list = db.get_grounds_list()
    available_slots = db.get_available_slots()
    teams_list = db.get_teams_list("TCL", "HT-7")

    print (unique_divisions)

    print (grounds_list)

    print (teams_list)
    captain_info = db.update_captain_name_email("TCL", "Panthers")
    print(captain_info)
    umpire_list = db.get_umpire_list()
    print(umpire_list)
    umpire_email = db.update_umpire_email_phone('Amit,Dave')
    print(umpire_email)
    db.update_availability(64)
    available_slots = db.get_available_slots()
    print(available_slots)

    vals = (str(datetime.now()), 'Vinod,Sharma', 'sharma@hotmail.com', '919-129-2345', 69)
    db.accept_request(vals)
    vals = ['Panthers', 'Kamal Dangeti', 'sridhardangeti@gmail.com', 'HT-4', 'RTP Chargers', 'Emperors',
            '2025-04-26', '16:00:00', 'FVAA-Lower', 'No']
    db.submit_request(vals)
    available_slots = db.get_available_slots()
    print(available_slots)
    # print (result)


if __name__ == "__main__":
    main()
