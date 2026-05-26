import unittest
import asyncio
from types import SimpleNamespace

from create_films import film_rating
from fsm import CreateFilm


class MockMessage:
    def __init__(self, text):
        self.text = text
        self.responses = []

    async def answer(self, text, reply_markup=None):
        self.responses.append(text)


class MockFSMContext:
    def __init__(self):
        self.data = {}
        self.state = None

    async def update_data(self, **kwargs):
        self.data.update(kwargs)

    async def get_data(self):
        return self.data

    async def set_state(self, state):
        self.state = state

    async def clear(self):
        self.data = {}
        self.state = None


class TestCreateFilmFSM(unittest.TestCase):
    def test_invalid_rating_non_numeric(self):
        msg = MockMessage("не число")
        state = MockFSMContext()
        asyncio.run(film_rating(msg, state))
        self.assertTrue(any("Некоректний" in r for r in msg.responses))

    def test_invalid_rating_out_of_range(self):
        msg = MockMessage("15")
        state = MockFSMContext()
        asyncio.run(film_rating(msg, state))
        self.assertTrue(any("Некоректний" in r for r in msg.responses))

    def test_valid_rating(self):
        msg = MockMessage("8.5")
        state = MockFSMContext()
        asyncio.run(film_rating(msg, state))
        self.assertEqual(state.data["rating"], 8.5)
        self.assertEqual(state.state, CreateFilm.genre)


if __name__ == "__main__":
    unittest.main()
