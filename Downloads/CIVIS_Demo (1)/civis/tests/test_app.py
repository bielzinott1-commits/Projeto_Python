from app.models import Occurrence
from app.extensions import db

def login(client):
    return client.post("/login", data={"username":"tester", "password":"uma-senha-de-teste-longa"}, follow_redirects=True)

def test_dashboard_requires_login(client):
    response = client.get("/dashboard")
    assert response.status_code in (302, 401)

def test_login_and_dashboard(client):
    response = login(client)
    assert response.status_code == 200
    assert b"Dashboard" in response.data

def test_create_occurrence_persists(app, client):
    login(client)
    response = client.post("/ocorrencias/nova", data={"title":"Registro fictício", "category":"Demonstrativo", "description":"Dados de teste"}, follow_redirects=True)
    assert response.status_code == 200
    with app.app_context():
        assert Occurrence.query.count() == 1
