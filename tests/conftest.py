import pytest
from app import create_app, db
from app.models.user import User

# Use a testing configuration if available
TESTING_CONFIG = 'testing' # Or 'default' or your config name

@pytest.fixture(scope='session')
def app():
    """Session-wide test Flask application."""
    _app = create_app(TESTING_CONFIG)
    with _app.app_context():
        # Create all database tables within the app context for the session
        db.create_all()
        yield _app
        # Drop all database tables after the session ends
        db.drop_all()

@pytest.fixture(scope='function')
def client(app):
    """Flask test client provided by pytest-flask."""
    # The app context is already active from the 'app' fixture
    return app.test_client()

@pytest.fixture(scope='function')
def test_user(app):
    """Create a test user in the database for authentication."""
    # The app context is managed by the 'app' fixture scope
    # Check if user exists first to avoid errors on re-runs within session
    user = User.query.filter_by(username='testuser').first()
    if not user:
        user = User(username='testuser')
        user.set_password('testpass') # Make sure you have a set_password method
        db.session.add(user)
        db.session.commit()
    else:
        # Ensure password is set if user already exists (e.g., from previous failed test run)
         user.set_password('testpass')
         db.session.commit()

    yield user # Provide the user object to the test

    # Clean up the user after the test function by deleting it
    # Using merge() handles potential session state issues if the object was detached
    user = db.session.merge(user)
    db.session.delete(user)
    db.session.commit()

# Remove any httpx or asgi-lifespan related fixtures if they were added 