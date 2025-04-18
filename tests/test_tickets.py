def test_create_ticket_unauthorized(client):
    """Test creating ticket without authentication."""
    response = client.post('/api/tickets/', json={
        'name': 'Test User',
        'phone': '1234567890',
        'address': '123 Test St',
        'reason': 'Test reason'
    })
    assert response.status_code == 401

def test_create_ticket(client, test_user):
    """Test creating ticket with authentication."""
    # First login to get token
    login_response = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'testpass'
    })
    token = login_response.json['access_token']
    
    # Create ticket with token
    response = client.post('/api/tickets/', 
        json={
            'name': 'Test User',
            'phone': '1234567890',
            'address': '123 Test St',
            'reason': 'Test reason'
        },
        headers={'Authorization': f'Bearer {token}'}
    )
    
    # Print response data for debugging
    print(f"\nResponse Status: {response.status_code}")
    print(f"Response Body: {response.get_json()}")
    
    assert response.status_code == 201
    assert response.json['status'] == 'success'
    assert 'ticket_id' in response.json 