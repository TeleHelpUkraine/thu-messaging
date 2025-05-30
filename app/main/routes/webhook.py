from flask import Blueprint, request, jsonify

webhook_bp = Blueprint('webhook', __name__)

@webhook_bp.route('/webhook', methods=['POST'])
def receive():
    data = request.get_json()
    return jsonify({'status': 'received'})

