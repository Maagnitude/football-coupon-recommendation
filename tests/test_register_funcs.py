# import unittest
# from recommendationapp import app, db
# from recommendationapp.funcs import create_user, create_event
# from recommendationapp.models import User
# import json

# class TestCreateUser(unittest.TestCase):
#     def setUp(self):
#         self.app = app(config_name="testing")
#         self.client = self.app.test_client()
#         self.app_context = self.app.app_context()
#         self.app_context.push()
#         db.create_all()

#     def tearDown(self):
#         db.session.remove()
#         db.drop_all()
#         self.app_context.pop()

#     def test_create_user(self):
#         user = {
#             "user_id": 1,
#             "birth_year": 1990,
#             "country": "USA",
#             "currency": "USD",
#             "gender": "Male",
#             "registration_date": "2022-05-08"
#         }
#         response = self.client.post("/users", data=json.dumps(user), content_type="application/json")
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json, {"message": "User created successfully", "user": user})
#         self.assertEqual(User.query.count(), 1)
