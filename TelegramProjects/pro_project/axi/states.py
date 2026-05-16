from aiogram.fsm.state import State, StatesGroup

class Register(StatesGroup):
    fullname = State()
    phone = State()

class DriverRegister(StatesGroup):
    fullname = State()
    phone = State()
    lat = State()
    lon = State()
    car_name = State()
    plate_number = State()
    car_color = State()

class OrderTaxi(StatesGroup):
    from_loc = State()
    to_loc = State()
    user_id = State()
    price = State()
    distance = State()
    confirm = State()
    tariff = State()

class DriverTracking(StatesGroup):
    active = State()

class Tariffs(StatesGroup):
    name = State()
    base_price = State()
    km_price = State()