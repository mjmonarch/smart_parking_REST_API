import psycopg2
from db import db

DBNAME = 'pi'
USER = 'pi'
PASSWORD = '$ecretP2nda'
HOST = '192.168.0.112'
PORT = 5432 


class FactModel(db.Model):
    __tablename__ = 'facts'
    _id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    violationType = db.Column(db.String(20), nullable=False)
    car_vrp = db.Column(db.String(20), nullable=False)
    car_contour = db.Column(db.Integer, nullable=False)
    violation = db.Column(db.Boolean, nullable=False)
    locationLatitude = db.Column(db.Float, nullable=False)
    locationLongitude = db.Column(db.Float, nullable=False)
    photoContent = db.Column(db.LargeBinary, nullable=False)
    id = db.Column(db.String(100), nullable=False )
    dispatchCode = db.Column(db.Integer, nullable=False)
    zoneNumber = db.Column(db.Integer, nullable=False)
    country = db.Column(db.String(40), nullable=True)
    address = db.Column(db.String(150), nullable=True)
    city = db.Column(db.String(40), nullable=True)

    def __init__(self, date, time, violationType, car_vrp, car_contour,
                violation, locationLatitude, locationLongitude, photoContent,
                id, dispatchCode, zoneNumber, country=None, address=None, city=None) -> None:
        self.date = date
        self.time = time
        self.violationType = violationType
        self.car_vrp = car_vrp
        self.car_contour = car_contour
        self.violation = violation
        self.locationLatitude = locationLatitude
        self.locationLongitude = locationLongitude
        self.photoContent = photoContent
        self.id = id
        self.dispatchCode = dispatchCode
        self.zoneNumber = zoneNumber
        self.country = country
        self.address = address
        self.city = city

    def json(self) -> dict:
        return {'car_vrp': self.car_vrp,
                'id': self.id,
                'date': self.date.strftime('%d.%m.%Y'),
                'time': self.time.strftime('%H:%M:%S'),
                'violationType': self.violationType,
                'latitude': self.locationLatitude,
                'longitude': self.locationLongitude,
                'country': self.country,
                'address': self.address,
                'city': self.city}


    @classmethod
    def find_by_vrp(cls, vrp_no):
        connection = psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD,
                                              host=HOST, port=PORT)
        cursor = connection.cursor()

        parameters = 'date, time, violationType, car_vrp, car_contour, violation, \
                    locationLatitude, locationLongitude, photoContent, id, \
                    dispatchCode, zoneNumber, country, address, city'

        if vrp_no != 'all':
            get_query = f"SELECT {parameters} FROM facts WHERE car_vrp=%s"
            cursor.execute(get_query, (vrp_no,))
            result = cursor.fetchall()
        else:
            get_query = f"SELECT {parameters} FROM facts"
            cursor.execute(get_query)
            result = cursor.fetchall()
        connection.close()

        facts = []
        for row in result:
            facts.append(cls(*row))
        return facts


    def insert(self):
        connection = psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD,
                                              host=HOST, port=PORT)
        cursor = connection.cursor()

        insert_query = "INSERT INTO facts VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        cursor.execute(insert_query, (self.date, self.time, self.violationType,
                                    self.car_vrp, self.car_contour,
                                    self.violation, self.locationLatitude,
                                    self.locationLongitude, self.photoContent,
                                    self.id,self.dispatchCode, self.zoneNumber,
                                    self.country, self.address, self.city))
        connection.commit()
        connection.close()
      
    

