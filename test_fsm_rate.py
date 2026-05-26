import asyncio
import unittest
from pathlib import Path

import data
from data import save_films
from search_films import RateFilm, process_rate_query, set_film_rating

TEST_FILE_PATH = Path("test_data.json")


class MockMessage:
    def __init__(self, text):
        self.text = text
        self.responses = []

    async def answer(self, text):
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


class TestRateFilmFSM(unittest.TestCase):
    def setUp(self):
        self.original_data_file = data.DATA_FILE
        data.DATA_FILE = TEST_FILE_PATH
        self.film = {
            "name": "Rateable Film",
            "description": "Desc",
            "rating": 4.0,
            "genre": "Genre",
            "actors": ["A", "B"],
            "poster": "http://poster.jpg",
        }
        save_films([self.film])

    def tearDown(self):
        data.DATA_FILE = self.original_data_file

    def test_rate_query_found(self):
        msg = MockMessage("Rateable Film")
        state = MockFSMContext()
        asyncio.run(process_rate_query(msg, state))
        self.assertEqual(state.data["film_index"], 0)
        self.assertEqual(state.state, RateFilm.set_rating)

    def test_set_rating_success(self):
        msg = MockMessage("9")
        state = MockFSMContext()
        state.data["film_index"] = 0
        asyncio.run(set_film_rating(msg, state))
        self.assertIn("updated to 9.0", msg.responses[0])


if __name__ == "__main__":
    unittest.main()
