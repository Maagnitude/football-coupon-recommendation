import sys, os
from funcs import create_user, find_user, find_all_users
import unittest
from unittest.mock import MagicMock, call

class TestUserFunctions(unittest.TestCase):
    def test_create_user(self):
        users = [
            {
                'user_id': '1234',
                'birth_year': 1990,
                'country': 'US',
                'currency': 'USD',
                'gender': 'Male',
                'registration_date': '2022-01-01'
            },
            {
                'user_id': '5678',
                'birth_year': 1985,
                'country': 'DE',
                'currency': 'EUR',
                'gender': 'Female',
                'registration_date': '2021-12-01'
            }
        ]

        mock_db_session = MagicMock()

        # Mock the User class
        mock_user_class = MagicMock(name='User')
        mock_user_instance = mock_user_class.return_value

        # Call the function being tested
        result, status_code = create_user(users, mock_db_session)

        # Assert the calls
        expected_calls = [
            call(user_id='1234', birth_year=1990, country='US', currency='USD', gender='Male', registration_date='2022-01-01'),
            call(user_id='5678', birth_year=1985, country='DE', currency='EUR', gender='Female', registration_date='2021-12-01')
        ]
        mock_user_class.assert_has_calls(expected_calls)
        mock_db_session.add_all.assert_called_once_with([mock_user_instance, mock_user_instance])
        mock_db_session.commit.assert_called_once()

        self.assertEqual(result, ["Users created successfully"])
        self.assertEqual(status_code, 200)
        
if __name__ == '__main__':
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'recommendationapp')))
    unittest.main()