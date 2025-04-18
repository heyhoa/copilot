import pytest
from jose import jwt # To decode the token for basic validation
# No need for AudioService import if only testing the route
# from app.services.audio_service import AudioService

# REMOVE the @pytest.mark.asyncio marker
# @pytest.mark.asyncio

# The test function is now synchronous
def test_join_call_room(client, test_user): # client is the standard Flask test client
    """Test generating a join token for a LiveKit room"""
    # 1. Login to get JWT token
    login_response = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'testpass'
    })
    assert login_response.status_code == 200
    auth_token = login_response.json['access_token']

    # 2. Request to join a call room for a specific ticket
    ticket_id = 'test_ticket_123'
    response = client.post('/api/calls/join',
        json={
            'ticket_id': ticket_id,
            # participant_name is now derived from JWT identity server-side
        },
        headers={'Authorization': f'Bearer {auth_token}'}
    )

    # 3. Assertions
    assert response.status_code == 200
    response_data = response.json
    assert response_data['status'] == 'success'
    assert response_data['room_name'] == f"ticket_{ticket_id}"
    assert 'token' in response_data
    assert 'ws_url' in response_data # Check if ws_url is returned

    # 4. Optional: Basic validation of the generated LiveKit token (decoding)
    # Note: This doesn't verify against LiveKit, just checks structure/claims
    try:
        # We don't have the secret to fully verify, but can decode headers/payload
        # Use verify=False option if available or just decode unsecured
        # For python-jose, decoding without verification isn't straightforward.
        # A simple check is that the token is a non-empty string.
        assert isinstance(response_data['token'], str) and len(response_data['token']) > 0
        # If you want deeper validation, you might need the PyJWT library
        # or implement more complex mocking.
    except Exception as e:
        pytest.fail(f"Generated LiveKit token is not a valid JWT format: {e}")

# Remove or comment out the old test_create_call_room
# def test_create_call_room(client, test_user): ... 