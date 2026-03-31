"""
Database initialization script for LETS GO Bus Service
This script creates tables and seeds initial data with ALL route combinations
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db, User, Route, Bus
from werkzeug.security import generate_password_hash
from datetime import time

app = create_app()

# All locations in the system
ALL_LOCATIONS = [
    'Pune Station',
    'Shivajinagar',
    'Swargate',
    'Hinjewadi Phase 1',
    'Hinjewadi Phase 2',
    'Wakad',
    'Baner',
    'Aundh',
    'Katraj',
    'Kondhwa',
    'Hadapsar',
    'Magarpatta',
    'Viman Nagar',
    'Kharadi',
    'Lohegaon',
    'Pimpri-Chinchwad',
    'Nigdi',
    'Kothrud Depot',
    'Warje Malwadi',
    'Bavdhan',
    'Koregaon Park',
    'Yerawada'
]

# Distance matrix (approximate distances in km)
DISTANCE_MATRIX = {
    ('Pune Station', 'Shivajinagar'): 3.5,
    ('Pune Station', 'Swargate'): 4.0,
    ('Pune Station', 'Hinjewadi Phase 1'): 18.5,
    ('Pune Station', 'Hinjewadi Phase 2'): 20.0,
    ('Pune Station', 'Wakad'): 15.0,
    ('Pune Station', 'Baner'): 12.0,
    ('Pune Station', 'Aundh'): 10.0,
    ('Pune Station', 'Katraj'): 12.0,
    ('Pune Station', 'Kondhwa'): 10.0,
    ('Pune Station', 'Hadapsar'): 5.0,
    ('Pune Station', 'Magarpatta'): 8.0,
    ('Pune Station', 'Viman Nagar'): 7.0,
    ('Pune Station', 'Kharadi'): 12.0,
    ('Pune Station', 'Lohegaon'): 10.0,
    ('Pune Station', 'Pimpri-Chinchwad'): 14.0,
    ('Pune Station', 'Nigdi'): 18.0,
    ('Pune Station', 'Kothrud Depot'): 6.0,
    ('Pune Station', 'Warje Malwadi'): 8.0,
    ('Pune Station', 'Bavdhan'): 10.0,
    ('Pune Station', 'Koregaon Park'): 4.0,
    ('Pune Station', 'Yerawada'): 5.0,
    
    ('Shivajinagar', 'Hinjewadi Phase 1'): 16.0,
    ('Shivajinagar', 'Hinjewadi Phase 2'): 18.0,
    ('Shivajinagar', 'Wakad'): 12.0,
    ('Shivajinagar', 'Baner'): 10.0,
    ('Shivajinagar', 'Aundh'): 8.0,
    ('Shivajinagar', 'Swargate'): 3.0,
    ('Shivajinagar', 'Katraj'): 11.0,
    ('Shivajinagar', 'Kondhwa'): 9.0,
    ('Shivajinagar', 'Hadapsar'): 6.0,
    ('Shivajinagar', 'Magarpatta'): 9.0,
    ('Shivajinagar', 'Viman Nagar'): 6.0,
    ('Shivajinagar', 'Kharadi'): 11.0,
    ('Shivajinagar', 'Lohegaon'): 9.0,
    ('Shivajinagar', 'Pimpri-Chinchwad'): 12.0,
    ('Shivajinagar', 'Nigdi'): 16.0,
    ('Shivajinagar', 'Kothrud Depot'): 5.0,
    ('Shivajinagar', 'Warje Malwadi'): 7.0,
    ('Shivajinagar', 'Bavdhan'): 9.0,
    ('Shivajinagar', 'Koregaon Park'): 3.5,
    ('Shivajinagar', 'Yerawada'): 4.5,
    
    ('Swargate', 'Katraj'): 9.0,
    ('Swargate', 'Kondhwa'): 7.0,
    ('Swargate', 'Hadapsar'): 8.0,
    ('Swargate', 'Magarpatta'): 10.0,
    ('Swargate', 'Hinjewadi Phase 1'): 20.0,
    ('Swargate', 'Hinjewadi Phase 2'): 22.0,
    ('Swargate', 'Wakad'): 18.0,
    ('Swargate', 'Baner'): 14.0,
    ('Swargate', 'Aundh'): 12.0,
    ('Swargate', 'Viman Nagar'): 6.0,
    ('Swargate', 'Kharadi'): 10.0,
    ('Swargate', 'Lohegaon'): 8.0,
    ('Swargate', 'Pimpri-Chinchwad'): 16.0,
    ('Swargate', 'Nigdi'): 20.0,
    ('Swargate', 'Kothrud Depot'): 5.0,
    ('Swargate', 'Warje Malwadi'): 7.0,
    ('Swargate', 'Bavdhan'): 9.0,
    ('Swargate', 'Koregaon Park'): 3.0,
    ('Swargate', 'Yerawada'): 5.0,
    
    ('Hinjewadi Phase 1', 'Wakad'): 5.0,
    ('Hinjewadi Phase 1', 'Baner'): 7.0,
    ('Hinjewadi Phase 1', 'Aundh'): 9.0,
    ('Hinjewadi Phase 1', 'Hinjewadi Phase 2'): 2.0,
    ('Hinjewadi Phase 1', 'Pimpri-Chinchwad'): 8.0,
    ('Hinjewadi Phase 1', 'Nigdi'): 12.0,
    ('Hinjewadi Phase 1', 'Kothrud Depot'): 12.0,
    ('Hinjewadi Phase 1', 'Warje Malwadi'): 10.0,
    ('Hinjewadi Phase 1', 'Bavdhan'): 12.0,
    
    ('Hinjewadi Phase 2', 'Wakad'): 4.0,
    ('Hinjewadi Phase 2', 'Baner'): 6.0,
    ('Hinjewadi Phase 2', 'Aundh'): 8.0,
    ('Hinjewadi Phase 2', 'Pimpri-Chinchwad'): 7.0,
    ('Hinjewadi Phase 2', 'Nigdi'): 11.0,
    ('Hinjewadi Phase 2', 'Kothrud Depot'): 14.0,
    ('Hinjewadi Phase 2', 'Warje Malwadi'): 12.0,
    ('Hinjewadi Phase 2', 'Bavdhan'): 14.0,
    
    ('Wakad', 'Baner'): 5.0,
    ('Wakad', 'Aundh'): 7.0,
    ('Wakad', 'Pimpri-Chinchwad'): 6.0,
    ('Wakad', 'Nigdi'): 10.0,
    ('Wakad', 'Kothrud Depot'): 10.0,
    ('Wakad', 'Warje Malwadi'): 8.0,
    ('Wakad', 'Bavdhan'): 10.0,
    
    ('Baner', 'Aundh'): 4.0,
    ('Baner', 'Pimpri-Chinchwad'): 8.0,
    ('Baner', 'Nigdi'): 12.0,
    ('Baner', 'Kothrud Depot'): 8.0,
    ('Baner', 'Warje Malwadi'): 6.0,
    ('Baner', 'Bavdhan'): 8.0,
    
    ('Aundh', 'Pimpri-Chinchwad'): 8.0,
    ('Aundh', 'Nigdi'): 12.0,
    ('Aundh', 'Kothrud Depot'): 6.0,
    ('Aundh', 'Warje Malwadi'): 5.0,
    ('Aundh', 'Bavdhan'): 6.0,
    
    ('Katraj', 'Kondhwa'): 6.0,
    ('Katraj', 'Hadapsar'): 10.0,
    ('Katraj', 'Magarpatta'): 12.0,
    ('Katraj', 'Kharadi'): 14.0,
    
    ('Kondhwa', 'Hadapsar'): 6.0,
    ('Kondhwa', 'Magarpatta'): 8.0,
    ('Kondhwa', 'Kharadi'): 10.0,
    
    ('Hadapsar', 'Magarpatta'): 3.0,
    ('Hadapsar', 'Viman Nagar'): 6.0,
    ('Hadapsar', 'Kharadi'): 8.0,
    ('Hadapsar', 'Lohegaon'): 7.0,
    ('Hadapsar', 'Koregaon Park'): 4.0,
    ('Hadapsar', 'Yerawada'): 5.0,
    
    ('Magarpatta', 'Viman Nagar'): 5.0,
    ('Magarpatta', 'Kharadi'): 7.0,
    ('Magarpatta', 'Lohegaon'): 6.0,
    
    ('Viman Nagar', 'Kharadi'): 5.0,
    ('Viman Nagar', 'Lohegaon'): 4.0,
    ('Viman Nagar', 'Koregaon Park'): 3.0,
    ('Viman Nagar', 'Yerawada'): 4.0,
    
    ('Kharadi', 'Lohegaon'): 6.0,
    
    ('Pimpri-Chinchwad', 'Nigdi'): 6.0,
    ('Pimpri-Chinchwad', 'Kothrud Depot'): 10.0,
    
    ('Kothrud Depot', 'Warje Malwadi'): 5.0,
    ('Kothrud Depot', 'Bavdhan'): 7.0,
    
    ('Warje Malwadi', 'Bavdhan'): 4.0,
    
    ('Koregaon Park', 'Yerawada'): 3.0,
    ('Koregaon Park', 'Kharadi'): 7.0,
    
    ('Yerawada', 'Kharadi'): 6.0,
}

def get_distance(start, destination):
    """Get distance between two locations"""
    key = (start, destination)
    if key in DISTANCE_MATRIX:
        return DISTANCE_MATRIX[key]
    # Try reverse
    reverse_key = (destination, start)
    if reverse_key in DISTANCE_MATRIX:
        return DISTANCE_MATRIX[reverse_key]
    # Default calculation based on location names
    return 10.0  # Default distance

def calculate_duration(distance_km):
    """Calculate estimated duration based on distance (avg speed 25 km/h in city)"""
    hours = int(distance_km / 25)
    minutes = int((distance_km / 25 - hours) * 60)
    if hours > 0:
        return f"{hours}h {minutes}m"
    return f"{minutes}m"

def calculate_fare(distance_km, bus_type):
    """Calculate fare based on distance and bus type"""
    base_fare = 10
    per_km_rate = 1.2 if bus_type == 'AC' else 0.8
    fare = base_fare + (distance_km * per_km_rate)
    return round(fare, 0)

def init_db():
    """Initialize database with tables and seed data"""
    with app.app_context():
        # Create all tables
        print("Creating database tables...")
        db.create_all()
        print("Tables created successfully!")

        # Check if data already exists - drop and recreate for fresh data
        if Route.query.first():
            print("Dropping existing tables...")
            db.drop_all()
            print("Creating fresh tables...")

        print("Seeding database with comprehensive route data...")

        # Generate all possible route combinations
        routes = []
        route_id_counter = 0
        
        # Create routes for all combinations (excluding same start and destination)
        for start in ALL_LOCATIONS:
            for destination in ALL_LOCATIONS:
                if start != destination:
                    distance = get_distance(start, destination)
                    duration = calculate_duration(distance)
                    
                    route = Route(
                        start_location=start,
                        destination=destination,
                        distance_km=distance,
                        estimated_duration=duration
                    )
                    routes.append(route)
                    db.session.add(route)
                    route_id_counter += 1

        db.session.flush()
        print(f"Added {len(routes)} routes")

        # Seed Buses for each route
        buses = []
        
        # Bus schedule configuration based on route type
        def get_schedule_config(start, destination):
            """Get bus schedule configuration based on route characteristics"""
            distance = get_distance(start, destination)
            
            # IT corridor routes (Hinjewadi, Wakad, Baner, Aundh, Shivajinagar)
            it_locations = ['Hinjewadi Phase 1', 'Hinjewadi Phase 2', 'Wakad', 'Baner', 'Aundh', 'Shivajinagar']
            is_it_route = start in it_locations and destination in it_locations
            
            # Station/Swargate are major terminals
            is_major_route = start in ['Pune Station', 'Swargate'] or destination in ['Pune Station', 'Swargate']
            
            # Short distance routes
            is_short_route = distance < 5
            
            if is_it_route:
                return {
                    'start_hour': 6,
                    'end_hour': 22,
                    'ac_fare': calculate_fare(distance, 'AC') + 5,
                    'non_ac_fare': calculate_fare(distance, 'Non-AC'),
                    'ac_prefix': 'IT-EXP',
                    'non_ac_prefix': 'IT',
                    'duration_mins': int(float(duration.replace('h', '*60+').replace('m', '')) if 'h' in duration else duration.replace('m', '')) + 5
                }
            elif is_major_route:
                return {
                    'start_hour': 5,
                    'end_hour': 23,
                    'ac_fare': calculate_fare(distance, 'AC') + 3,
                    'non_ac_fare': calculate_fare(distance, 'Non-AC'),
                    'ac_prefix': 'EXP',
                    'non_ac_prefix': 'CITY',
                    'duration_mins': int(float(duration.replace('h', '*60+').replace('m', '')) if 'h' in duration else duration.replace('m', '')) + 3
                }
            elif is_short_route:
                return {
                    'start_hour': 6,
                    'end_hour': 22,
                    'ac_fare': calculate_fare(distance, 'AC'),
                    'non_ac_fare': calculate_fare(distance, 'Non-AC'),
                    'ac_prefix': 'LINK',
                    'non_ac_prefix': 'SHUTTLE',
                    'duration_mins': max(10, int(float(duration.replace('h', '*60+').replace('m', '')) if 'h' in duration else duration.replace('m', '')))
                }
            else:
                return {
                    'start_hour': 6,
                    'end_hour': 21,
                    'ac_fare': calculate_fare(distance, 'AC') + 2,
                    'non_ac_fare': calculate_fare(distance, 'Non-AC'),
                    'ac_prefix': 'EXP',
                    'non_ac_prefix': 'CITY',
                    'duration_mins': int(float(duration.replace('h', '*60+').replace('m', '')) if 'h' in duration else duration.replace('m', '')) + 3
                }

        def add_buses_for_route(route, route_idx):
            """Add buses for a route with alternating AC and Non-AC buses"""
            config = get_schedule_config(route.start_location, route.destination)
            bus_list = []
            
            current_hour = config['start_hour']
            current_minute = 0
            bus_num = 1
            
            while current_hour < config['end_hour'] or (current_hour == config['end_hour'] and current_minute == 0):
                departure_time_str = f"{current_hour:02d}:{current_minute:02d}"

                # Calculate arrival time
                duration_mins = config['duration_mins']
                arr_minute = current_minute + duration_mins
                arr_hour = current_hour + (arr_minute // 60)
                arr_minute = arr_minute % 60
                arrival_time_str = f"{arr_hour:02d}:{arr_minute:02d}"

                # Alternate between AC and Non-AC buses
                if bus_num % 2 == 1:
                    # AC Bus
                    bus_list.append({
                        'name': f'{config["ac_prefix"]} {route_idx}-{bus_num:03d}',
                        'type': 'AC',
                        'fare': config['ac_fare'],
                        'departure': departure_time_str,
                        'arrival': arrival_time_str,
                        'route': route
                    })
                else:
                    # Non-AC Bus
                    bus_list.append({
                        'name': f'{config["non_ac_prefix"]} {route_idx}-{bus_num:03d}',
                        'type': 'Non-AC',
                        'fare': config['non_ac_fare'],
                        'departure': departure_time_str,
                        'arrival': arrival_time_str,
                        'route': route
                    })

                # Add 20-30 minute gap (alternate between 20 and 30 for frequent service)
                current_minute += 20 if bus_num % 2 == 1 else 30
                if current_minute >= 60:
                    current_hour += current_minute // 60
                    current_minute = current_minute % 60

                bus_num += 1
                
                # Limit to 20 buses per route to avoid excessive data
                if bus_num > 20:
                    break

            return bus_list

        # Generate buses for all routes
        all_buses_data = []
        for idx, route in enumerate(routes):
            all_buses_data.extend(add_buses_for_route(route, idx))

        print(f"Generating {len(all_buses_data)} bus schedules...")

        # Create bus objects
        for bus_data in all_buses_data:
            hour, minute = map(int, bus_data['departure'].split(':'))
            departure_time = time(hour, minute)

            arr_hour, arr_minute = map(int, bus_data['arrival'].split(':'))
            arrival_time = time(arr_hour, arr_minute)

            bus = Bus(
                bus_name=bus_data['name'],
                bus_type=bus_data['type'],
                total_seats=40,
                fare_per_seat=bus_data['fare'],
                departure_time=departure_time,
                arrival_time=arrival_time,
                route_id=bus_data['route'].id,
                amenities='["GPS Tracking", "Emergency Exit", "First Aid", "WiFi", "USB Charging"]' if bus_data['type'] == 'AC' else '["Emergency Exit", "First Aid"]'
            )
            buses.append(bus)
            db.session.add(bus)

        print(f"Added {len(buses)} buses across all routes")

        # Create demo users
        demo_users = [
            User(
                full_name='John Doe',
                email='john@example.com',
                password=generate_password_hash('password123'),
                phone='9876543210'
            ),
            User(
                full_name='Admin User',
                email='admin@letsgo.com',
                password=generate_password_hash('admin123'),
                phone='9999999999'
            )
        ]
        
        for user in demo_users:
            db.session.add(user)

        # Commit all changes
        db.session.commit()
        print("Database seeded successfully!")
        print("\n=== Database Initialization Complete ===")
        print(f"Total Locations: {len(ALL_LOCATIONS)}")
        print(f"Total Routes: {len(routes)}")
        print(f"Total Buses: {len(buses)}")
        print(f"\nAverage buses per route: {len(buses) / len(routes):.1f}")
        print("\nDemo User Credentials:")
        print("  1. Email: john@example.com / Password: password123")
        print("  2. Email: admin@letsgo.com / Password: admin123")
        print("========================================")

if __name__ == '__main__':
    init_db()
