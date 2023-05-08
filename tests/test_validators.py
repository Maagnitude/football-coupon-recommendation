import unittest
import jsonschema
from recommendationapp.validators import validate_coupon, validate_event, validate_user

class TestValidateUser(unittest.TestCase):
    def test_valid_data(self):
        # valid input data
        data = {
            "birth_year": 1990,
            "country": "USA",
            "currency": "USD",
            "gender": "Male",
            "registration_date": "2022-01-01",
            "user_id": 123
        }

        # validate data
        result = validate_user(data)

        # assert data is unchanged
        self.assertEqual(data, result)

    def test_missing_required_field(self):
        # input data missing required field
        data = {
            "birth_year": 1990,
            "country": "USA",
            "currency": "USD",
            "gender": "Male",
            "registration_date": "2022-01-01"
        }

        # validate data
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            validate_user(data)

    def test_invalid_gender(self):
        # input data with invalid gender
        data = {
            "birth_year": 1990,
            "country": "USA",
            "currency": "USD",
            "gender": "invalid_gender",
            "registration_date": "2022-01-01",
            "user_id": 123
        }

        # validate data
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            validate_user(data)
            

class TestValidateCoupon(unittest.TestCase):
    def test_valid_coupon(self):
        coupon = {
            "coupon_id": "abc123",
            "selections": [
                {"event_id": "evt_001", "odds": 1.5},
                {"event_id": "evt_002", "odds": 2.0},
                {"event_id": "evt_003", "odds": 2.5}
            ],
            "stake": 10.0,
            "timestamp": "2021-05-08T15:30:00Z",
            "user_id": 1234
        }
        result = validate_coupon(coupon)
        self.assertEqual(result, coupon)

    def test_missing_required_field(self):
        coupon = {
            "selections": [
                {"event_id": "evt_001", "odds": 1.5},
                {"event_id": "evt_002", "odds": 2.0},
                {"event_id": "evt_003", "odds": 2.5}
            ],
            "stake": 10.0,
            "timestamp": "2021-05-08T15:30:00Z",
            "user_id": 1234
        }
        with self.assertRaises(jsonschema.ValidationError):
            validate_coupon(coupon)

    def test_invalid_field_type(self):
        coupon = {
            "coupon_id": "abc123",
            "selections": [
                {"event_id": "evt_001", "odds": 1.5},
                {"event_id": "evt_002", "odds": 2.0},
                {"event_id": "evt_003", "odds": 2.5}
            ],
            "stake": 10.0,
            "timestamp": "2021-05-08T15:30:00Z",
            "user_id": "1234"
        }
        with self.assertRaises(jsonschema.ValidationError):
            validate_coupon(coupon)
            
class TestValidateEvent(unittest.TestCase):
    def test_valid_data(self):
        data = {
            "event": [
                {
                    "begin_timestamp": "2022-01-01T12:00:00Z",
                    "country": "USA",
                    "end_timestamp": "2022-01-01T13:00:00Z",
                    "event_id": "123",
                    "league": "NBA",
                    "participants": "Team A vs Team B",
                    "sport": "Basketball"
                }
            ]
        }
        result = validate_event(data)
        self.assertEqual(result, data)

    def test_invalid_data(self):
        data = {
            "event": [
                {
                    "begin_timestamp": "2022-01-01T12:00:00Z",
                    "country": "USA",
                    "end_timestamp": "2022-01-01T13:00:00Z",
                    "event_id": "123",
                    "league": "NBA",
                    "sport": "Basketball"
                }
            ]
        }
        with self.assertRaises(jsonschema.ValidationError):
            validate_event(data)
            
if __name__ == '__main__':
    unittest.main()