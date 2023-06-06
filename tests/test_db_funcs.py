import unittest
from unittest import mock
from typing import Tuple, Union, Dict
from flask import jsonify

# Import the functions you want to test
from recommendationapp.funcs import create_user, find_user, find_all_users, create_event, find_event, find_all_events

class TestFunctions(unittest.TestCase):
    def setUp(self):
        # Set up any necessary mocks or test data
        self.mock_validate_user = mock.Mock()
        self.mock_validate_event = mock.Mock()
        self.mock_db = mock.Mock()

    def tearDown(self):
        # Clean up any resources used in the tests
        pass

    def test_create_user(self):
        # Prepare test data
        user_data = {
            'user_id': 1,
            'birth_year': 1990,
            'country': 'USA',
            'currency': 'USD',
            'gender': 'Male',
            'registration_date': '2023-06-01'
        }

        # Set up the mock objects and their behaviors
        self.mock_validate_user.return_value = user_data
        self.mock_db.session.add.return_value = None
        self.mock_db.session.commit.return_value = None

        # Patch the necessary functions or objects with the mocks
        with mock.patch('recommendationapp.validators.validate_user', self.mock_validate_user):
            with mock.patch('recommendationapp.__init__.db.session', self.mock_db):
                # Call the function under test
                result = create_user(user_data)

        # Assert the expected results
        expected_result = (jsonify("User created successfully", user_data), 200)
        self.assertEqual(result, expected_result)
        self.assertTrue(self.mock_validate_user.called)
        self.mock_db.session.add.assert_called_once()
        self.mock_db.session.commit.assert_called_once()

    def test_find_user(self):
        # Prepare test data
        wanted_user = {
            'user_id': 1
        }

        # Set up the mock objects and their behaviors
        mock_user = mock.Mock()
        mock_user.user_id = wanted_user['user_id']
        mock_query = mock.Mock()
        mock_query.filter_by.return_value.first.return_value = mock_user
        self.mock_db.session.query.return_value = mock_query

        # Patch the necessary functions or objects with the mocks
        with mock.patch('recommendationapp.models.User', self.mock_db):
            # Call the function under test
            result = find_user(wanted_user)

        # Assert the expected results
        expected_user_dict = {
            "user_id": mock_user.user_id,
            "birth_year": mock_user.birth_year,
            "country": mock_user.country,
            "currency": mock_user.currency,
            "gender": mock_user.gender,
            "registration_date": mock_user.registration_date
        }
        expected_result = (jsonify("User found!", expected_user_dict), 200)
        self.assertEqual(result, expected_result)
        self.mock_db.session.query.assert_called_once_with(self.mock_db.User)
        mock_query.filter_by.assert_called_once_with(user_id=wanted_user['user_id'])
        mock_query.filter_by.return_value.first.assert_called_once()

    def test_find_all_users(self):
        # Set up the mock objects and their behaviors
        mock_users = [
            mock.Mock(user_id=1, birth_year=1990, country='USA', currency='USD', gender='Male',
                      registration_date='2023-06-01'),
            mock.Mock(user_id=2, birth_year=1985, country='Canada', currency='CAD', gender='Female',
                      registration_date='2023-06-02')
        ]
        mock_query = mock.Mock()
        mock_query.all.return_value = mock_users
        self.mock_db.session.query.return_value = mock_query

        # Patch the necessary functions or objects with the mocks
        with mock.patch('recommendationapp.models.User', self.mock_db):
            # Call the function under test
            result = find_all_users()

        # Assert the expected results
        expected_users_list = [
            {
                "User no. 1": {
                    "user_id": mock_users[0].user_id,
                    "birth_year": mock_users[0].birth_year,
                    "country": mock_users[0].country,
                    "currency": mock_users[0].currency,
                    "gender": mock_users[0].gender,
                    "registration_date": mock_users[0].registration_date
                }
            },
            {
                "User no. 2": {
                    "user_id": mock_users[1].user_id,
                    "birth_year": mock_users[1].birth_year,
                    "country": mock_users[1].country,
                    "currency": mock_users[1].currency,
                    "gender": mock_users[1].gender,
                    "registration_date": mock_users[1].registration_date
                }
            }
        ]
        expected_result = (jsonify("List of all the users: ", expected_users_list), 200)
        self.assertEqual(result, expected_result)
        self.mock_db.session.query.assert_called_once_with(self.mock_db.User)
        mock_query.all.assert_called_once()

    def test_create_event(self):
        # Prepare test data
        event_data = {
            'begin_timestamp': '2023-06-01',
            'country': 'USA',
            'end_timestamp': '2023-06-02',
            'event_id': 1,
            'league': 'NFL',
            'participants': ['TeamA', 'TeamB'],
            'sport': 'Football'
        }

        # Set up the mock objects and their behaviors
        self.mock_validate_event.return_value = event_data
        self.mock_db.session.add.return_value = None
        self.mock_db.session.commit.return_value = None

        # Patch the necessary functions or objects with the mocks
        with mock.patch('recommendationapp.validators.validate_event', self.mock_validate_event):
            with mock.patch('recommendationapp.__init__.db.session', self.mock_db):
                # Call the function under test
                result = create_event(event_data)

        # Assert the expected results
        expected_result = (jsonify("Event created successfully", event_data), 200)
        self.assertEqual(result, expected_result)
        self.assertTrue(self.mock_validate_event.called)
        self.mock_db.session.add.assert_called_once()
        self.mock_db.session.commit.assert_called_once()

    def test_find_event(self):
        # Prepare test data
        wanted_event = {
            'event_id': 1
        }

        # Set up the mock objects and their behaviors
        mock_event = mock.Mock()
        mock_event.event_id = wanted_event['event_id']
        mock_query = mock.Mock()
        mock_query.filter_by.return_value.first.return_value = mock_event
        self.mock_db.session.query.return_value = mock_query

        # Patch the necessary functions or objects with the mocks
        with mock.patch('recommendationapp.models.Event', self.mock_db):
            # Call the function under test
            result = find_event(wanted_event)

        # Assert the expected results
        expected_event_dict = {
            "begin_timestamp": mock_event.begin_timestamp,
            "country": mock_event.country,
            "end_timestamp": mock_event.end_timestamp,
            "event_id": mock_event.event_id,
            "league": mock_event.league,
            "participants": mock_event.participants,
            "sport": mock_event.sport
        }
        expected_result = (jsonify("Event found!", expected_event_dict), 200)
        self.assertEqual(result, expected_result)
        self.mock_db.session.query.assert_called_once_with(self.mock_db.Event)
        mock_query.filter_by.assert_called_once_with(event_id=wanted_event['event_id'])
        mock_query.filter_by.return_value.first.assert_called_once()

    def test_find_all_events(self):
        # Set up the mock objects and their behaviors
        mock_events = [
            mock.Mock(begin_timestamp='2023-06-01', country='USA', end_timestamp='2023-06-02', event_id=1,
                      league='NFL', participants=['TeamA', 'TeamB'], sport='Football'),
            mock.Mock(begin_timestamp='2023-06-03', country='Canada', end_timestamp='2023-06-04', event_id=2,
                      league='NHL', participants=['TeamX', 'TeamY'], sport='Hockey')
        ]
        mock_query = mock.Mock()
        mock_query.all.return_value = mock_events
        self.mock_db.session.query.return_value = mock_query

        # Patch the necessary functions or objects with the mocks
        with mock.patch('recommendationapp.models.Event', self.mock_db):
            # Call the function under test
            result = find_all_events()

        # Assert the expected results
        expected_events_list = [
            {
                "Event no. 1": {
                    "begin_timestamp": mock_events[0].begin_timestamp,
                    "country": mock_events[0].country,
                    "end_timestamp": mock_events[0].end_timestamp,
                    "event_id": mock_events[0].event_id,
                    "league": mock_events[0].league,
                    "participants": mock_events[0].participants,
                    "sport": mock_events[0].sport
                }
            },
            {
                "Event no. 2": {
                    "begin_timestamp": mock_events[1].begin_timestamp,
                    "country": mock_events[1].country,
                    "end_timestamp": mock_events[1].end_timestamp,
                    "event_id": mock_events[1].event_id,
                    "league": mock_events[1].league,
                    "participants": mock_events[1].participants,
                    "sport": mock_events[1].sport
                }
            }
        ]
        expected_result = (jsonify("List of all the events: ", expected_events_list), 200)
        self.assertEqual(result, expected_result)
        self.mock_db.session.query.assert_called_once_with(self.mock_db.Event)
        mock_query.all.assert_called_once()

if __name__ == '__main__':
    unittest.main()
