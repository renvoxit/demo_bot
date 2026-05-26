import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from data import get_films, save_films

search_films_router = Router()


def format_film(film: dict) -> str:
    return (
        f"<b>Title:</b> {film['name']}\n"
        f"<b>Description:</b> {film['description']}\n"
        f"<b>Rating:</b> {film['rating']}\n"
        f"<b>Genre:</b> {film['genre']}\n"
        f"<b>Actors:</b> {', '.join(film['actors'])}"
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
        "User %s (%s) called /search_film",
        message.from_user.username,
        message.from_user.id,
    )
    await state.set_state(SearchFilm.search_query)
    await message.answer("Enter the film title to search for:")


@search_films_router.message(SearchFilm.search_query)
async def process_search_query(message: Message, state: FSMContext) -> None:
    query = message.text.casefold().strip()
    films = get_films()
    results = [film for film in films if query in film["name"].casefold()]

    if results:
        for film in results:
            await message.answer(format_film(film))
    else:
        await message.answer("Film not found.")
    await state.clear()


class FilterFilm(StatesGroup):
    filter_criteria = State()


@search_films_router.message(Command("filter_films"))
async def filter_films(message: Message, state: FSMContext) -> None:
    logging.info(
        "User %s (%s) called /filter_films",
        message.from_user.username,
        message.from_user.id,
    )
    await state.set_state(FilterFilm.filter_criteria)
    await message.answer("Enter a genre to filter films:")


@search_films_router.message(FilterFilm.filter_criteria)
async def process_filter_criteria(message: Message, state: FSMContext) -> None:
    criteria = message.text.casefold().strip()
    films = get_films()
    filtered = [film for film in films if criteria in film["genre"].casefold()]

    if filtered:
        for film in filtered:
            await message.answer(format_film(film))
    else:
        await message.answer("No films found for this genre.")
    await state.clear()


class DeleteFilm(StatesGroup):
    delete_query = State()


@search_films_router.message(Command("delete_film"))
async def delete_film(message: Message, state: FSMContext) -> None:
    logging.info(
        "User %s (%s) called /delete_film",
        message.from_user.username,
        message.from_user.id,
    )
    await state.set_state(DeleteFilm.delete_query)
    await message.answer("Enter the title of the film you want to delete:")


@search_films_router.message(DeleteFilm.delete_query)
async def process_delete_query(message: Message, state: FSMContext) -> None:
    films = get_films()
    film_index = find_film_index(films, message.text)

    if film_index is not None:
        deleted_film = films.pop(film_index)
        save_films(films)
        await message.answer(f"Film <b>{deleted_film['name']}</b> has been deleted successfully.")
        await state.clear()
        return

    await message.answer("Film not found.")
    await state.clear()


class EditFilm(StatesGroup):
    edit_query = State()
    edit_description = State()


@search_films_router.message(Command("edit_film"))
async def edit_film(message: Message, state: FSMContext) -> None:
    logging.info(
        "User %s (%s) called /edit_film",
        message.from_user.username,
        message.from_user.id,
    )
    await state.set_state(EditFilm.edit_query)
    await message.answer("Enter the title of the film you want to edit:")


@search_films_router.message(EditFilm.edit_query)
async def process_edit_query(message: Message, state: FSMContext) -> None:
    films = get_films()
    film_index = find_film_index(films, message.text)

    if film_index is not None:
        await state.update_data(film_index=film_index)
        await message.answer("Enter the new film description:")
        await state.set_state(EditFilm.edit_description)
        return

    await message.answer("Film not found.")
    await state.clear()


@search_films_router.message(EditFilm.edit_description)
async def update_film_description(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    film_index = data["film_index"]
    films = get_films()
    films[film_index]["description"] = message.text
    save_films(films)
    await message.answer(
        f"The description for <b>{films[film_index]['name']}</b> has been updated successfully."
    )
    await state.clear()


class RateFilm(StatesGroup):
    rate_query = State()
    set_rating = State()


@search_films_router.message(Command("rate_film"))
async def rate_film(message: Message, state: FSMContext) -> None:
    logging.info(
        "User %s (%s) called /rate_film",
        message.from_user.username,
        message.from_user.id,
    )
    await state.set_state(RateFilm.rate_query)
    await message.answer("Enter the title of the film you want to rate:")


@search_films_router.message(RateFilm.rate_query)
async def process_rate_query(message: Message, state: FSMContext) -> None:
    films = get_films()
    film_index = find_film_index(films, message.text)

    if film_index is not None:
        await state.update_data(film_index=film_index)
        await message.answer("Enter the new rating (from 1 to 10):")
        await state.set_state(RateFilm.set_rating)
        return

    await message.answer("Film not found.")
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
            await message.answer(
                f"The rating for <b>{films[film_index]['name']}</b> has been updated to {rating}."
            )
            await state.clear()
        else:
            await message.answer("Invalid rating. Enter a number from 1 to 10.")
    except ValueError:
        await message.answer("Invalid input. Enter a number.")
