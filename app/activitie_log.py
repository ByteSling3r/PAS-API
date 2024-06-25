from flask import Blueprint, jsonify
from .models import DeviceStateChange

activities_bp = Blueprint('activities_bp', __name__)


@activities_bp.route('/api/state/log', methods=['GET'])
def get_state_changes():
    records = DeviceStateChange.query.all()
    results = [
        {
            "device": record.device,
            "state": record.state,
            "time": record.time.strftime("%I:%M:%S %p") if record.time else None,
            "date": record.date.strftime("%Y-%m-%d") if record.date else None
        } for record in records
    ]
    return jsonify(results), 200
