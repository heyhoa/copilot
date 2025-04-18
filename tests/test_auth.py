def test_register(client):
    """Test user registration."""
    response = client.post('/api/auth/register', json={
        'username': 'newuser',
        'password': 'newpass'
    })
    assert response.status_code == 201
    assert response.json['status'] == 'success'

def test_login(client, test_user):
    """Test user login."""
    response = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'testpass'
    })
    assert response.status_code == 200
    assert 'access_token' in response.json

def test_invalid_login(client, test_user):
    """Test invalid login credentials."""
    response = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'wrongpass'
    })
    assert response.status_code == 401 