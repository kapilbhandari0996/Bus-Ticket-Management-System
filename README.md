# LETS GO Bus Service - Backend

A Python Flask backend for the LETS GO Bus Ticket Management System with PostgreSQL database.

## Features

- **User Authentication**: Register, login, JWT-based authentication
- **Bus Search**: Search buses by route, date, type (AC/Non-AC), and price range
- **Seat Selection**: Real-time seat availability and selection
- **Booking Management**: Create, view, and cancel bookings
- **Payment Integration**: UPI QR code payment with transaction tracking
- **E-Ticket Generation**: PDF ticket download with booking details

## Tech Stack

- **Backend**: Python 3.x, Flask, Flask-RESTful
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT (JSON Web Tokens)
- **PDF Generation**: ReportLab

## Prerequisites

- Python 3.8 or higher
- PostgreSQL 12 or higher
- pip (Python package manager)

## Installation

### 1. Install PostgreSQL

Download and install PostgreSQL from: https://www.postgresql.org/download/

### 2. Create Database

Open pgAdmin or use psql command line:

```sql
CREATE DATABASE lets_go_bus;
```

### 3. Clone/Navigate to Project

```bash
cd D:\PROJECT\backend
```

### 4. Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure Environment Variables

Edit the `.env` file in the backend directory:

```env
SECRET_KEY=your-secret-key-change-in-production
JWT_SECRET_KEY=your-jwt-secret-key-change-in-production
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/lets_go_bus
```

Replace `your_password` with your PostgreSQL password.

### 7. Initialize Database

```bash
python init_db.py
```

This will:
- Create all database tables
- Seed initial routes and buses
- Create a demo user (john@example.com / password123)

### 8. Run the Backend Server

```bash
python app.py
```

The server will start at: http://localhost:5000

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | Login user |
| GET | `/api/auth/me` | Get current user (requires auth) |
| PUT | `/api/auth/profile` | Update profile (requires auth) |

### Buses

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/buses/search` | Search buses |
| GET | `/api/buses/locations` | Get all locations |
| GET | `/api/buses/<id>` | Get bus details |
| GET | `/api/buses/<id>/seats` | Get available seats |
| GET | `/api/buses/routes` | Get all routes |

### Bookings

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/bookings` | Create booking (requires auth) |
| GET | `/api/bookings/my-bookings` | Get user bookings (requires auth) |
| GET | `/api/bookings/<id>` | Get booking details (requires auth) |
| POST | `/api/bookings/<id>/cancel` | Cancel booking (requires auth) |
| GET | `/api/bookings/<ref>` | Get booking by reference |

### Payment

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/payment/initiate` | Initiate payment (requires auth) |
| POST | `/api/payment/confirm` | Confirm payment (requires auth) |
| GET | `/api/payment/<id>/status` | Get payment status |
| GET | `/api/payment/<id>/ticket/pdf` | Download ticket PDF |

## API Usage Examples

### Register User

```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "John Doe",
    "email": "john@example.com",
    "password": "password123",
    "phone": "9876543210"
  }'
```

### Login

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "password123"
  }'
```

### Search Buses

```bash
curl "http://localhost:5000/api/buses/search?start=Pune Station&destination=Hinjewadi&date=2024-03-25"
```

### Create Booking

```bash
curl -X POST http://localhost:5000/api/bookings \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "bus_id": 1,
    "travel_date": "2024-03-25",
    "seats": [1, 3, 4],
    "passenger_name": "John Doe",
    "passenger_email": "john@example.com",
    "passenger_phone": "9876543210"
  }'
```

## Frontend Integration

The frontend files are located in `D:\PROJECT\frontend\` and are already configured to connect to the backend API.

To use the frontend:

1. Make sure the backend server is running
2. Open `index.html` in a web browser
3. Register or login with the demo account
4. Start booking bus tickets!

## Default Demo Account

After running `init_db.py`, you can login with:

- **Email**: john@example.com
- **Password**: password123

## Database Schema

### Tables

- **users**: User accounts
- **routes**: Bus routes (start/destination)
- **buses**: Bus details and schedules
- **bookings**: Ticket bookings
- **seats**: Seat assignments
- **payments**: Payment transactions

## Troubleshooting

### Database Connection Error

- Verify PostgreSQL is running
- Check DATABASE_URL in `.env`
- Ensure database `lets_go_bus` exists

### Port Already in Use

Change the port in `app.py`:

```python
app.run(debug=True, port=5001)  # Use port 5001 instead
```

### Module Not Found

Make sure virtual environment is activated and dependencies are installed:

```bash
pip install -r requirements.txt
```

## Security Notes

- Change `SECRET_KEY` and `JWT_SECRET_KEY` in production
- Use HTTPS in production
- Implement rate limiting for production
- Add CORS origins for specific domains

## License

MIT License

## Support

For issues or questions, please create an issue in the project repository.
