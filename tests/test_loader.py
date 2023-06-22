import sys, os
from unittest import TestCase, mock
from teams.loader import load_leagues, export_teams, generate_events, \
    create_events, add_odds, load_countries, create_users
import unittest
import uuid

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'recommendationapp')))

# 1. load_leagues(league_json_files) test
class TestLoadLeagues(TestCase):
    def test_load_leagues(self):
        with mock.patch('builtins.open', mock.mock_open(read_data='{"name": "Bundesliga", "matches": []}')):
            leagues = load_leagues(['league1.json', 'league2.json'])
        
        self.assertEqual(len(leagues), 2)
        self.assertEqual(leagues[0]['name'], 'Bundesliga')
        self.assertEqual(leagues[1]['name'], 'Bundesliga')
        
# 2. export_teams(leagues) test
class TestExportTeams(TestCase):
    def test_export_teams(self):
        leagues = [
            {'name': 'Bundesliga 2020/21', 'matches': [{'team1': 'Bayern', 'team2': 'Dortmund'}]},
            {'name': 'Premier League 2020/21', 'matches': [{'team1': 'Chelsea', 'team2': 'Man Utd'}]}
        ] 
        teams_data = export_teams(leagues)
        
        self.assertEqual(len(teams_data), 2)
        self.assertEqual(teams_data[0]['league'], 'Bundesliga')
        self.assertEqual(teams_data[0]['country'], 'Germany')
        self.assertEqual(teams_data[0]['teams'], ['Bayern', 'Dortmund'])
        self.assertEqual(teams_data[1]['league'], 'Premier League')
        self.assertEqual(teams_data[1]['country'], 'England')
        self.assertEqual(teams_data[1]['teams'], ['Chelsea', 'Man Utd'])
        
# 3. generate_events(league) test
class TestGenerateEvents(TestCase):
    def test_generate_events(self):
        league = {
            'league': 'Bundesliga',
            'country': 'Germany',
            'teams': ['Bayern', 'Dortmund']
        }
        with mock.patch('uuid.uuid4', side_effect=[uuid.UUID('00000000-0000-0000-0000-000000000001')]):
            events = generate_events(league)

        self.assertEqual(len(events), 1)
        self.assertIn(events[0]['home'], ['Bayern', 'Dortmund'])
        self.assertIn(events[0]['away'], ['Bayern', 'Dortmund'])
        self.assertNotEqual(events[0]['home'], events[0]['away'])
        self.assertEqual(events[0]['league'], 'Bundesliga')
        self.assertEqual(events[0]['country'], 'Germany')
        self.assertEqual(events[0]['sport'], 'football')
        self.assertEqual(str(events[0]['event_id']), '00000000-0000-0000-0000-000000000001')
        
# 4. create_events(leagues) test
class TestCreateEvents(TestCase):
    def test_create_events(self):
        leagues = [
            {'teams': ['Bayern', 'Dortmund']},
            {'teams': ['Chelsea', 'Man Utd']}
        ] 
        with mock.patch('teams.loader.generate_events', side_effect=[[{'home': 'Bayern', 'away': 'Dortmund'}], [{'home': 'Chelsea', 'away': 'Man Utd'}]]):
            events = create_events(leagues)
        
        self.assertEqual(len(events), 2)
        self.assertEqual(events[0]['home'], 'Bayern')
        self.assertEqual(events[0]['away'], 'Dortmund')
        self.assertEqual(events[1]['home'], 'Chelsea')
        self.assertEqual(events[1]['away'], 'Man Utd')
        
# 5. add_odds(events) test
class TestAddOdds(TestCase):
    def test_add_odds(self):
        events = [
            {'event_id': 'event1'},
            {'event_id': 'event2'}
        ]    
        with mock.patch('random.uniform', return_value=2.5):
            odds = add_odds(events)
        
        self.assertEqual(len(odds), 2)
        self.assertIsInstance(odds[0]['odd_id'], str)
        self.assertEqual(odds[0]['event_id'], 'event1')
        self.assertEqual(odds[0]['odds'], 2.5)
        self.assertIsInstance(odds[1]['odd_id'], str)
        self.assertEqual(odds[1]['event_id'], 'event2')
        self.assertEqual(odds[1]['odds'], 2.5)
        
# 6. load_countries(countries_json) test
class TestLoadCountries(TestCase):
    def test_load_countries(self):
        countries_json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'recommendationapp', 'teams', 'countries.json'))
        with mock.patch('json.load', return_value={'countries': {'country': [{'countryCode': 'DE', 'currencyCode': 'EUR'}]}}):
            country_list = load_countries([countries_json_path])
            
        self.assertEqual(len(country_list), 1)
        self.assertEqual(country_list[0]['code'], 'DE')
        self.assertEqual(country_list[0]['currency'], 'EUR')
        
# 7. create_users(country_list) test
class TestCreateUsers(unittest.TestCase):
    def test_create_users(self):
        country_list = [
            {'code': 'DE', 'currency': 'EUR'},
            {'code': 'US', 'currency': 'USD'}
        ]
        users = create_users(country_list)
            
        self.assertEqual(len(users), 100)
        self.assertIsInstance(users[0]['user_id'], str)
        self.assertIsInstance(users[0]['birth_year'], int)
        self.assertIsInstance(users[0]['country'], str)
        self.assertIsInstance(users[0]['currency'], str)
        self.assertIn(users[0]['gender'], ['Male', 'Female'])
        self.assertIsInstance(users[0]['registration_date'], str)
        
if __name__ == '__main__':
    unittest.main()