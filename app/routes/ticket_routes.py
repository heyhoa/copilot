from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.ticket import Ticket
from app import db
from app.utils.error_handlers import APIError

ticket_bp = Blueprint('ticket', __name__)

@ticket_bp.route('/', methods=['POST'])
@jwt_required()
def create_ticket():
    """Create a new support ticket"""
    try:
        # Get the current user ID from the JWT token
        current_user_id = get_jwt_identity()
        
        data = request.get_json()
        current_app.logger.info(f"Received ticket data: {data}")
        
        if not data:
            raise APIError('No data provided', status_code=400)
            
        required_fields = ['name', 'phone', 'address', 'reason']
        for field in required_fields:
            if field not in data:
                current_app.logger.warning(f"Missing required field: {field}")
                raise APIError(f'Missing required field: {field}', status_code=400)
        
        ticket = Ticket(
            name=data['name'],
            phone=data['phone'],
            email=data.get('email'),
            address=data['address'],
            reason=data['reason']
        )
        
        db.session.add(ticket)
        db.session.commit()
        
        current_app.logger.info(f'Created ticket {ticket.id} for {ticket.name} by user {current_user_id}')
        
        return jsonify({
            "status": "success",
            "message": "Ticket created",
            "ticket_id": ticket.id
        }), 201
        
    except APIError as e:
        current_app.logger.warning(f'API Error in create_ticket: {str(e)}')
        raise
    except Exception as e:
        current_app.logger.error(f'Unexpected error in create_ticket: {str(e)}')
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 422

@ticket_bp.route('/', methods=['GET'])
@jwt_required()
def get_tickets():
    """Get all tickets"""
    tickets = Ticket.query.all()
    return jsonify({
        "tickets": [ticket.to_dict() for ticket in tickets]
    })