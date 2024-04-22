import pytest
from server import find_club_by_name, find_competition_by_name, app
"""
@pytest.fixture
def clubs():
    return loadClubs()

@pytest.fixture
def competitions():
    return loadCompetitions()

def test_find_club_by_name(clubs):
    club = find_club_by_name("Simply Lift")
    assert club is not None
    assert club['name'] == "Simply Lift"

def test_find_club_by_name_not_found(clubs):
    club = find_club_by_name("Non Existent Club")
    assert club is None

def test_find_competition_by_name(competitions):
    competition = find_competition_by_name("Spring Festival")
    assert competition is not None
    assert competition['name'] == "Spring Festival"

def test_find_competition_by_name_not_found(competitions):
    competition = find_competition_by_name("Non Existent Competition")
    assert competition is None
"""
