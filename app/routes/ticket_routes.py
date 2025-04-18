from flask import Blueprint, request, jsonify, current_app
from app.models.ticket import Ticket
from app import db
from app.utils.error_handlers import APIError

ticket_bp = Blueprint('ticket', __name__)

@ticket_bp.route('/', methods=['POST'])
def create_ticket():
    """Create a new support ticket"""
    try:
        data = request.get_json()
        if not data:
            raise APIError('No data provided', status_code=400)
            
        required_fields = ['name', 'phone', 'address', 'reason']
        for field in required_fields:
            if field not in data:
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
        
        current_app.logger.info(f'Created ticket {ticket.id} for {ticket.name}')
        
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
        raise APIError('Internal server error', status_code=500)

@ticket_bp.route('/', methods=['GET'])
def get_tickets():
    """Get all tickets"""
    return jsonify({
        "tickets": []
    })