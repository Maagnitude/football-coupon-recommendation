from glob import glob
import os
import json
import random
import datetime
import uuid
import requests

# TESTS FOR load_leagues, export_teams, generate_events, create_events, add_odds, load_countries, create_users OK

# LEAGUES FOR EVENTS
def load_leagues(league_json_files):
    leagues = []
    for league_json_file in league_json_files:
        with open(league_json_file) as json_file:
            league = json.load(json_file)
            leagues.append(league)
    return leagues

# TEAMS FOR EVENTS
def export_teams(leagues):
    data = []
    country_data = {'Bundesliga': 'Germany', 'Premier League': 'England', 'Primera Division': 'Spain', 'Serie A': 'Italy', 'Ligue 1': 'France',
                    'Super League': 'Greece', 'Eredivisie': 'Netherlands', 'First League': 'Hungary', 'Primeira Liga': 'Portugal', 'Premiership': 'Scotland'}
    for league in leagues:
        cur_league = league['name'].replace('2020/21', '').strip()
        teams = []
        for match in league['matches']:
            if match['team1'] not in teams:
                teams.append(match['team1'])
            if match['team2'] not in teams:
                teams.append(match['team2'])

        for i, team in enumerate(teams):
            teams[i] = team.replace(' 04', '').replace('1.', '').replace(' 05', '').strip()
        data.append({'league': cur_league, 'country': country_data[cur_league],'teams': teams})
    return data

# EVENTS
def generate_events(league):
    events = []
    allteams = league['teams']
    while (len(allteams) > 0):
        delta_minutes = (random.choice([0, 15, 30, 45])//15)*15 # So the minutes will be 0, 15, 30 or 45
        # Matchdate will always be 10 to 20 days from now, random hour and 15 minute interval, always 90 minutes long
        matchdate = datetime.datetime.now().replace(minute=delta_minutes) + datetime.timedelta(days=random.randint(10, 20), hours=random.randint(0,23))
        team1 = random.choice(allteams)
        allteams.pop(allteams.index(team1))
        team2 = random.choice(allteams)
        allteams.pop(allteams.index(team2))
        if team1 != team2:
            events.append({'home': team1, 
                           'away': team2, 
                           'league': league['league'],
                           'country': league['country'], 
                           'begin_timestamp': str(matchdate)[:-7], 
                           'end_timestamp': str(matchdate+datetime.timedelta(minutes=90))[:-7],
                           'sport': 'football',
                           'event_id': str(uuid.uuid4())})
    return events

def create_events(leagues):
    events = []
    for league in leagues:
        events += generate_events(league)
    return events

def import_events(events):
    requests.post('http://127.0.0.1:5000/register_event', json=events)

# ODDS       
def add_odds(events):
    odds = []
    for event in events:
        odds.append({'odd_id': str(uuid.uuid4()),
                     'event_id': event['event_id'],
                     'odds': int(random.uniform(1, 5) * 100) / 100})
    return odds

def import_odds(odds):
    requests.post('http://127.0.0.1:5000/register_odds', json=odds)
    
# USERS   
def load_countries(countries_json):
    countries = []
    country_list = []
    for country_json in countries_json:
        with open(country_json) as json_file:
            country = json.load(json_file)
            countries.append(country)
    for country in countries[0]["countries"]["country"]:
        country_list.append({"code": country["countryCode"], "currency": country["currencyCode"]})
    return country_list

def create_users(country_list):
    users = []
   
    for _ in range(100):
        users.append({"user_id": str(uuid.uuid4()),
                      "birth_year": random.randint(1950, 2004),
                      "country": random.choice(country_list)["code"],
                      "currency": random.choice(country_list)["currency"],
                      "gender": random.choice(["Male", "Female"]),
                      "registration_date": str(datetime.datetime.now() - datetime.timedelta(days=random.randint(10, 365*2)))[:-7]
                      })
    return users

def import_users(users):
    requests.post('http://127.0.0.1:5000/register_user', json=users)

if __name__ == '__main__':
    working_directory = os.getcwd()
    leagues_json_files = glob(os.path.join(working_directory, 'recommendationapp/teams/data/*.json'))
    countries_json = glob(os.path.join(working_directory, 'recommendationapp/teams/countries.json'))
    leagues = load_leagues(leagues_json_files)
    data = export_teams(leagues)
    all_events = create_events(data)
    import_events(all_events)
    odds = add_odds(all_events)
    import_odds(odds)
    country_list = load_countries(countries_json)
    users = create_users(country_list)
    import_users(users)