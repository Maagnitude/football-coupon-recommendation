from recommendationapp.validators import validate_coupon, validate_event, validate_user

class Tester():
    
    def test_user_val():
        data = {
                    "user_id": 2,
                    "birth_year": 1980,
                    "country": "FRA",
                    "currency": "EUR",
                    "gender": "Male",
                    "registration_date": "2018-04-07T12:08:54"
                }
        assert validate_user(data) == data