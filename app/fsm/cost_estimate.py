from aiogram.fsm.state import State, StatesGroup


class CostEstimateFSM(StatesGroup):
    dimensions = State()
    private_or_public = State()
    project_need = State()
    indoor_outdoor = State()
    equipment_location = State()
    pool_type = State()
    embedded_type = State()
    embedded_material = State()
    water_type = State()
    purpose = State()
    finish = State()
    heating = State()
    disinfection = State()
    extra_disinfection = State()
    lighting = State()
    music = State()
    attractions = State()
    cover = State()
    phone = State()
    email = State()
