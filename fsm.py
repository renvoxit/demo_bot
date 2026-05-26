from aiogram.fsm.state import State, StatesGroup


class CreateFilm(StatesGroup):
    name = State()
    description = State()
    rating = State()
    genre = State()
    actors = State()
    poster = State()
