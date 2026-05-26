from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import logging
from data import get_films, save_films

search_films_router = Router()


def format_film(film: dict) -> str:
    return (
        f"<b>Назва:</b> {film['name']}\n"
        f"<b>Опис:</b> {film['description']}\n"
        f"<b>Рейтинг:</b> {film['rating']}\n"
        f"<b>Жанр:</b> {film['genre']}\n"
        f"<b>Актори:</b> {', '.join(film['actors'])}"
    )


def find_film_index(films: list[dict], name: str) -> int | None:
    normalized_name = name.casefold().strip()
    for index, film in enumerate(films):
        if film["name"].casefold() == normalized_name:
            return index
    return None


class SearchFilm(StatesGroup):
    search_query = State()


@search_films_router.message(Command("search_film"))
async def search_film(message: Message, state: FSMContext) -> None:
    logging.info(
        f"User {message.from_user.username} ({message.from_user.id}) вызвал команду /search_film")
    await state.set_state(SearchFilm.search_query)
    await message.answer("Введіть назву фільму для пошуку:")


@search_films_router.message(SearchFilm.search_query)
async def process_search_query(message: Message, state: FSMContext) -> None:
    query = message.text.casefold().strip()
    films = get_films()

    results = [film for film in films if query in film["name"].casefold()]

    if results:
        for film in results:
            await message.answer(format_film(film))
    else:
        await message.answer("Фільм не знайдено.")
    await state.clear()


class FilterFilm(StatesGroup):
    filter_criteria = State()


@search_films_router.message(Command("filter_films"))
async def filter_films(message: Message, state: FSMContext) -> None:
    logging.info(
        f"User {message.from_user.username} ({message.from_user.id}) вызвал команду /filter_films")
    await state.set_state(FilterFilm.filter_criteria)
    await message.answer("Введіть жанр для фільтрації фільмів:")


@search_films_router.message(FilterFilm.filter_criteria)
async def process_filter_criteria(message: Message, state: FSMContext) -> None:
    criteria = message.text.casefold().strip()
    films = get_films()
    filtered = [film for film in films if criteria in film["genre"].casefold()]

    if filtered:
        for film in filtered:
            await message.answer(format_film(film))
    else:
        await message.answer("Фільм за таким жанром не знайдено.")
    await state.clear()


class DeleteFilm(StatesGroup):
    delete_query = State()


@search_films_router.message(Command("delete_film"))
async def delete_film(message: Message, state: FSMContext) -> None:
    logging.info(
        f"User {message.from_user.username} ({message.from_user.id}) вызвал команду /delete_film")
    await state.set_state(DeleteFilm.delete_query)
    await message.answer("Введіть назву фільму, який бажаєте видалити:")


@search_films_router.message(DeleteFilm.delete_query)
async def process_delete_query(message: Message, state: FSMContext) -> None:
    films = get_films()
    film_index = find_film_index(films, message.text)

    if film_index is not None:
        deleted_film = films.pop(film_index)
        save_films(films)
        await message.answer(f"Фільм <b>{deleted_film['name']}</b> успішно видалено.")
        await state.clear()
        return

    await message.answer("Фільм не знайдено.")
    await state.clear()


class EditFilm(StatesGroup):
    edit_query = State()
    edit_description = State()


@search_films_router.message(Command("edit_film"))
async def edit_film(message: Message, state: FSMContext) -> None:
    logging.info(
        f"User {message.from_user.username} ({message.from_user.id}) вызвал команду /edit_film")
    await state.set_state(EditFilm.edit_query)
    await message.answer("Введіть назву фільму, який бажаєте редагувати:")


@search_films_router.message(EditFilm.edit_query)
async def process_edit_query(message: Message, state: FSMContext) -> None:
    films = get_films()
    film_index = find_film_index(films, message.text)

    if film_index is not None:
        await state.update_data(film_index=film_index)
        await message.answer("Введіть новий опис фільму:")
        await state.set_state(EditFilm.edit_description)
        return

    await message.answer("Фільм не знайдено.")
    await state.clear()


@search_films_router.message(EditFilm.edit_description)
async def update_film_description(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    film_index = data["film_index"]
    films = get_films()
    films[film_index]["description"] = message.text
    save_films(films)
    await message.answer(f"Опис фільму <b>{films[film_index]['name']}</b> успішно оновлено.")
    await state.clear()


class RateFilm(StatesGroup):
    rate_query = State()
    set_rating = State()


@search_films_router.message(Command("rate_film"))
async def rate_film(message: Message, state: FSMContext) -> None:
    logging.info(
        f"User {message.from_user.username} ({message.from_user.id}) вызвал команду /rate_film")
    await state.set_state(RateFilm.rate_query)
    await message.answer("Введіть назву фільму, який бажаєте оцінити:")


@search_films_router.message(RateFilm.rate_query)
async def process_rate_query(message: Message, state: FSMContext) -> None:
    films = get_films()
    film_index = find_film_index(films, message.text)

    if film_index is not None:
        await state.update_data(film_index=film_index)
        await message.answer("Введіть новий рейтинг (від 1 до 10):")
        await state.set_state(RateFilm.set_rating)
        return

    await message.answer("Фільм не знайдено.")
    await state.clear()


@search_films_router.message(RateFilm.set_rating)
async def set_film_rating(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    film_index = data["film_index"]
    films = get_films()

    try:
        rating = float(message.text.replace(",", "."))
        if 1 <= rating <= 10:
            films[film_index]["rating"] = rating
            save_films(films)
            await message.answer(f"Рейтинг фільму <b>{films[film_index]['name']}</b> оновлено на {rating}.")
            await state.clear()
        else:
            await message.answer("Некоректний рейтинг. Введіть число від 1 до 10.")
    except ValueError:
        await message.answer("Некоректний ввід. Введіть число.")
