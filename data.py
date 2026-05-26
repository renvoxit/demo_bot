import json
from pathlib import Path

from config import DATA_FILE


def resolve_data_file(data_file: str | Path | None = None) -> Path:
    return Path(data_file or DATA_FILE)


def get_films(data_file: str | Path | None = None) -> list[dict]:
    path = resolve_data_file(data_file)
    if not path.exists():
        return []

    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("films", [])


def save_films(films: list[dict], data_file: str | Path | None = None) -> None:
    path = resolve_data_file(data_file)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump({"films": films}, f, ensure_ascii=False, indent=2)


def get_film_by_name(name: str, data_file: str | Path | None = None) -> dict | None:
    normalized_name = name.casefold().strip()
    return next(
        (film for film in get_films(data_file) if film["name"].casefold() == normalized_name),
        None,
    )


def get_films_by_genre(genre: str, data_file: str | Path | None = None) -> list[dict]:
    normalized_genre = genre.casefold().strip()
    return [
        film
        for film in get_films(data_file)
        if normalized_genre in film["genre"].casefold()
    ]


def add_film(film: dict, data_file: str | Path | None = None) -> None:
    films = get_films(data_file)
    films.append(film)
    save_films(films, data_file)
