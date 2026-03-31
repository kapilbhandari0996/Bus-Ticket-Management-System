from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    db.init_app(app)
    jwt = JWTManager(app)
    
    # Register blueprints
    from routes.auth import auth_bp
    from routes.buses import buses_bp
    from routes.bookings import bookings_bp
    from routes.payment import payment_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(buses_bp, url_prefix='/api/buses')
    app.register_blueprint(bookings_bp, url_prefix='/api/bookings')
    app.register_blueprint(payment_bp, url_prefix='/api/payment')
    
    @app.route('/')
    def index():
        return jsonify({'message': 'Welcome to Let\'s Go Bus API', 'endpoints': {
            'health': '/api/health',
            'auth': '/api/auth',
            'buses': '/api/buses',
            'bookings': '/api/bookings',
            'payment': '/api/payment'
        }})

    @app.route('/api/health')
    def health_check():
        return jsonify({'status': 'healthy', 'message': 'Backend is running!'})

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
