from aiogram.filters import Command
from aiogram.types.bot_command import BotCommand

FILMS_COMMAND = Command("films")
START_COMMAND = Command("start")
FILM_CREATE_COMMAND = Command("create_film")

FILMS_BOT_COMMAND = BotCommand(command="films", description="View the movie list")
START_BOT_COMMAND = BotCommand(command="start", description="Start the bot")

BOT_COMMANDS = [
    BotCommand(command="start", description="Start the bot"),
    BotCommand(command="films", description="View the movie list"),
    BotCommand(command="create_film", description="Add a film"),
    BotCommand(command="filter_films", description="Filter by genre"),
    BotCommand(command="edit_film", description="Edit a description"),
    BotCommand(command="rate_film", description="Rate a film"),
    BotCommand(command="search_film", description="Search by title"),
    BotCommand(command="delete_film", description="Delete a film"),
    BotCommand(command="cancel", description="Cancel the current action"),
]
