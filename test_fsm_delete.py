import unittest
import asyncio
from pathlib import Path

from search_films import process_delete_query
import data
from data import save_films, get_films

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
        self.data_file = TEST_FILE_PATH
        self.original_data_file = data.DATA_FILE
        data.DATA_FILE = self.data_file
        self.film = {
            "name": "Deletable Film",
            "description": "Desc",
            "rating": 4.0,
            "genre": "Genre",
            "actors": ["A", "B"],
            "poster": "http://poster.jpg"
        }
        save_films([self.film])

    def tearDown(self):
        data.DATA_FILE = self.original_data_file

    def test_delete_existing_film(self):
        msg = MockMessage("Deletable Film")
        state = MockFSMContext()
        asyncio.run(process_delete_query(msg, state))
        self.assertIn("успішно видалено", msg.responses[0])
        films = get_films()
        self.assertEqual(len(films), 0)


if __name__ == "__main__":
    unittest.main()
