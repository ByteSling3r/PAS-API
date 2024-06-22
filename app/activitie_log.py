from flask import Blueprint, jsonify
from datetime import datetime

activities_bp = Blueprint('activities_bp', __name__)


@activities_bp.route('/api/activities', methods=['GET'])
def get_activities():
    return jsonify({
        '2024-06-19': {

            'Light': {
                'date': datetime.now().strftime("%H:%M"),
                'state': 'OFF'
            },
            'air': {
                'date': datetime.now().strftime("%H:%M"),
                'state': 'OFF'
            }
        },
        '2024-06-18': {
            'Light': {
                'date': '20:40:33',
                'state': 'ON'
            },
            'Light': {
                'date': datetime.now().strftime("%H:%M"),
                'state': 'OFF'
            },
            'air': {
                'date': datetime.now().strftime("%H:%M"),
                'state': 'OFF'
            }
        }
    })