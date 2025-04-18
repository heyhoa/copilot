from flask import Blueprint, request, jsonify

main = Blueprint('main', __name__)

@main.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Voice Agent API is running."})

@main.route("/ticket", methods=["POST"])
def create_ticket():
    data = request.json
    # For now, just echo the data back
    return jsonify({
        "status": "received",
        "data": data
    })
