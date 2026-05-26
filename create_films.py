from data import add_film
from models import Film
from aiogram import Router, html
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from fsm import CreateFilm
import logging
from aiogram.filters import StateFilter

film_create_router = Router()


@film_create_router.message(Command("cancel"), StateFilter("*"))
async def cancel_any_state(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Дію скасовано.", reply_markup=ReplyKeyboardRemove())


@film_create_router.message(Command("create_film"))
async def film_create(message: Message, state: FSMContext) -> None:
    logging.info(
        "User %s (%s) called /create_film",
        message.from_user.username,
        message.from_user.id,
    )
    await state.set_state(CreateFilm.name)
    await message.answer(
        "Введіть назву фільму.",
        reply_markup=ReplyKeyboardRemove(),
    )


@film_create_router.message(CreateFilm.name)
async def film_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.set_state(CreateFilm.description)
    await message.answer(
        "Введіть опис фільму.",
        reply_markup=ReplyKeyboardRemove(),
    )


@film_create_router.message(CreateFilm.description)
async def film_description(message: Message, state: FSMContext) -> None:
    await state.update_data(description=message.text)
    await state.set_state(CreateFilm.rating)
    await message.answer(
        "Вкажіть рейтинг фільму від 0 до 10.",
        reply_markup=ReplyKeyboardRemove(),
    )


@film_create_router.message(CreateFilm.rating)
async def film_rating(message: Message, state: FSMContext) -> None:
    try:
        rating = float(message.text.replace(",", "."))
        if not (0 <= rating <= 10):
            raise ValueError()
    except ValueError:
        await message.answer("Некоректний рейтинг. Введіть число від 0 до 10.")
        return

    await state.update_data(rating=rating)
    await state.set_state(CreateFilm.genre)
    await message.answer(
        "Введіть жанр фільму.",
        reply_markup=ReplyKeyboardRemove(),
    )


@film_create_router.message(CreateFilm.genre)
async def film_genre(message: Message, state: FSMContext) -> None:
    await state.update_data(genre=message.text)
    await state.set_state(CreateFilm.actors)
    await message.answer(
        text="Введіть акторів фільму через кому.\n"
             + html.bold("Наприклад: Emma Stone, Ryan Gosling"),
        reply_markup=ReplyKeyboardRemove(),
    )


@film_create_router.message(CreateFilm.actors)
async def film_actors(message: Message, state: FSMContext) -> None:
    actors = [actor.strip() for actor in message.text.split(",") if actor.strip()]
    if not actors:
        await message.answer("Додайте хоча б одного актора.")
        return

    await state.update_data(actors=actors)
    await state.set_state(CreateFilm.poster)
    await message.answer(
        "Введіть посилання на постер фільму.",
        reply_markup=ReplyKeyboardRemove(),
    )


@film_create_router.message(CreateFilm.poster)
async def film_poster(message: Message, state: FSMContext) -> None:
    await state.update_data(poster=message.text)
    data = await state.get_data()
    await state.clear()

    film = Film(**data)
    add_film(film.model_dump())

    await message.answer(
        f"Фільм <b>{html.quote(film.name)}</b> успішно додано!",
        reply_markup=ReplyKeyboardRemove(),
    )
