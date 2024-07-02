from flask import Blueprint, jsonify, request, current_app
from .models import DeviceState, DeviceStateChange, DeviceProgramming
from .database import db
from datetime import datetime
import pytz
from .socketio import socketio
from .scheduler import job_wrapper


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


@state_bp.route('/api/programming', methods=['POST'])
def program_device():
    data = request.json
    device_name = data['device_name']
    on_time = data['on_time']
    off_time = data['off_time']

    new_programming = DeviceProgramming(device_name=device_name, on_time=on_time, off_time=off_time)
    db.session.add(new_programming)
    db.session.commit()

    current_app.scheduler.remove_all_jobs()

    current_app.scheduler.add_job(func=job_wrapper, args=[device_name, 'ON'], trigger='cron', hour=int(on_time.split(':')[0]), minute=int(on_time.split(':')[1]), id=f'{device_name}_on')
    current_app.scheduler.add_job(func=job_wrapper, args=[device_name, 'OFF'], trigger='cron', hour=int(off_time.split(':')[0]), minute=int(off_time.split(':')[1]), id=f'{device_name}_off')

    if not device_name or not on_time or not off_time:
        return jsonify({'error': 'Missing required fields'}), 400
    return jsonify({'message': 'Programming successful'}), 200
