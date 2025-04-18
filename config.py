import os
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-very-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///voice_agent.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'another-secret-key'
    LOG_FILE = 'logs/voice_agent.log'

    # LiveKit Configuration
    LIVEKIT_API_KEY = os.environ.get('LIVEKIT_API_KEY')
    LIVEKIT_API_SECRET = os.environ.get('LIVEKIT_API_SECRET')
    LIVEKIT_HOST = os.environ.get('LIVEKIT_HOST')

    # AI Service Keys
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    CARTESIA_API_KEY = os.environ.get('CARTESIA_API_KEY')
    # Add others as needed
    # DEEPGRAM_API_KEY = os.environ.get('DEEPGRAM_API_KEY')

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), '../dev.db')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite://' # In-memory SQLite for tests
    WTF_CSRF_ENABLED = False
    # Use mock/test keys for testing if real keys aren't available/desired
    LIVEKIT_API_KEY = os.environ.get('LIVEKIT_API_KEY', 'test_api_key')
    LIVEKIT_API_SECRET = os.environ.get('LIVEKIT_API_SECRET', 'test_api_secret')
    LIVEKIT_HOST = os.environ.get('LIVEKIT_HOST', 'ws://localhost:7880')
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', 'test_openai_key')
    CARTESIA_API_KEY = os.environ.get('CARTESIA_API_KEY', 'test_cartesia_key')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), '../data.sqlite')
    # Add any production-specific settings here

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
