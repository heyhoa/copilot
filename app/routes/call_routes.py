from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from sqlalchemy import text
import livekit.api as api
import uuid

call_bp = Blueprint('call', __name__)

@call_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        # Test database connection with proper text() wrapper
        db.session.execute(text('SELECT 1'))
        
        # Check LiveKit API credentials presence (optional but good practice)
        api_key = current_app.config.get('LIVEKIT_API_KEY')
        api_secret = current_app.config.get('LIVEKIT_API_SECRET')
        livekit_host = current_app.config.get('LIVEKIT_HOST')

        if not all([api_key, api_secret, livekit_host]):
             current_app.logger.warning("LiveKit configuration missing in health check.")
             # Decide if this should make the health check fail or just warn
             # return jsonify({"status": "unhealthy", "message": "LiveKit config missing"}), 503

        return jsonify({
            "status": "healthy",
            "message": "Service is running",
            "database": "connected",
            "livekit_config": "present" if all([api_key, api_secret, livekit_host]) else "missing"
        })
    except Exception as e:
        current_app.logger.error(f'Health check failed: {str(e)}', exc_info=True)
        return jsonify({
            "status": "unhealthy",
            "message": f"Service issues detected: {str(e)}",
            "database": "error"
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
async def handle_audio_stream():
    """Handle incoming audio stream"""
    try:
        room_name = request.json.get('room_name')
        token = request.json.get('token')
        
        # Connect to room and handle audio
        room = await audio_service.connect_to_room(room_name, token)
        
        return jsonify({
            'status': 'success',
            'message': 'Audio stream processing started'
        })
        
    except Exception as e:
        current_app.logger.error(f'Error handling audio stream: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

def create_participant_token(room_name, participant_identity):
    """Helper function to create a LiveKit token for a participant."""
    api_key = current_app.config['LIVEKIT_API_KEY']
    api_secret = current_app.config['LIVEKIT_API_SECRET']

    if not api_key or not api_secret:
        current_app.logger.error("LiveKit API Key or Secret not configured.")
        raise ValueError("LiveKit credentials not configured.")

    try:
        # Grant permissions for a user joining the call
        grant = api.VideoGrants(
            room=room_name,
            room_join=True,
            can_publish=True,
            can_subscribe=True,
            can_publish_data=True,
            # Add other permissions as needed
        )

        # Use the builder pattern based on documentation examples
        token_builder = api.AccessToken(api_key, api_secret)
        token = (
            token_builder
            .with_identity(participant_identity)
            # Use with_grants (plural) to add the grant object
            .with_grants(grant)
            # Optionally set name and metadata if needed
            # .with_name("Participant Name")
            # .with_metadata('{"role": "user"}')
            .to_jwt() # Generate the JWT token string
        )
        return token

    except Exception as e:
        # Log the specific error during token creation
        current_app.logger.error(f"Error creating LiveKit token: {str(e)}", exc_info=True)
        # Re-raise as a ConnectionError for the route handler to catch
        raise ConnectionError(f"Failed to generate LiveKit token: {str(e)}")

@call_bp.route('/join', methods=['POST'])
@jwt_required()
async def join_call_room():
    """Generate a token for the authenticated user to join a call room."""
    try:
        user_identity_from_jwt = get_jwt_identity() # Get user ID (e.g., primary key) from JWT
        ticket_id = request.json.get('ticket_id')

        if not ticket_id:
            current_app.logger.warning("Join call request missing ticket_id")
            return jsonify({'status': 'error', 'message': 'ticket_id is required'}), 400

        # Define room name based on ticket_id
        room_name = f"ticket_{ticket_id}"
        # Define participant identity (ensure it's unique and useful)
        # Using "user_" prefix + JWT identity (which should be the user's ID)
        participant_identity = f"user_{user_identity_from_jwt}"

        current_app.logger.info(f"Join request for room '{room_name}' by participant '{participant_identity}' (JWT sub: {user_identity_from_jwt})")

        # Generate the token using the updated helper function
        token = create_participant_token(room_name, participant_identity)

        # Return the token and connection details to the client
        # Ensure LIVEKIT_HOST is the correct config variable name used in config.py
        # It should be the base host (e.g., your-project.livekit.cloud),
        # the client SDK typically constructs the ws(s):// URL.
        livekit_host_url = current_app.config.get('LIVEKIT_HOST')
        if not livekit_host_url:
             current_app.logger.error("LIVEKIT_HOST is not configured in the application.")
             raise ValueError("LiveKit host URL configuration is missing.")

        return jsonify({
            'status': 'success',
            'room_name': room_name,
            'token': token,
            'ws_url': livekit_host_url # Send Host URL to client
        })

    except ValueError as e: # Catch config errors (e.g., missing keys, missing host)
         current_app.logger.error(f'Configuration error for call join: {str(e)}', exc_info=True)
         return jsonify({
             'status': 'error',
             'message': str(e)
         }), 500 # Use 500 for server config issues
    except ConnectionError as e: # Catch token generation errors
         current_app.logger.error(f'LiveKit token error for call join: {str(e)}', exc_info=True)
         # This error originates from create_participant_token failure
         return jsonify({
             'status': 'error',
             'message': str(e) # The message already includes "Failed to generate..."
         }), 500 # Use 500 for external service interaction failure
    except Exception as e:
        # Catch any other unexpected errors
        current_app.logger.error(f'Unexpected error generating join token: {str(e)}', exc_info=True)
        return jsonify({
            'status': 'error',
            'message': 'An unexpected server error occurred while preparing the call.'
        }), 500