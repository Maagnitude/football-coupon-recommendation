import sys, os
from funcs import create_user, create_event
from unittest import mock
import unittest

class TestCreateUser(unittest.TestCase):

    def setUp(self):
        self.db_session = mock.MagicMock(spec=['add_all', 'commit'])

    def test_create_user_successfully(self):
        users = [
            {
                "user_id": "1",
                "birth_year": 1990,
                "country": "IT",
                "currency": "EUR",
                "gender": "Male",
                "registration_date": "2018-04-07T12:08:54"
            },
            {
                "user_id": "2",
                "birth_year": 1985,
                "country": "USA",
                "currency": "USD",
                "gender": "Female",
                "registration_date": "2018-04-07T12:08:54"
            }
        ]
        response = create_user(users, self.db_session)

        self.assertEqual(response[-1], 200)
        self.assertTrue(self.db_session.add_all.called)
        self.assertTrue(self.db_session.commit.called)

    def test_create_user_duplicate_id(self):
        users = [
            {
                "user_id": "1",
                "birth_year": 1990,
                "country": "IT",
                "currency": "EUR",
                "gender": "Male",
                "registration_date": "2018-04-07T12:08:54"
            }
        ]
        self.db_session.commit.side_effect = Exception("UNIQUE constraint failed")


        response = create_user(users, self.db_session)

        expected_error = "User creation failed! There is a user with the same ID! (user_id=1)"
        self.assertEqual(response, (expected_error, 400))
        self.assertTrue(self.db_session.add_all.called)
        self.assertTrue(self.db_session.commit.called)


class TestCreateEvent(unittest.TestCase):

    def setUp(self):
        self.db_session = mock.MagicMock(spec=['add_all', 'commit'])

    def test_create_event_successfully(self):
        events = [
            {
                    "home": "Liverpool",
                    "away": "Arsenal",
                    "begin_timestamp": "2020-02-09 18:00:00+00",
                    "country": "England",
                    "end_timestamp": "2021-01-01 00:00:00+00",
                    "event_id": "1",
                    "league": "Premier League",
                    "sport": "football"
                },
                {
                    "home": "Liverpool",
                    "away": "Arsenal",
                    "begin_timestamp": "2020-02-09 18:00:00+00",
                    "country": "England",
                    "end_timestamp": "2021-01-01 00:00:00+00",
                    "event_id": "2",
                    "league": "Premier League",
                    "sport": "football"
            }
        ]
        response = create_event(events, self.db_session)

        self.assertEqual(response[-1], 200)
        self.assertTrue(self.db_session.add_all.called)
        self.assertTrue(self.db_session.commit.called)

    def test_create_event_duplicate_id(self):
        events = [
            {
                    "home": "Liverpool",
                    "away": "Arsenal",
                    "begin_timestamp": "2020-02-09 18:00:00+00",
                    "country": "England",
                    "end_timestamp": "2021-01-01 00:00:00+00",
                    "event_id": "1",
                    "league": "Premier League",
                    "sport": "football"
            }
        ]
        self.db_session.commit.side_effect = Exception("UNIQUE constraint failed")

        response = create_event(events, self.db_session)

        expected_error = "Event creation failed! There is an event with the same ID! (event_id=1)"
        self.assertEqual(response, (expected_error, 400))
        self.assertTrue(self.db_session.add_all.called)
        self.assertTrue(self.db_session.commit.called)
        
if __name__ == '__main__':
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'recommendationapp')))
    unittest.main()