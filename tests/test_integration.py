import pytest
from server import find_club_by_name, find_competition_by_name, app, Club

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_login_successful(client):
    response = client.post('/showSummary', data={'email': 'john@simplylift.co'}, follow_redirects=True)
    assert b"Welcome, john@simplylift.co" in response.data
    assert response.status_code == 200

def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to the GUDLFT Registration Portal!" in response.data

def test_show_summary(client, monkeypatch):
    monkeypatch.setattr('server.find_club_by_email', lambda x: Club('She Lifts', 'kate@shelifts.co.uk', '4'))
    response = client.post('/showSummary', data={'email': 'kate@shelifts.co.uk'})
    assert response.status_code == 200
    assert "She Lifts" in response.data.decode()
    
