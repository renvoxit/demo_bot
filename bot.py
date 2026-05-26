from external import async_log_function_call
from config import BOT_TOKEN
from search_films import search_films_router
import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery, URLInputFile


from commands import (
    FILMS_COMMAND,
    START_COMMAND,
    BOT_COMMANDS,
)
from data import get_films
from models import Film
from keyboard import films_keyboard_markup, FilmCallback
from create_films import film_create_router

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)

dp = Dispatcher()

dp.include_router(film_create_router)
dp.include_router(search_films_router)


@dp.message(START_COMMAND)
@async_log_function_call
async def command_start_handler(message: Message) -> None:
    logging.info(
        "User %s (%s) called /start",
        message.from_user.username,
        message.from_user.id,
    )
    await message.answer(
        "Привіт! Я бот для персональної колекції фільмів: можу показати список, "
        "знайти фільм, відфільтрувати за жанром і додати новий запис."
    )


@dp.message(FILMS_COMMAND)
@async_log_function_call
async def command_films_handler(message: Message) -> None:
    logging.info(
        "User %s (%s) called /films",
        message.from_user.username,
        message.from_user.id,
    )
    films = get_films()
    if not films:
        await message.answer("У колекції поки немає фільмів. Додайте перший через /create_film.")
        return

    markup = films_keyboard_markup(films_list=films)
    await message.answer(
        "Перелік фільмів. Натисніть на назву для перегляду деталей.",
        reply_markup=markup
    )


@dp.callback_query(FilmCallback.filter())
@async_log_function_call
async def callback_film(callback: CallbackQuery, callback_data: FilmCallback) -> None:
    logging.info(
        "User %s (%s) selected film ID %s",
        callback.from_user.username,
        callback.from_user.id,
        callback_data.id,
    )
    film_id = callback_data.id
    films = get_films()
    if film_id >= len(films):
        await callback.answer("Фільм не знайдено.", show_alert=True)
        return

    film_data = films[film_id]
    film = Film(**film_data)

    text = (
        f"Фільм: {film.name}\n"
        f"Опис: {film.description}\n"
        f"Рейтинг: {film.rating}\n"
        f"Жанр: {film.genre}\n"
        f"Актори: {', '.join(film.actors)}\n"
    )

    await callback.message.answer_photo(
        caption=text,
        photo=URLInputFile(
            film.poster,
            filename=f"{film.name}_poster.{film.poster.split('.')[-1]}"
        )
    )
    await callback.answer()


async def main():
    if not BOT_TOKEN:
        raise RuntimeError(
            "BOT_TOKEN is not set. Add it to your environment before starting the bot."
        )

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(BOT_COMMANDS)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
