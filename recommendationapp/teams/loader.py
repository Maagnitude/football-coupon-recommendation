from glob import glob
import os
import json
import random
import datetime
import uuid
import requests

def load_leagues(league_json_files):
    leagues = []
    
    for league_json_file in league_json_files:
        with open(league_json_file) as json_file:
            league = json.load(json_file)
            leagues.append(league)
    return leagues

def export_teams(leagues):
    data = []
    country_data = {'Bundesliga': 'Germany', 'Premier League': 'England'}
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

def generate_events(league):
    events = []
    matchdate = datetime.datetime.now() + datetime.timedelta(days=60)
    allteams = league['teams']
    while (len(allteams) > 0):
        team1 = random.choice(allteams)
        allteams.pop(allteams.index(team1))
        team2 = random.choice(allteams)
        allteams.pop(allteams.index(team2))
        if team1 != team2:
            events.append({'home': team1, 
                           'away': team2, 
                           'league': league['league'],
                           'country': league['country'], 
                           'begin_timestamp': str(matchdate), 
                           'end_timestamp': str(matchdate+datetime.timedelta(minutes=90)),
                           'sport': 'football',
                           'event_id': str(uuid.uuid4())})
    return events

def create_events(leagues):
    events = []
    for league in leagues:
        events += generate_events(league)
    return events

# def create_coupons(events):
#     coupons = []
#     for i in range(10):
#         coupon = []
#         for j in range(5):
#             coupon.append(random.choice(events))
#         coupons.append(coupon)
#     return coupons

# endpoint POST, θα δεχετε χρηστη και stake, θα επιστρεφει το coupon με τα αντιστοιχα odds
# INPUT: mode- high, low, random | stake | user | number of matches
#              high: θα επιλεγει τα ακριβοτερα odds
# 

def import_events(events):
    events = {'events': events}
    requests.post('http://127.0.0.1:5000/register_event', json=json.dumps(events))
        
def create_odds(events):
    odds = []
    for event in events:
        odds.append({'event_id': event['event_id'],
                     'odds': random.uniform(1, 4)})
    return odds

def import_odds(odds):
    odds = {'odds': odds}
    requests.post('http://127.0.0.1:5000/register_odds', json=json.dumps(odds))

if __name__ == '__main__':
    working_directory = os.getcwd()
    leagues_json_files = glob(os.path.join(working_directory, 'recommendationapp/teams/data/*.json'))
    leagues = load_leagues(leagues_json_files)
    data = export_teams(leagues)
    all_events = create_events(data)
    import_events(all_events)
    odds = create_odds(all_events)
    print(odds)
    #import_odds(odds) TODO: endpoint for odds
    # TODO: GENERATE COUPONS