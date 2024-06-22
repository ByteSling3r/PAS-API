from flask import Blueprint


programming_bp = Blueprint('programming_bp', __name__)


@programming_bp.route('/api/programmig', methods=['GET'])
def get_programming():
    return {"Hello": "World"}
