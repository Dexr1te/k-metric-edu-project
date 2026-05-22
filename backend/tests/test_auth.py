import pytest
from app import create_app, db
from app.models import User

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })

    with app.app_context():
        db.create_all()
        yield app
        # EDU: SQLite не поддерживает DROP VIEW через SQLAlchemy drop_all() для моделей-вью.
        # Поэтому мы просто закрываем сессию, а память очистится сама.
        db.session.remove()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

def test_user_password_hashing():
    """EDU: Тестируем, что пароли не хранятся в открытом виде."""
    user = User(username='test_hash')
    user.set_password('secret')
    assert user.password_hash != 'secret'
    assert user.check_password('secret') is True
    assert user.check_password('wrong') is False

def test_register(client):
    """EDU: Тестируем API регистрации пользователя."""
    response = client.post('/auth/register', json={
        'username': 'unique_user',
        'password': 'password123'
    })
    assert response.status_code == 201
    assert b'User created successfully' in response.data

def test_login(client):
    """EDU: Тестируем получение JWT токена."""
    # Сначала регистрируем
    client.post('/auth/register', json={
        'username': 'loginuser',
        'password': 'password123'
    })
    
    # Пытаемся войти
    response = client.post('/auth/login', json={
        'username': 'loginuser',
        'password': 'password123'
    })
    assert response.status_code == 200
    assert 'token' in response.get_json()
