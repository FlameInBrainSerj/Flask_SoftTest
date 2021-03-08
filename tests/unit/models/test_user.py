from models.user import UserModel
from tests.unit.unit_base_test import UnitBaseTest


class UserTest(UnitBaseTest):
    def test_crate_user(self):
        user = UserModel("Test User", "abcd")

        self.assertEqual(user.username, "Test User")
        self.assertEqual(user.password, "abcd")