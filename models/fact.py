from db import db

class FactModel(db.Model):
    __tablename__ = 'facts'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    violation_type = db.Column(db.String(20), nullable=False)
    car_vrp = db.Column(db.String(20), nullable=False)
    car_contour = db.Column(db.Integer, nullable=False)
    violation = db.Column(db.Boolean, nullable=False)
    location_latitude = db.Column(db.Float, nullable=False)
    location_longitude = db.Column(db.Float, nullable=False)
    photo_content = db.Column(db.LargeBinary, nullable=False)
    fact_id = db.Column(db.String(100), nullable=False )
    dispatch_code = db.Column(db.Integer, nullable=False)
    zone_number = db.Column(db.Integer, nullable=False)
    country = db.Column(db.String(40), nullable=True)
    address = db.Column(db.String(150), nullable=True)
    city = db.Column(db.String(40), nullable=True)

    def __init__(self, date, time, violation_type, car_vrp, car_contour,
                violation, location_latitude, location_longitude, photo_content,
                fact_id, dispatch_code, zone_number, country=None, address=None, city=None) -> None:
        self.date = date
        self.time = time
        self.violation_type = violation_type
        self.car_vrp = car_vrp
        self.car_contour = car_contour
        self.violation = violation
        self.location_latitude = location_latitude
        self.location_longitude = location_longitude
        self.photo_content = photo_content
        self.fact_id = fact_id
        self.dispatch_code = dispatch_code
        self.zone_number = zone_number
        self.country = country
        self.address = address
        self.city = city


    def json(self) -> dict:
        return {'car_vrp': self.car_vrp,
                'date': self.date.strftime('%d.%m.%Y'),
                'time': self.time.strftime('%H:%M:%S'),
                'fact_id': self.fact_id,
                'violation_type': self.violation_type,
                'latitude': self.location_latitude,
                'longitude': self.location_longitude,
                'country': self.country,
                'address': self.address,
                'city': self.city}

    @classmethod
    def find_by_vrp(cls, vrp_no):
        return cls.query.filter_by(car_vrp=vrp_no).all()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save(self):
        db.session.add(self)
        db.session.commit()

