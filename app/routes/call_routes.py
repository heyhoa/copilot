from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required
from app import db
from sqlalchemy import text

call_bp = Blueprint('call', __name__)

@call_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        # Test database connection with proper text() wrapper
        db.session.execute(text('SELECT 1'))
        
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

@call_bp.route('/incoming', methods=['POST'])
@jwt_required()
def handle_incoming_call():
    """Handle incoming call webhook from telephony provider"""
    return jsonify({
        "message": "Call received",
        "status": "processing"
    })

@call_bp.route('/stream', methods=['POST'])
@jwt_required()
def handle_audio_stream():
    """Handle incoming audio stream"""
    return jsonify({
        "message": "Audio stream received",
        "status": "processing"
    })