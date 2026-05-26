import asyncio
import unittest
from pathlib import Path

import data
from data import get_films, save_films
from search_films import process_delete_query

TEST_FILE_PATH = Path("test_data.json")


class MockMessage:
    def __init__(self, text):
        self.text = text
        self.responses = []

    async def answer(self, text):
        self.responses.append(text)


class MockFSMContext:
    async def set_state(self, state):
        pass

    async def clear(self):
        pass


class TestDeleteFilmFSM(unittest.TestCase):
    def setUp(self):
        self.original_data_file = data.DATA_FILE
        data.DATA_FILE = TEST_FILE_PATH
        self.film = {
            "name": "Deletable Film",
            "description": "Desc",
            "rating": 4.0,
            "genre": "Genre",
            "actors": ["A", "B"],
            "poster": "http://poster.jpg",
        }
        save_films([self.film])

    def tearDown(self):
        data.DATA_FILE = self.original_data_file

    def test_delete_existing_film(self):
        msg = MockMessage("Deletable Film")
        state = MockFSMContext()
        asyncio.run(process_delete_query(msg, state))
        self.assertIn("deleted successfully", msg.responses[0])
        self.assertEqual(len(get_films()), 0)


if __name__ == "__main__":
    unittest.main()
