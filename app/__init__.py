from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv


def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    load_dotenv()

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)


    @app.route('/')
    def index():
        return render_template('index.html')


    class DeviceState(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        device_name = db.Column(db.String(50), unique=True, nullable=False)
        state = db.Column(db.String(10), nullable=False)

        def __repr__(self):
            return f'<DeviceState {self.device_name}: {self.state}>'


    @app.route('/api/state', methods=['GET'])
    def get_state():
        device_states = DeviceState.query.all()
        state_dict = {device.device_name: device.state for device in device_states}
        return jsonify(state_dict)


    @app.route('/api/state', methods=['PUT'])
    def set_state():
        data = request.json
        for device_name, state in data.items():
            device = DeviceState.query.filter_by(device_name=device_name).first()
            if device:
                device.state = state
            else:
                new_device = DeviceState(device_name=device_name, state=state)
                db.session.add(new_device)
        db.session.commit()
        return jsonify({"message": "Device states updated successfully"})
    return app

