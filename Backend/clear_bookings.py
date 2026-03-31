"""
Clear All Bookings Script
This script removes all booking history from the database permanently.
Run this script to reset all bookings, seats, payments, and booking history.
"""

import sys
import os

# Add parent directory to path to import models
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db, Booking, Seat, Payment, BookingHistory

def clear_all_bookings():
    """Delete all bookings and related data from the database"""
    
    app = create_app()
    
    with app.app_context():
        print("🗑️  Starting to clear all booking history...")
        print("-" * 50)
        
        try:
            # Count records before deletion
            bookings_count = Booking.query.count()
            seats_count = Seat.query.count()
            payments_count = Payment.query.count()
            history_count = BookingHistory.query.count()
            
            print(f"📊 Current records:")
            print(f"   • Bookings: {bookings_count}")
            print(f"   • Seats: {seats_count}")
            print(f"   • Payments: {payments_count}")
            print(f"   • Booking History: {history_count}")
            print("-" * 50)
            
            if bookings_count == 0:
                print("✅ No bookings to delete. Database is already clean!")
                return
            
            # Confirm deletion
            print("⚠️  WARNING: This action is PERMANENT and cannot be undone!")
            confirm = input("Type 'YES' to confirm deletion of all bookings: ")
            
            if confirm != 'YES':
                print("❌ Deletion cancelled.")
                return
            
            # Delete in correct order (respecting foreign keys)
            print("\n🗑️  Deleting booking history...")
            BookingHistory.query.delete()
            db.session.commit()
            print("   ✓ Booking history deleted")
            
            print("🗑️  Deleting payments...")
            Payment.query.delete()
            db.session.commit()
            print("   ✓ Payments deleted")
            
            print("🗑️  Deleting seats...")
            Seat.query.delete()
            db.session.commit()
            print("   ✓ Seats deleted")
            
            print("🗑️  Deleting bookings...")
            Booking.query.delete()
            db.session.commit()
            print("   ✓ Bookings deleted")
            
            print("-" * 50)
            print("✅ All booking history has been permanently deleted!")
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
            
            if remaining_bookings == 0 and remaining_seats == 0 and remaining_payments == 0:
                print("\n🎉 Success! Database is now clean.")
            else:
                print("\n⚠️  Warning: Some records may still remain.")
                
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error occurred: {str(e)}")
            print("Database has been rolled back. No changes made.")

if __name__ == '__main__':
    clear_all_bookings()
