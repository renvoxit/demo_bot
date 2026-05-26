import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery, Message, URLInputFile

from commands import BOT_COMMANDS, FILMS_COMMAND, START_COMMAND
from config import BOT_TOKEN
from create_films import film_create_router
from data import get_films
from external import async_log_function_call
from keyboard import FilmCallback, films_keyboard_markup
from models import Film
from search_films import search_films_router

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
        "Hi! I can help you manage a personal movie collection: browse films, "
        "search by title, filter by genre, and add new records."
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
        await message.answer("Your movie collection is empty. Add the first film with /create_film.")
        return

    markup = films_keyboard_markup(films_list=films)
    await message.answer(
        "Here is your movie list. Select a title to view details.",
        reply_markup=markup,
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
        await callback.answer("Film not found.", show_alert=True)
        return

    film = Film(**films[film_id])
    text = (
        f"Film: {film.name}\n"
        f"Description: {film.description}\n"
        f"Rating: {film.rating}\n"
        f"Genre: {film.genre}\n"
        f"Actors: {', '.join(film.actors)}\n"
    )

    await callback.message.answer_photo(
        caption=text,
        photo=URLInputFile(
            film.poster,
            filename=f"{film.name}_poster.{film.poster.split('.')[-1]}",
        ),
    )
    await callback.answer()


async def main() -> None:
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
