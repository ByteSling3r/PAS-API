from flask import Blueprint, jsonify, request
from .models import DeviceState, DeviceStateChange
from .database import db
from datetime import datetime
import pytz
from .socketio import socketio

state_bp = Blueprint('state', __name__)


def current_date_colombia():
    colombia_tz = pytz.timezone('America/Bogota')
    return datetime.now(colombia_tz).date()


def current_time_colombia():
    colombia_tz = pytz.timezone('America/Bogota')
    return datetime.now(colombia_tz).time().strftime("%I:%M:%S %p")


@state_bp.route('/api/state', methods=['GET'])
def get_state():
    device_states = DeviceState.query.all()
    state_dict = {device.device_name: device.state for device in device_states}
    return jsonify(state_dict)


@state_bp.route('/api/state', methods=['PUT'])
def set_state():
    data = request.json
    for device_name, state in data.items():
        device = DeviceState.query.filter_by(device_name=device_name).first()
        if device:
            if device.state != state:
                device.state = state
                if device_name in ["Light", "air"]:
                    new_record = DeviceStateChange(device=device_name,
                                                   state=state,
                                                   time=current_time_colombia(),
                                                   date=current_date_colombia())
                    db.session.add(new_record)
        else:
            new_device = DeviceState(device_name=device_name, state=state)
            db.session.add(new_device)
            if device_name in ["Light", "air"]:
                new_record = DeviceStateChange(device=device_name,
                                               state=state,
                                               time=current_time_colombia(),
                                               date=current_date_colombia())
                db.session.add(new_record)

    db.session.commit()
    socketio.emit('state_updated', data)
    return jsonify({"message": "Device states updated successfully"}), 200
