from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://localhost/kmetric')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'super-secret-key')

    db.init_app(app)
    migrate.init_app(app, db)

    frontend_origins = [
        os.getenv('FRONTEND_ORIGIN', 'http://localhost:5173'),
        'http://127.0.0.1:5173',
    ]
    CORS(
        app,
        resources={r"/*": {"origins": frontend_origins}},
        supports_credentials=True,
        methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'],
        allow_headers=['Content-Type', 'Authorization'],
    )

    with app.app_context():
        from .routes import auth, dashboard
        app.register_blueprint(auth.bp)
        app.register_blueprint(dashboard.bp)

    return app
