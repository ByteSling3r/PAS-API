from flask import Flask, render_template
from flask_cors import CORS
from .database import db, migrate
import os
from flask_bootstrap import Bootstrap
from dotenv import load_dotenv
from .device_state import state_bp
from .activitie_log import activities_bp
from .models import initialize_default_devices
from .socketio import socketio
from .scheduler import create_scheduler  # Importamos la función para crear el scheduler

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    bootstrap = Bootstrap(app)
    socketio.init_app(app)
    load_dotenv()

    # Blueprints
    app.register_blueprint(state_bp)
    app.register_blueprint(activities_bp)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    migrate.init_app(app, db)

    @app.before_request
    def setup_defaults():
        db.create_all()
        initialize_default_devices()

    # Inicializamos y adjuntamos el scheduler a la aplicación
    app.scheduler = create_scheduler(app)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.errorhandler(404)
    def not_found(error):
        return render_template('error404.html'), 404

    return app
