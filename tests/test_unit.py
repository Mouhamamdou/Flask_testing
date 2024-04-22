import pytest
from server import ClubManager, CompetitionManager, Club, Competition, app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def init_club_manager(monkeypatch):
    def mock_load_clubs(self):
        return [Club('Test Club', 'test@example.com', '10')]
    monkeypatch.setattr(ClubManager, 'loadClubs', mock_load_clubs)

@pytest.fixture
def init_competition_manager(monkeypatch):
    def mock_load_competitions(self):
        return [Competition('Test Competition', '2024-01-01 00:00:00', '5')]
    monkeypatch.setattr(CompetitionManager, 'loadCompetitions', mock_load_competitions)


def test_club_loading(client, init_club_manager):
    club_manager = ClubManager()
    clubs = club_manager.loadClubs()
    assert clubs[0].name == 'Test Club'
    assert clubs[0].email == 'test@example.com'
    assert clubs[0].points == '10'

def test_competition_loading(client, init_competition_manager):
    competition_manager = CompetitionManager()
    competitions = competition_manager.loadCompetitions()
    assert competitions[0].name == 'Test Competition'
    assert competitions[0].date == '2024-01-01 00:00:00'
    assert competitions[0].nb_of_places == '5'
