import pytest
from flask import session
from server import find_club_by_name, find_competition_by_name, app, Club, Competition, CompetitionManager, ClubManager

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_login_successful(client):
    response = client.post('/showSummary', data={'email': 'john@simplylift.co'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Welcome, john@simplylift.co" in response.data

def test_logout(client):
    response = client.get('/logout', follow_redirects=True)
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

def test_clubs_view(client):
    response = client.get('/clubs', follow_redirects=True)
    assert response.status_code == 200

def test_past_competition(client, monkeypatch):
    monkeypatch.setattr(CompetitionManager, 'loadCompetitions', lambda self : [
        Competition('Past Competition', '2024-01-01 00:00:00', '30')
    ])

    response = client.get('/book/Past Competition/Test Club')

    assert response.status_code == 200
    assert 'Cannot book places in past competitions' in response.data.decode()

@pytest.fixture
def mock_data(monkeypatch):
    def mock_load_clubs(self):
        return [Club('Test Club', 'test@club.com', '10')]
    def mock_load_competitions(self):
        return [Competition('Test Competition', '2024-06-01 00:00:00', '50')]
    monkeypatch.setattr(ClubManager, 'loadClubs', mock_load_clubs)
    monkeypatch.setattr(CompetitionManager, 'loadCompetitions', mock_load_competitions)

def test_purchase_places(client, mock_data):
    response = client.post('/purchasePlaces', data={
        'club': 'Test Club',
        'competition': 'Test Competition',
        'places': '5'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert 'places successfully booked' in response.data.decode()

def test_not_enough_points(client, mock_data):
    response = client.post('/purchasePlaces', data={
        'club': 'Test Club',
        'competition': 'Test Competition',
        'places': '11'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert 'Club does not have enough points' in response.data.decode()

def test_book_many_places(client, mock_data):
    response = client.post('/purchasePlaces', data={
        'club': 'Test Club',
        'competition': 'Test Competition',
        'places': '15'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert 'Cannot book more than 12 places' in response.data.decode()
