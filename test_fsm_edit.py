import unittest
import asyncio
from pathlib import Path

from search_films import process_edit_query, update_film_description
from search_films import EditFilm

import data
from data import save_films

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


class TestEditFilmFSM(unittest.TestCase):
    def setUp(self):
        self.data_file = TEST_FILE_PATH
        self.original_data_file = data.DATA_FILE
        data.DATA_FILE = self.data_file
        self.initial_film = {
            "name": "Editable Film",
            "description": "Old description",
            "rating": 5.0,
            "genre": "Drama",
            "actors": ["X", "Y"],
            "poster": "http://poster.jpg"
        }
        save_films([self.initial_film])

    def tearDown(self):
        data.DATA_FILE = self.original_data_file

    def test_edit_query_found(self):
        msg = MockMessage("Editable Film")
        state = MockFSMContext()
        asyncio.run(process_edit_query(msg, state))
        self.assertEqual(state.data["film_index"], 0)
        self.assertEqual(state.state, EditFilm.edit_description)

    def test_edit_description_update(self):
        msg = MockMessage("New edited description")
        state = MockFSMContext()
        state.data["film_index"] = 0
        asyncio.run(update_film_description(msg, state))
        self.assertIn("успішно оновлено", msg.responses[0])


if __name__ == "__main__":
    unittest.main()
