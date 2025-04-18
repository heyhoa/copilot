from flask import Blueprint, request, jsonify

call_bp = Blueprint('call', __name__)

@call_bp.route('/incoming', methods=['POST'])
def handle_incoming_call():
    """Handle incoming call webhook from telephony provider"""
    return jsonify({
        "message": "Call received",
        "status": "processing"
    })

@call_bp.route('/stream', methods=['POST'])
def handle_audio_stream():
    """Handle incoming audio stream"""
    return jsonify({
        "message": "Audio stream received",
        "status": "processing"
    })