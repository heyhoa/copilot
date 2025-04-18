from flask import Blueprint, request, jsonify, current_app
from app import db

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

@call_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        db.session.execute('SELECT 1')
        
        return jsonify({
            "status": "healthy",
            "message": "Service is running",
            "database": "connected"
        })
    except Exception as e:
        current_app.logger.error(f'Health check failed: {str(e)}')
        return jsonify({
            "status": "unhealthy",
            "message": "Service issues detected",
            "database": "disconnected"
        }), 503