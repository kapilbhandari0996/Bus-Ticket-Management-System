"""
Quick database seeding script - adds minimal test data
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db, User, Route, Bus, BookingHistory
from werkzeug.security import generate_password_hash
from datetime import time

app = create_app()

def seed_data():
    """Seed database with minimal test data"""
    with app.app_context():
        # Create tables if they don't exist
        print("Creating database tables...")
        db.create_all()
        print("Tables created successfully!")

        # Check if routes already exist
        existing_route = Route.query.first()
        if existing_route:
            print("Data already exists in database!")
            print(f"Routes count: {Route.query.count()}")
            print(f"Buses count: {Bus.query.count()}")
            print(f"Users count: {User.query.count()}")
            return

        print("Seeding database with sample data...")

        # Create sample routes (only a few key routes)
        sample_routes = [
            Route(start_location='Pune Station', destination='Shivajinagar', distance_km=3.5, estimated_duration='8m'),
            Route(start_location='Pune Station', destination='Swargate', distance_km=4.0, estimated_duration='10m'),
            Route(start_location='Pune Station', destination='Hinjewadi Phase 1', distance_km=18.5, estimated_duration='45m'),
            Route(start_location='Pune Station', destination='Baner', distance_km=12.0, estimated_duration='30m'),
            Route(start_location='Pune Station', destination='Aundh', distance_km=10.0, estimated_duration='25m'),
            Route(start_location='Shivajinagar', destination='Hinjewadi Phase 1', distance_km=16.0, estimated_duration='40m'),
            Route(start_location='Shivajinagar', destination='Baner', distance_km=10.0, estimated_duration='25m'),
            Route(start_location='Swargate', destination='Katraj', distance_km=9.0, estimated_duration='20m'),
            Route(start_location='Swargate', destination='Hadapsar', distance_km=8.0, estimated_duration='18m'),
            Route(start_location='Hadapsar', destination='Viman Nagar', distance_km=6.0, estimated_duration='15m'),
        ]

        for route in sample_routes:
            db.session.add(route)

        db.session.flush()
        print(f"Added {len(sample_routes)} routes")

        # Create sample buses for each route
        sample_buses = []
        bus_templates = [
            {'name': 'EXP-101', 'type': 'AC', 'fare': 50, 'departure': time(6, 0), 'arrival': time(6, 45)},
            {'name': 'CITY-101', 'type': 'Non-AC', 'fare': 30, 'departure': time(6, 30), 'arrival': time(7, 15)},
            {'name': 'EXP-102', 'type': 'AC', 'fare': 50, 'departure': time(7, 0), 'arrival': time(7, 45)},
            {'name': 'CITY-102', 'type': 'Non-AC', 'fare': 30, 'departure': time(7, 30), 'arrival': time(8, 15)},
            {'name': 'EXP-103', 'type': 'AC', 'fare': 50, 'departure': time(8, 0), 'arrival': time(8, 45)},
        ]

        for idx, route in enumerate(sample_routes):
            for template in bus_templates:
                # Calculate arrival time based on route duration
                bus = Bus(
                    bus_name=f"{template['name']}-{idx+1}",
                    bus_type=template['type'],
                    total_seats=40,
                    fare_per_seat=template['fare'],
                    departure_time=template['departure'],
                    arrival_time=template['arrival'],
                    route_id=route.id,
                    amenities='["GPS Tracking", "Emergency Exit", "First Aid"]'
                )
                sample_buses.append(bus)
                db.session.add(bus)

        print(f"Added {len(sample_buses)} buses")

        # Create sample users
        admin_user = User(
            full_name='Admin User',
            email='admin@letsgo.com',
            password=generate_password_hash('admin123'),
            phone='9999999999'
        )
        test_user = User(
            full_name='Test User',
            email='test@example.com',
            password=generate_password_hash('test123'),
            phone='9876543210'
        )

        db.session.add(admin_user)
        db.session.add(test_user)
        print("Added 2 users")

        # Commit all changes
        db.session.commit()

        print("\n=== Database Seeding Complete ===")
        print(f"Total Routes: {Route.query.count()}")
        print(f"Total Buses: {Bus.query.count()}")
        print(f"Total Users: {User.query.count()}")
        print("\nUser Credentials:")
        print("  1. Email: admin@letsgo.com / Password: admin123")
        print("  2. Email: test@example.com / Password: test123")
        print("====================================")

if __name__ == '__main__':
    seed_data()
