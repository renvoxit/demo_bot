import unittest
from pathlib import Path

from data import get_films, add_film, save_films, get_film_by_name, get_films_by_genre

TEST_FILE_PATH = Path("test_data.json")

test_data = {
    "name": "Test Film",
    "description": "Test description",
    "rating": 5.0,
    "genre": "Test Genre",
    "actors": ["Actor One", "Actor Two"],
    "poster": "http://example.com/poster.jpg",
}


class TestFilmDataFunctionsIsolated(unittest.TestCase):
    def setUp(self):
        self.data_file = TEST_FILE_PATH
        save_films([test_data], self.data_file)

    def test_get_films_all(self):
        films = get_films(self.data_file)
        self.assertEqual(len(films), 1)
        self.assertEqual(films[0]["name"], "Test Film")

    def test_get_film_by_name(self):
        film = get_film_by_name("test film", self.data_file)
        self.assertIsNotNone(film)
        self.assertEqual(film["genre"], "Test Genre")

    def test_get_films_by_genre(self):
        films = get_films_by_genre("genre", self.data_file)
        self.assertEqual(len(films), 1)
        self.assertEqual(films[0]["name"], "Test Film")

    def test_add_film(self):
        new_film = {
            "name": "Another Film",
            "description": "Another description",
            "rating": 6.7,
            "genre": "Drama",
            "actors": ["Someone", "Someone Else"],
            "poster": "http://example.com/another.jpg"
        }
        add_film(new_film, self.data_file)
        films = get_films(self.data_file)
        self.assertEqual(len(films), 2)
        self.assertEqual(films[1]["name"], "Another Film")

    def test_save_films(self):
        films = [
            {
                "name": "Saved Film",
                "description": "Saved description",
                "rating": 7.5,
                "genre": "Sci-Fi",
                "actors": ["A", "B"],
                "poster": "http://example.com/saved.jpg"
            }
        ]
        save_films(films, self.data_file)
        saved_films = get_films(self.data_file)
        self.assertEqual(len(saved_films), 1)
        self.assertEqual(saved_films[0]["genre"], "Sci-Fi")


if __name__ == "__main__":
    unittest.main()
