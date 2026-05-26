
from aiogram.filters import Command
from aiogram.types.bot_command import BotCommand

FILMS_COMMAND = Command("films")
START_COMMAND = Command("start")

FILMS_BOT_COMMAND = BotCommand(
    command="films", description="Переглянути список фільмів")
START_BOT_COMMAND = BotCommand(command="start", description="Почати роботу")

FILM_CREATE_COMMAND = Command("create_film")
BOT_COMMANDS = [
    BotCommand(command="start", description="Почати роботу"),
    BotCommand(command="films", description="Переглянути список фільмів"),
    BotCommand(command="create_film", description="Додати фільм"),
    BotCommand(command="filter_films",
               description="Фільтрувати за жанром"),
    BotCommand(command="edit_film", description="Редагувати опис"),
    BotCommand(command="rate_film", description="Оцінити фільм"),
    BotCommand(command="search_film", description="Знайти фільм за назвою"),
    BotCommand(command="delete_film", description="Видалити фільм"),
    BotCommand(command="cancel", description="Скасувати дію"),
]
