import psycopg2
from flask_restful import Resource, reqparse
from flask import jsonify, make_response
from datetime import date, time
import json

DBNAME = 'pi'
USER = 'pi'
PASSWORD = '$ecretP2nda'
HOST = '192.168.0.112'
PORT = 5432

class Fact(Resource):
    root_parser = reqparse.RequestParser()
    root_parser.add_argument('fact',
        type=dict,
        required=True
    )

    parser = reqparse.RequestParser()
    parser.add_argument('date',
        type=str,
        required=True,
        location='fact',
        help="DataTime string in format: DD.MM.YYYY HH.MM.SS.000+TZ"
    )
    parser.add_argument('violationType',
        type=str,
        required=True,
        location='fact',
        help="Violation type, 'noViolation' if everything is OK"
    )
    parser.add_argument('car',
        type=dict,
        required=True,
        location='fact'
    )
    parser.add_argument('violation',
        type=bool,
        required=True,
        location='fact',
        help="True if violation exist, False otherwise"
    )
    parser.add_argument('locationLatitude',
        type=float,
        location='fact',
        required=True,
    )
    parser.add_argument('locationLongitude',
        type=float,
        location='fact',
        required=True,
    )
    parser.add_argument('photoContent',
        type=str,
        required=True,
        location='fact',
        help='photo in base64 data format'
    )
    parser.add_argument('id',
        type=str,
        required=True,
        location='fact'
    )
    parser.add_argument('dispatchCode',
        type=int,
        location='fact',
        required=True
    )
    parser.add_argument('zoneNumber',
        type=int,
        location='fact',
        required=True
    )
    parser.add_argument('country',
        type=str,
        location='fact',
        required=False
    )
    parser.add_argument('address',
        type=str,
        location='fact',
        required=False
    )
    parser.add_argument('city',
        type=str,
        location='fact',
        required=False
    )

    @classmethod
    def find_by_vrp(cls, vrp_no):
        connection = psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD,
                                              host=HOST, port=PORT)
        cursor = connection.cursor()

        parameters = 'date, time, car_vrp, violationType, locationLatitude, locationLongitude, \
        country, address, city'

        if vrp_no != 'all':
            get_query = f"SELECT {parameters} FROM facts WHERE car_vrp=%s"
            cursor.execute(get_query, (vrp_no,))
            result = cursor.fetchall()
        else:
            get_query = f"SELECT {parameters} FROM facts"
            cursor.execute(get_query)
            result = cursor.fetchall()
        connection.close()

        return result


    def get(self, vrp_no=None):
        try:
            result = self.find_by_vrp(vrp_no) if vrp_no else self.find_by_vrp('all')
        except:
            return {'message': 'An error occurred while querying the database'}, 500

        facts = []
        if result:
            for row in result:
                facts.append({'vrp': row[2], 'date': row[0].strftime('%d.%m.%Y'),
                'time': row[1].strftime('%H:%M:%S'), 'violationType': row[3],
                'latitude': row[4], 'longitude': row[5], 'country': row[6],
                'address': row[7], 'city': row[8]})
            return {'facts': facts}, 201
        else:
            return {'message': f'No records with given vrp {vrp_no} are present in database'}, 404

    def post(self):
        data = Fact.parser.parse_args(req=Fact.root_parser.parse_args())
        fact = {}
        date_time = data['date']

        fact = {}
        fact['date'] = date(int(date_time[6:10]), int(date_time[3:5]), int(date_time[0:2]))
        fact['time'] = time(int(date_time[11:13]), int(date_time[14:16]), int(date_time[17:19]))
        fact['violationType'] = data['violationType']
        fact['car_vrp'] = data['car']['vrp']
        fact['car_contour'] = data['car']['contourClass']
        fact['violation'] = data['violation']
        fact['locationLatitude'] = data['locationLatitude']
        fact['locationLongitude'] = data['locationLongitude']
        fact['photoContent'] = data['photoContent'].encode()
        fact['id'] = data['id']
        fact['dispatchCode'] = data['dispatchCode']
        fact['zoneNumber'] = data['zoneNumber']
        fact['country'] = data['country'] or None
        fact['address'] = data['address'] or None
        fact['city'] = data['city'] or None

        connection = psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD,
                                      host=HOST, port=PORT)
        cursor = connection.cursor()

        insert_query = "INSERT INTO facts VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        try:
            cursor.execute(insert_query, (fact['date'], fact['time'], fact['violationType'],
                                         fact['car_vrp'], fact['car_contour'],
                                         fact['violation'], fact['locationLatitude'],
                                         fact['locationLongitude'], fact['photoContent'],
                                         fact['id'],fact['dispatchCode'], fact['zoneNumber'],
                                         fact['country'], fact['address'], fact['city']))
            connection.commit()
            connection.close()
        except:
            connection.close()
            return {'message': 'An error occurred inserting the fact'}, 500

        return {'message': 'data was inserted successfully'}, 201
        # return json.dumps(fact, indent=4, sort_keys=True, default=str), 201


if __name__ == '__main__':
    print("OK")
