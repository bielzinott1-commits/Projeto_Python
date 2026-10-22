import pytest
from app import create_app
from app.extensions import db
from app.models import User

@pytest.fixture()
def app():
    app = create_app({"TESTING": True, "WTF_CSRF_ENABLED": False, "SQLALCHEMY_DATABASE_URI": "sqlite://"})
    with app.app_context():
        db.create_all()
        user = User(username="tester", role="administrador")
        user.set_password("uma-senha-de-teste-longa")
        db.session.add(user)
        db.session.commit()
    yield app
    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture()
def client(app):
    return app.test_client()
