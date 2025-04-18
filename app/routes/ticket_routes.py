from flask import Blueprint, request, jsonify

ticket_bp = Blueprint('ticket', __name__)

@ticket_bp.route('/', methods=['POST'])
def create_ticket():
    """Create a new support ticket"""
    return jsonify({
        "message": "Ticket created",
        "ticket_id": "123"
    })

@ticket_bp.route('/', methods=['GET'])
def get_tickets():
    """Get all tickets"""
    return jsonify({
        "tickets": []
    })