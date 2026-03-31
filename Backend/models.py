from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


def calculate_ticket_price(distance_km):
    """
    Calculate ticket price based on distance travelled.
    
    Fare Table:
    0–5 km   = ₹10
    5–10 km  = ₹20
    10–15 km = ₹30
    15–20 km = ₹40
    20–25 km = ₹50
    25–30 km = ₹60
    30–40 km = ₹70
    40–50 km = ₹80
    50–60 km = ₹90
    60–70 km = ₹100
    70–80 km = ₹120
    
    Minimum fare = ₹10
    
    Args:
        distance_km: Distance in kilometers (float)
    
    Returns:
        int: Ticket price in rupees
    """
    if distance_km <= 0:
        return 10  # Minimum fare
    
    if distance_km <= 5:
        return 10
    elif distance_km <= 10:
        return 20
    elif distance_km <= 15:
        return 30
    elif distance_km <= 20:
        return 40
    elif distance_km <= 25:
        return 50
    elif distance_km <= 30:
        return 60
    elif distance_km <= 40:
        return 70
    elif distance_km <= 50:
        return 80
    elif distance_km <= 60:
        return 90
    elif distance_km <= 70:
        return 100
    elif distance_km <= 80:
        return 120
    else:
        # For distances above 80km, charge ₹120 + ₹2 per additional km
        return 120 + int((distance_km - 80) * 2)

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    bookings = db.relationship('Booking', backref='user', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'email': self.email,
            'phone': self.phone,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Route(db.Model):
    __tablename__ = 'routes'
    
    id = db.Column(db.Integer, primary_key=True)
    start_location = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    distance_km = db.Column(db.Float)
    estimated_duration = db.Column(db.String(50))
    
    buses = db.relationship('Bus', backref='route', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'start_location': self.start_location,
            'destination': self.destination,
            'distance_km': self.distance_km,
            'estimated_duration': self.estimated_duration
        }

class Bus(db.Model):
    __tablename__ = 'buses'
    
    id = db.Column(db.Integer, primary_key=True)
    bus_name = db.Column(db.String(100), nullable=False)
    bus_type = db.Column(db.String(20), nullable=False)  # AC, Non-AC, Sleeper
    total_seats = db.Column(db.Integer, default=40)
    fare_per_seat = db.Column(db.Float, nullable=False)
    departure_time = db.Column(db.Time, nullable=False)
    arrival_time = db.Column(db.Time, nullable=False)
    route_id = db.Column(db.Integer, db.ForeignKey('routes.id'), nullable=False)
    amenities = db.Column(db.Text)  # JSON string for amenities
    
    def to_dict(self):
        return {
            'id': self.id,
            'bus_name': self.bus_name,
            'bus_type': self.bus_type,
            'total_seats': self.total_seats,
            'fare_per_seat': self.fare_per_seat,
            'departure_time': self.departure_time.strftime('%H:%M') if self.departure_time else None,
            'arrival_time': self.arrival_time.strftime('%H:%M') if self.arrival_time else None,
            'route': self.route.to_dict() if self.route else None,
            'amenities': self.amenities
        }

class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    booking_reference = db.Column(db.String(20), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    bus_id = db.Column(db.Integer, db.ForeignKey('buses.id'), nullable=False)
    source = db.Column(db.String(100), nullable=True)  # Added for route tracking
    destination = db.Column(db.String(100), nullable=True)  # Added for route tracking
    distance_km = db.Column(db.Float, nullable=True)  # Added for distance tracking
    travel_date = db.Column(db.Date, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, cancelled
    passenger_name = db.Column(db.String(100), nullable=False)
    passenger_email = db.Column(db.String(120), nullable=False)
    passenger_phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    bus = db.relationship('Bus', backref='bookings', lazy=True)
    seats = db.relationship('Seat', backref='booking', lazy=True)
    payment = db.relationship('Payment', backref='booking', lazy=True, uselist=False)

    def to_dict(self):
        return {
            'id': self.id,
            'booking_reference': self.booking_reference,
            'user_id': self.user_id,
            'user': self.user.to_dict() if self.user else None,
            'bus': self.bus.to_dict() if self.bus else None,
            'source': self.source,
            'destination': self.destination,
            'distance_km': self.distance_km,
            'travel_date': self.travel_date.isoformat() if self.travel_date else None,
            'total_amount': self.total_amount,
            'status': self.status,
            'passenger_name': self.passenger_name,
            'passenger_email': self.passenger_email,
            'passenger_phone': self.passenger_phone,
            'seats': [seat.to_dict() for seat in self.seats],
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Seat(db.Model):
    __tablename__ = 'seats'
    
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False)
    seat_number = db.Column(db.Integer, nullable=False)
    seat_type = db.Column(db.String(20), default='regular')  # regular, premium
    is_booked = db.Column(db.Boolean, default=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'booking_id': self.booking_id,
            'seat_number': self.seat_number,
            'seat_type': self.seat_type,
            'is_booked': self.is_booked
        }

class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False, unique=True)
    payment_method = db.Column(db.String(50))  # UPI, Card, NetBanking
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, completed, failed
    transaction_id = db.Column(db.String(100))
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'booking_id': self.booking_id,
            'payment_method': self.payment_method,
            'amount': self.amount,
            'status': self.status,
            'transaction_id': self.transaction_id,
            'payment_date': self.payment_date.isoformat() if self.payment_date else None
        }


class BookingHistory(db.Model):
    """
    Booking History table - stores all booking records for tracking and history.
    Every successful booking creates an entry here automatically.
    """
    __tablename__ = 'booking_history'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    bus_id = db.Column(db.Integer, db.ForeignKey('buses.id'), nullable=False)
    source = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    seat_number = db.Column(db.Integer, nullable=False)
    distance_km = db.Column(db.Float, nullable=False)
    ticket_price = db.Column(db.Float, nullable=False)
    booking_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    status = db.Column(db.String(20), default='CONFIRMED')  # CONFIRMED / CANCELLED

    # Relationships
    user = db.relationship('User', backref='booking_history')
    bus = db.relationship('Bus', backref='booking_history')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'bus_id': self.bus_id,
            'source': self.source,
            'destination': self.destination,
            'seat_number': self.seat_number,
            'distance_km': self.distance_km,
            'ticket_price': self.ticket_price,
            'booking_time': self.booking_time.isoformat() if self.booking_time else None,
            'status': self.status
        }
