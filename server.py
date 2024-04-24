import json
from flask import Flask,render_template,request,redirect,flash,url_for
from datetime import datetime
import os


class Club:
    def __init__(self, name, email, points):
        self.name = name
        self.email = email
        self.points = points

    def to_dict(self):
        return {
            'name':self.name,
            'email':self.email,
            'points':self.points
        }

class Competition:
    def __init__(self, name, date, nb_of_places):
        self.name = name
        self.date = date
        self.nb_of_places = nb_of_places

    def to_dict(self):
        return {
            'name':self.name,
            'date':self.date,
            'nb_of_places':self.nb_of_places
        }
class ClubManager:
    def __init__(self):
        self.clubs = []
        self.loadClubs()

    def loadClubs(self):
        self.clubs = []
        base_dir = os.path.dirname(os.path.abspath(__file__))
        clubs_file = os.path.join(base_dir, 'clubs.json')
        with open(clubs_file) as c:
             clubs = json.load(c)['clubs']
             for data in clubs:
                 self.clubs.append(Club(**data))
        return self.clubs

    def saveClubs(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        clubs_file = os.path.join(base_dir, 'clubs.json')
        with open(clubs_file, 'w') as c:
            json.dump({'clubs': [club.to_dict() for club in self.clubs]}, c, indent=4)

    def update_club_points(self, club_name, points_change):
        club = next((club for club in self.clubs if club.name == club_name), None)
        if club is not None:
            club.points = points_change

class CompetitionManager:
    def __init__(self):
        self.competitions = []
        self.loadCompetitions()

    def loadCompetitions(self):
        self.competitions = []
        base_dir = os.path.dirname(os.path.abspath(__file__))
        competitions_file = os.path.join(base_dir, 'competitions.json')
        with open(competitions_file) as comps:
             competitions = json.load(comps)['competitions']
             for data in competitions:
                 self.competitions.append(Competition(**data))
        return self.competitions

    def saveCompetitions(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        competitions_file = os.path.join(base_dir, 'competitions.json')
        with open(competitions_file, 'w') as c:
            json.dump({'competitions': [comp.to_dict() for comp in self.competitions]}, c, indent=4)

    def update_competition_places(self, competition_name, places_change):
        competition = next((competition for competition in self.competitions if competition.name == competition_name), None)
        if competition is not None:
            competition.nb_of_places = places_change


app = Flask(__name__)
app.secret_key = 'something_special'

def find_club_by_name(name):
    club_manager = ClubManager()
    clubs = club_manager.loadClubs()
    return next((club for club in clubs if club.name == name), None)

def find_club_by_email(email):
    club_manager = ClubManager()
    clubs = club_manager.loadClubs()
    return next((club for club in clubs if club.email == email), None)

def find_competition_by_name(competition_name):
    competition_manager = CompetitionManager()
    competitions = competition_manager.loadCompetitions()
    return next((competition for competition in competitions if competition.name == competition_name), None)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def show_summary():
    club_manager = ClubManager()
    competition_manager = CompetitionManager()
    clubs = club_manager.loadClubs()
    competitions = competition_manager.loadCompetitions()
    club = find_club_by_email(request.form['email'])
    if not club:
        flash("Email not found")
        return redirect(url_for('index'))
    return render_template('welcome.html',club=club,competitions=competitions,clubs=clubs)


@app.route('/book/<competition_name>/<club_name>')
def book(competition_name,club_name):
    club_manager = ClubManager()
    competition_manager = CompetitionManager()
    clubs = club_manager.loadClubs()
    competitions = competition_manager.loadCompetitions()

    club = find_club_by_name(club_name)
    competition = find_competition_by_name(competition_name)

    if datetime.strptime(competition.date, "%Y-%m-%d %H:%M:%S") > datetime.now():
        return render_template('booking.html',club=club,competition=competition)
    else:
        flash("Cannot book places in past competitions")
        return render_template('welcome.html', club=club, competitions=competitions, clubs=clubs)


@app.route('/purchasePlaces',methods=['POST'])
def purchase_places():

    club_manager = ClubManager()
    competition_manager = CompetitionManager()

    clubs = club_manager.loadClubs()
    competitions = competition_manager.loadCompetitions()

    competition = find_competition_by_name(request.form['competition'])
    club = find_club_by_name(request.form['club'])

    required_places = int(request.form['places'])

    if required_places > 12:
        flash('Cannot book more than 12 places')
        return render_template('welcome.html', club=club, competitions=competitions, clubs=clubs)

    if int(club.points) < required_places:
        flash('Club does not have enough points')
        return render_template('welcome.html', club=club, competitions=competitions, clubs=clubs)

    if int(competition.nb_of_places) < required_places:
        flash("Not enough places available for this competition.")
        return render_template('welcome.html', club=club, competitions=competitions, clubs=clubs)

    competition.nb_of_places = int(competition.nb_of_places)-required_places
    club.points = str(int(club.points) - required_places)

    club_manager.update_club_points(club.name, club.points)
    competition_manager.update_competition_places(competition.name, competition.nb_of_places)

    club_manager.saveClubs()
    competition_manager.saveCompetitions()

    flash(f"{required_places} places successfully booked for {competition.name}.")
    return render_template('welcome.html', club=club, competitions=competitions, clubs=clubs)



# TODO: Add route for points display
@app.route('/clubs')
def clubs():
    club_manager = ClubManager()
    clubs = club_manager.loadClubs()
    return render_template('clubs.html', clubs=clubs)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))

