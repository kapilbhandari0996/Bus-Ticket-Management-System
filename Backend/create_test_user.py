"""
Create a test user with ID 1 for testing purposes
Run this script to ensure a test user exists in the database
"""
from app import create_app
from models import db, User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Check if user with ID 1 exists
    user = db.session.get(User, 1)
    
    if user:
        print(f"User with ID 1 already exists: {user.email}")
    else:
        # Create test user
        test_user = User(
            id=1,
            full_name='Test User',
            email='test@example.com',
            password=generate_password_hash('test123'),
            phone='1234567890'
        )
        db.session.add(test_user)
        db.session.commit()
        print("Test user created successfully!")
        print("Email: test@example.com")
        print("Password: test123")
