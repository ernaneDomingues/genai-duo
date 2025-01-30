from flask import Blueprint, jsonify

api_bp = Blueprint('api', __name__)

@api_bp.route('/ask', methods=['POST'])
def ask():
    return jsonify({"message": "API funcionando!"})