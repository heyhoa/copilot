import pytest
from app import create_app, db
from app.models.user import User

@pytest.fixture
def app():
    """Create application for the tests."""
    app = create_app('testing')
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'
    })
    
    # Setup test database
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Test client for the application."""
    return app.test_client()

@pytest.fixture
def test_user(app):
    """Create test user."""
    with app.app_context():
        user = User(username='testuser')
        user.set_password('testpass')
        db.session.add(user)
        db.session.commit()
        return user 