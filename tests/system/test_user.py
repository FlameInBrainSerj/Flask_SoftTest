import json

from models.user import UserModel
from tests.base_test import BaseTest


class UserTest(BaseTest):
    def test_register_user(self):
        with self.app() as client:
            with self.app_context():
                response = client.post("/register", data={"username": "Test User", "password": "1234"})

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_username("Test User"))
                self.assertDictEqual({"msg": "User created successfully!"},
                                     json.loads(response.data))

    def test_register_and_login(self):
        with self.app() as client:
            with self.app_context():
                client.post("/register", data={"username": "Test User", "password": "1234"})
                auth_request = client.post("/auth",
                                           data=json.dumps({"username": "Test User", "password": "1234"}),
                                           headers={"Content-Type": "application/json"})

                self.assertIn("access_token", json.loads(auth_request.data).keys())

    def test_register_duplicate_user(self):
        with self.app() as client:
            with self.app_context():
                client.post("/register", data={"username": "Test User", "password": "1234"})
                response = client.post("/register", data={"username": "Test User", "password": "1234"})

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({"msg": "A user with this username already exists"},
                                     json.loads(response.data))
