from aiogram.fsm.state import State, StatesGroup


class ProjectCreation(StatesGroup):
    start = State()
    general_full_name = State()
    general_phone = State()
    general_email = State()
    general_address = State()
    geometry_length = State()
    geometry_width = State()
    geometry_depth = State()
    review = State()
