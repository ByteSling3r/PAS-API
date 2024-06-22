from flask import Blueprint, jsonify, request
from .models import DeviceState
from .database import db

state_bp = Blueprint('state', __name__)


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
            device.state = state
        else:
            new_device = DeviceState(device_name=device_name, state=state)
            db.session.add(new_device)
    db.session.commit()
    return jsonify({"message": "Device states updated successfully"})
