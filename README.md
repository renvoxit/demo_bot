# Telegram Movie Collection Bot

Telegram bot for managing a small personal movie collection. It can show film details, search by title, filter by genre, add new films, edit descriptions, update ratings, and delete records.

## Features

- Telegram commands built with aiogram 3
- FSM-based flow for creating, editing, rating, and deleting films
- JSON storage for a lightweight demo setup
- Inline keyboard for browsing the movie list
- Unit tests for storage helpers and FSM handlers

## Tech Stack

- Python 3.11+
- aiogram
- Pydantic
- unittest

## Setup

1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Create your local environment file:

```powershell
Copy-Item .env.example .env
```

4. Add your Telegram token to `.env`. The bot loads this file automatically on startup.

5. Run the bot:

```powershell
python bot.py
```

## Commands

- `/start` - start the bot
- `/films` - show all films
- `/search_film` - search by title
- `/filter_films` - filter by genre
- `/create_film` - add a new film
- `/edit_film` - edit a film description
- `/rate_film` - update a film rating
- `/delete_film` - delete a film
- `/cancel` - cancel the current action

## Tests

```powershell
python -m unittest discover -v
```

## Security Note

Never commit a real Telegram bot token. Store it in environment variables or a local `.env` file that is ignored by Git.

## Author

Built by Renvoxit Systems.

Portfolio: https://renvoxit.com
