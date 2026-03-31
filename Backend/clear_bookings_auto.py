"""
Clear All Bookings Script (Non-Interactive)
This script removes all booking history from the database permanently.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db, Booking, Seat, Payment, BookingHistory

def clear_all_bookings():
    """Delete all bookings and related data from the database"""
    
    app = create_app()
    
    with app.app_context():
        print("🗑️  Clearing all booking history...")
        print("-" * 50)
        
        try:
            # Count records before deletion
            bookings_count = Booking.query.count()
            seats_count = Seat.query.count()
            payments_count = Payment.query.count()
            history_count = BookingHistory.query.count()
            
            print(f"📊 Records to delete:")
            print(f"   • Bookings: {bookings_count}")
            print(f"   • Seats: {seats_count}")
            print(f"   • Payments: {payments_count}")
            print(f"   • Booking History: {history_count}")
            print("-" * 50)
            
            if bookings_count == 0:
                print("✅ No bookings to delete. Database is already clean!")
                return
            
            # Delete in correct order (respecting foreign keys)
            print("\n🗑️  Deleting booking history...")
            BookingHistory.query.delete()
            db.session.commit()
            
            print("🗑️  Deleting payments...")
            Payment.query.delete()
            db.session.commit()
            
            print("🗑️  Deleting seats...")
            Seat.query.delete()
            db.session.commit()
            
            print("🗑️  Deleting bookings...")
            Booking.query.delete()
            db.session.commit()
            
            print("-" * 50)
            print("✅ All booking history permanently deleted!")
            print("-" * 50)
            
            # Verify deletion
            remaining_bookings = Booking.query.count()
            remaining_seats = Seat.query.count()
            remaining_payments = Payment.query.count()
            remaining_history = BookingHistory.query.count()
            
            print(f"📊 Remaining records:")
            print(f"   • Bookings: {remaining_bookings}")
            print(f"   • Seats: {remaining_seats}")
            print(f"   • Payments: {remaining_payments}")
            print(f"   • Booking History: {remaining_history}")
            
            if remaining_bookings == 0:
                print("\n🎉 Success! All bookings cleared.")
            else:
                print("\n⚠️  Warning: Some records may still remain.")
                
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error: {str(e)}")

if __name__ == '__main__':
    clear_all_bookings()
