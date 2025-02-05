import unittest

from src.user_state import UserState


class TestUserState(unittest.TestCase):
    def setUp(self):
        self.state = UserState()

    def test_initial_state(self):
        self.assertIsNone(self.state.discipline)
        self.assertIsNone(self.state.practice_number)
        self.assertIsNone(self.state.variant)

    def test_is_complete(self):
        self.assertFalse(self.state.is_complete())
        self.state.discipline = "Math"
        self.state.practice_number = "1"
        self.state.variant = "A"
        self.assertTrue(self.state.is_complete())

    def test_reset(self):
        self.state.discipline = "Math"
        self.state.reset()
        self.assertIsNone(self.state.discipline)


if __name__ == '__main__':
    unittest.main()
