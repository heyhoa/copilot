def test_health_check(client):
    """Test health check endpoint."""
    response = client.get('/api/calls/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'
    assert response.json['database'] == 'connected' 