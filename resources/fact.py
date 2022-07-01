from flask_restful import Resource, reqparse
from datetime import date, time
from models.fact import FactModel


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


    def get(self, vrp_no=None):
        try:
            result = FactModel.find_by_vrp(vrp_no) if vrp_no else FactModel.find_all()
        except:
            return {'message': 'An error occurred while querying the database'}, 500

        facts = []
        if result:
            for row in result:
                facts.append(row.json())
            return {'facts': facts}, 201
        else:
            return {'message': f'No records with given vrp {vrp_no} are present in database'}, 404

    def post(self):
        data = Fact.parser.parse_args(req=Fact.root_parser.parse_args())
        _fact = {}
        date_time = data['date']
        _fact['date'] = date(int(date_time[6:10]), int(date_time[3:5]), int(date_time[0:2]))
        _fact['time'] = time(int(date_time[11:13]), int(date_time[14:16]), int(date_time[17:19]))
        _fact['violation_type'] = data['violationType']
        _fact['car_vrp'] = data['car']['vrp']
        _fact['car_contour'] = data['car']['contourClass']
        _fact['violation'] = data['violation']
        _fact['location_latitude'] = data['locationLatitude']
        _fact['location_longitude'] = data['locationLongitude']
        _fact['photo_content'] = data['photoContent'].encode()
        _fact['fact_id'] = data['id']
        _fact['dispatch_code'] = data['dispatchCode']
        _fact['zone_number'] = data['zoneNumber']
        _fact['country'] = data['country'] or None
        _fact['address'] = data['address'] or None
        _fact['city'] = data['city'] or None

        fact = FactModel(**_fact)
        print(fact.json())

        try:
            # fact.insert()
            fact.save()
        except:
            return {'message': 'An error occurred inserting the fact'}, 500

        return {'message': 'data was inserted successfully'}, 201


if __name__ == '__main__':
    print("OK")
