from aiogram.fsm.state import State, StatesGroup


class AdminAddProject(StatesGroup):
    waiting_title = State()
    waiting_city = State()
    waiting_size = State()
    waiting_type = State()
    waiting_description = State()
    waiting_photos = State()
    waiting_confirmation = State()


class AdminEditProject(StatesGroup):
    choosing_field = State()
    waiting_title = State()
    waiting_city = State()
    waiting_size = State()
    waiting_type = State()
    waiting_description = State()
    waiting_photo_action = State()
    waiting_photos = State()
