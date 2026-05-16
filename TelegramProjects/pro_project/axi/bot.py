import asyncio
from datetime import datetime
from geopy.geocoders import Nominatim
from aiogram.fsm.context import FSMContext

import db
from db import create_table
from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
from aiogram.types import (Message, ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, CallbackQuery, InlineKeyboardButton)
from config import BOT_TOKEN, ADMIN_ID
from states import Register, DriverRegister, OrderTaxi, DriverTracking, Tariffs
from utils import calculate_distance, find_driver

TOKEN = BOT_TOKEN

bot = Bot(
    TOKEN,
    default=DefaultBotProperties(parse_mode='HTML')
)

dp = Dispatcher()

@dp.message(Command("start"))
async def start_command(message: Message, state: FSMContext):
    name = message.from_user.full_name
    user = db.get_user(message.from_user.id)
    if user in ADMIN_ID:
        await admin_panel()

    if user:
        await main_menu(message, state)
    else:
        keyboard = [
            [KeyboardButton(text="Yo'lovchi")],
            [KeyboardButton(text="Haydovchi")]
        ]
        await message.answer(f"👋🏻  Salom {name}! \n\n🚕  Axi ga xush kelibsiz \n👇  O'zingizga keraklisini tanlang", reply_markup=ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True))


@dp.message(lambda message: message.text in ["Yo'lovchi", "Haydovchi"])
async def message_handler(message: Message, state: FSMContext):
    if message.text == "Yo'lovchi":
        await user_register(message, state)
    if message.text == "Haydovchi":
        await driver_register(message, state)

async def user_register(message: Message, state: FSMContext):
    await message.answer("✏️  To'liq ismingizni kiriting: ")
    await state.set_state(Register.fullname)
    # await get_fullname(message, state)

@dp.message(Register.fullname)
async def get_fullname(message: Message, state: FSMContext):
    keyboard = [
        [KeyboardButton(text="📞 Raqamimni yuborish", request_contact=True)]
    ]

    await state.update_data(fullname=message.text)
    await message.answer("Telefon raqamingizni yuboring: ", reply_markup=ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True))
    await state.set_state(Register.phone)
    # await get_phone(message, state)

@dp.message(Register.phone)
async def get_phone(message: Message, state: FSMContext):
    data = await state.get_data()
    if not message.contact:
        await message.answer("❌ Iltimos, tugma orqali raqam yuboring")
        return

    phone = message.contact.phone_number
    phone = phone.replace("+998", "")
    telegram_id = message.from_user.id
    full_name = data["fullname"]

    db.add_user(telegram_id=telegram_id, full_name=full_name, phone=phone)

    await message.answer(f"✅ Ro'yxatdan o'tdingiz!\n{full_name} | {phone}")
    await state.clear()
    await main_menu(message, state)

async def driver_register(message: Message, state: FSMContext):
    await message.answer("✏️ To'liq Ism-Familyangizni kiriting: ")
    await state.set_state(DriverRegister.fullname)

@dp.message(DriverRegister.fullname)
async def get_driver_fullname(message: Message, state: FSMContext):
    keyboard = [
        [KeyboardButton(text="📞 Raqamimni yuborish", request_contact=True)]
    ]

    await state.update_data(fullname=message.text)
    await message.answer("Telefon raqamingizni yuboring: ", reply_markup=ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True))
    await state.set_state(DriverRegister.phone)

@dp.message(DriverRegister.phone)
async def get_driver_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.contact.phone_number)
    keyboard = [[KeyboardButton(text="locatsiyani yuborish", request_location=True)]]
    await message.answer("Locatsiyangizni yuboring", reply_markup=ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True))
    await state.set_state(DriverRegister.lat)

@dp.message(DriverRegister.lat)
async def get_driver_location(message: Message, state: FSMContext):
    await state.update_data(lat=message.location.latitude, lon=message.location.longitude)
    await message.answer("Mashinangizni nomi va modelini yozing.\nMasalan: Nexia 3")
    await state.set_state(DriverRegister.car_name)

@dp.message(DriverRegister.car_name)
async def get_car_name(message: Message, state:FSMContext):
    await state.update_data(car_name=message.text)
    await message.answer("Mashinangiz raqamini to'liq yozing\nMasalan: 01|X000XX")
    await state.set_state(DriverRegister.plate_number)

@dp.message(DriverRegister.plate_number)
async def get_plate_number(message: Message, state: FSMContext):
    await state.update_data(plate_number=message.text)
    await message.answer("Mashinangiz rangi?")
    await state.set_state(DriverRegister.car_color)

@dp.message(DriverRegister.car_color)
async def get_car_color(message: Message, state: FSMContext):
    data = await state.get_data()
    telegram_id = message.from_user.id
    full_name = data["fullname"]
    phone = data["phone"]
    lat = data["lat"]
    lon = data["lon"]
    car_name = data["car_name"]
    plate_number = data["plate_number"]
    car_color = message.text
    is_active = True

    db.add_driver(telegram_id=telegram_id, full_name=full_name,  phone=phone, lat=lat, lon=lon, car_name=car_name, car_plate_number=plate_number, car_color=car_color, is_active=is_active)
    await message.answer(f"✅ Ro'yxatdan o'tdingiz!\n{full_name} | {phone}\nMashina nomi: {car_name}\nMashina raqami: {plate_number}\nMashina rangi: {car_color}")
    await state.clear()

    await message.answer_photo(photo='location.jpg' ,text="📍 Iltimos, jonli joylashuvingizni yuboring \n(Rasmda belgilangan funksiya tanlansin!)")

async def update_driver_location(message: Message):
    user_id = message.from_user.id

    driver = db.get_driver(user_id)

    if driver:
        if not message.location.live_period:
            return message.answer("Iltimos, 'Jonli joylashuv' ni yuboring")
    else:
        return

    lat = message.location.latitude
    lon = message.location.longitude

    db.update_driver_location(user_id, lat, lon)


async def main_menu(message: Message, state: FSMContext):
    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="🚕 Buyurtma qilish"), KeyboardButton(text="📦 Buyurtmalar tarixi")],
        [KeyboardButton(text="⚙ Sozlamalar")]
    ], resize_keyboard=True)
    await message.answer("👇 Kerakli bo‘limni tanlang:", reply_markup=keyboard)


@dp.message(lambda message: message.text == "🚕 Buyurtma qilish")
async def start_ordering(message: Message, state: FSMContext):
    user_id = message.from_user.id
    await state.set_state(OrderTaxi.user_id)
    keyboard = [
        [KeyboardButton(text="Manzilni yuborish", request_location=True)]
    ]
    await message.answer("Hozir turgan manzilingizni yuboring: ", reply_markup=ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True))
    await state.set_state(OrderTaxi.from_loc)

@dp.message(OrderTaxi.from_loc)
async def get_to_loc(message: Message, state: FSMContext):
    from_loc = f"{message.location.latitude},{message.location.longitude}"
    await state.update_data(from_loc=from_loc)
    keyboard = [
        [KeyboardButton(text="Manzilni yuborish", request_location=True)]
    ]
    await message.answer("Borayotgan manzilingizni kiriting: ", reply_markup=ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True))
    await state.set_state(OrderTaxi.to_loc)

@dp.message(OrderTaxi.to_loc)
async def choose_tariffs(message: Message, state: FSMContext):
    to_loc = f"{message.location.latitude},{message.location.longitude}"
    await state.update_data(to_loc=to_loc)
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="econom")],
            [KeyboardButton(text="comfort")]
        ],
        resize_keyboard=True
    )
    await message.answer("Tarifni tanlang: ", reply_markup=keyboard)
    await state.set_state(OrderTaxi.tariff)

@dp.message(OrderTaxi.tariff)
async def confirm(message: Message, state: FSMContext):
    data = await state.get_data()
    tariff = db.get_tariff(name=message.text)
    if not tariff:
        await message.answer("Tarif noto'g'ri")
        await state.clear()
        return

    await state.update_data(tariff=tariff[1])
    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="✅ Ha")],
        [KeyboardButton(text="❌ Yo‘q")]
    ], resize_keyboard=True)

    from_lat, from_lon = map(float, data["from_loc"].split(","))
    to_lat, to_lon = map(float, data["to_loc"].split(","))

    distance = calculate_distance(from_lat, from_lon, to_lat, to_lon)

    geolocator = Nominatim(user_agent="taxi_bot")

    from_location = geolocator.reverse((from_lat, from_lon))
    to_location = geolocator.reverse((to_lat, to_lon))

    price = int(tariff[2] + (distance * tariff[3]))

    await state.update_data(price=price, distance=distance)
    await message.answer(f"📍 <b>Qayerdan:</b> {from_location.address}\n\n"
                         f"🏁 <b>Qayerga:</b> {to_location.address}\n\n"
                         f"🛣 <b>Masofa:</b> {distance:.2f} km\n\n"
                         f"💰 <b>Narx:</b> {price} so'm | <b>Tariff:</b> {tariff[1]}\n\n"
                         f"Buyurtmani tasdiqlaysizmi?",
                         reply_markup=keyboard
                         )
    await state.set_state(OrderTaxi.confirm)


@dp.message(OrderTaxi.confirm)
async def confirm_order(message: Message, state: FSMContext):
    await state.update_data(confirm=message.text)
    data = await state.get_data()
    user_id = message.from_user.id
    from_loc = data['from_loc']
    to_loc = data['to_loc']
    distance = data['distance']
    price = data['price']
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if message.text == "✅ Ha":
        await message.answer("Buyurtma tasdiqlandi")
        print("Order saved!")

        from_lat, from_lon = map(float, data["from_loc"].split(","))
        to_lat, to_lon = map(float, data["to_loc"].split(","))

        geolocator = Nominatim(user_agent="taxi_bot")

        from_location = geolocator.reverse((from_lat, from_lon))
        to_location = geolocator.reverse((to_lat, to_lon))

        drivers = db.get_active_drivers()

        driver_id, _ = find_driver(from_lat, from_lon, drivers)
        order_id = db.create_order(user_id=user_id, from_loc=from_location.address, to_loc=to_location.address, price=price, distance=distance, created_at=created_at)

        if driver_id:
            db.assign_driver(order_id, driver_id)
            keyboard = ReplyKeyboardMarkup(keyboard=[
                [KeyboardButton(text="✅ Qabul qilish")],
                [KeyboardButton(text="❌ Rad etish")]
            ], resize_keyboard=True)
            await bot.send_message(driver_id,
                                    f"🚕 Yangi buyurtma!\n\n"
                                    f"📍 Qayerdan: {from_loc}\n\n"
                                    f"🏁 Qayerga: {to_loc}\n\n"
                                    f"💰 Narx: {price} so'm\n\n",
                                    reply_markup=keyboard
                                   )
            await message.answer("🚗 Haydovchi topildi, javob kuting...")
        else:
            await message.answer("Haydovchi topilmadi")
            await main_menu(message, state)

        await state.clear()

    if message.text == "❌ Yo‘q":
        await message.answer("Buyurtma bekor qilindi")
        await state.clear()
        await main_menu(message, state)

@dp.message(lambda m: m.text == "❌ Rad etish")
async def reject_order(message: Message):
    driver_id = message.from_user.id
    order = db.get_last_order_by_driver(driver_id)
    if not order:
        return await message.answer("❌ Buyurtma topilmadi")

    order_id = order["id"]
    db.add_rejected_driver(order_id, driver_id)
    await message.answer("❌ Buyurtma rad etildi")

    rejected_raw = db.get_rejected_drivers(order_id)
    rejected_ids = [int(x) for x in rejected_raw.split(",") if x]

    from_lat, from_lon = map(float, order["from_loc"].split(","))
    to_lat, to_lon = map(float, data["to_loc"].split(","))

    geolocator = Nominatim(user_agent="taxi_bot")

    from_location = geolocator.reverse((from_lat, from_lon))
    to_location = geolocator.reverse((to_lat, to_lon))

    drivers = db.get_available_drivers_excluding(rejected_ids)
    new_driver_id, _ = find_driver(from_lat, from_lon, drivers)
    if not new_driver_id:
        await bot.send_message(order["user_id"], "❌ Afsuski, haydovchi topilmadi")
        return

    db.assign_driver(order_id, new_driver_id)

    await bot.send_message(
        new_driver_id,
        f"🚕 Yangi buyurtma!\n\n"
        f"📍 {from_location.address}\n"
        f"🏁 {to_location.address}",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="✅ Qabul qilish")],
                [KeyboardButton(text="❌ Rad etish")]
            ],
            resize_keyboard=True
        )
    )

@dp.message(lambda m: m.text == "✅ Qabul qilish")
async def accept_order(message: Message):
    driver_id = message.from_user.id

    order = db.get_last_order_by_driver(driver_id)

    if not order:
        return await message.answer("❌ Buyurtma yo‘q")

    db.update_order_status(order["id"], "qabul_qilindi")

    await message.answer("✅ Qabul qilindi")

    # Notify user
    await bot.send_message(
        order["user_id"],
        "🚗 Haydovchi buyurtmani qabul qildi!"
    )

    # Driver button
    await message.answer(
        "Yo‘lga tushasizmi?",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="🚗 Yo'lga tushdim")]],
            resize_keyboard=True
        )
    )

@dp.message(lambda m: m.text == "🚗 Yo'lga tushdim")
async def driver_started(message: Message, state: FSMContext):
    await state.set_state(DriverTracking.active)

    driver_id = message.from_user.id

    order = db.get_last_order_by_driver(driver_id)

    if not order:
        return await message.answer("❌ Buyurtma topilmadi")

    await bot.send_message(
        order["user_id"],
        "🚗 Haydovchi yo‘lga chiqdi"
    )

@dp.message(DriverTracking.active, lambda m: m.location is not None)
async def track_driver(message: Message):
    driver_id = message.from_user.id

    order = db.get_last_order_by_driver(driver_id)
    if not order:
        return

    driver_lat = message.location.latitude
    driver_lon = message.location.longitude

    user_lat, user_lon = map(float, order["from_loc"].split(","))

    distance = calculate_distance(driver_lat, driver_lon, user_lat, user_lon)

    await bot.send_location(order["user_id"], driver_lat, driver_lon)

    if distance < 1:
        await bot.send_message(order["user_id"], "🚗 Haydovchi yaqin!")
    if distance < 0.1:
        await bot.send_message(driver_id, "Yetib keldingizmi?",
                               reply_markup=ReplyKeyboardMarkup(
                                   keyboard=[KeyboardButton(text="Yetib keldim")],
                                   resize_keyboard=True)
                               )

@dp.message(lambda m: m.text == "Yetib keldim")
async def driver_arrived(message: Message):
    driver_id = message.from_user.id

    order = db.get_last_order_by_driver(driver_id)

    db.update_order_status(order["id"], "yetib_keldi")

    await bot.send_message(order["user_id"], "🚗 Haydovchi yetib keldi!")

    await message.answer("Yo'lovchini oldingizmi?", reply_markup=ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🧍 Yo'lovchini oldim")]
        ],resize_keyboard=True))

@dp.message(lambda m: m.text == "🧍 Yo'lovchini oldim")
async def get_passenger(message: Message):
    driver_id = message.from_user.id
    order = db.get_last_order_by_driver(driver_id)

    db.update_order_status(order["id"], "jarayonda")
    await bot.send_message(order["user_id"], "🚕 Safar boshlandi")

    keyboard = [[KeyboardButton(text="🏁 Yetkazdim")]]

    await message.answer("Manzilga yetgach, tugmani bosing", reply_markup=ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True))

@dp.message(lambda m: m.text == "🏁 Yetkazdim")
async def complete_ride(message: Message, state: FSMContext):
    driver_id = message.from_user.id

    order = db.get_last_order_by_driver(driver_id)
    db.update_order_status(order["id"], "yakunlandi")

    await bot.send_message(order["user_id"], "🏁 Siz manzilga yetib keldingiz!\nRahmat 😊")
    await state.clear()
    await message.answer("✅ Safar yakunlandi")

@dp.message(lambda message: message.text == "📦 Buyurtmalar tarixi")
async def order_history(message: Message, state: FSMContext):
    user_id = message.from_user.id
    orders = db.get_order(user_id)
    if not orders:
        await message.answer("Buyurtmalar yo'q")
        await main_menu(message, state)

    text = ""

    for order in orders:
        order_id = order[0]
        from_loc = order[1]
        to_loc = order[2]
        driver_id = order[3]
        distance = round(order[4], 2)
        price = order[5]
        created_at = order[6]

        text += (f"🆔  <b>Buyurtma</b>: {order_id}\n\n"
                 f"📍 <b>Yo'nalish:</b> {from_loc}------>{to_loc}\n"
                 f"🛣 <b>Masofa:</b>{distance}\n\n"
                 f"🚗 <b>Haydovchi:</b> {driver_id}\n"
                 f"💰 <b>Narx:</b> {price} so'm.\n"
                 f"🕒 <b>Vaqti:</b> {created_at}\n___________________\n\n")

    await message.answer(text)
    await main_menu(message, state)

@dp.message(lambda message: message.text == "⚙ Sozlamalar")
async def settings(message: Message, state: FSMContext):
    user_id = message.from_user.id

    user = db.get_user(user_id)
    text = ""
    if user:
        full_name = user[1]
        phone = user[2]

        text += (f"Ismingiz: {full_name}\n"
                 f"Telefon raqamingiz: {phone}")
    else:
        await message.answer("Siz ro'yxatdan o'tmagansiz")

    await message.answer(text)
    await main_menu(message, state)

@dp.message(Command("admin"))
async def admin_panel(message: Message):
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="📊 Statistika")],
                [KeyboardButton(text="📋 Tariflar")]
            ],
            resize_keyboard=True
        )
        await message.answer("Salom, admin! \n\n🛠 Sizning panel:", reply_markup=keyboard)

@dp.message(lambda message: message.text == "📊 Statistika")
async def statistics(message: Message):
    x = db.count_driver()
    y = db.count_user()

    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="📦 Oxirgi 10 ta buyurtma", callback_data="last_orders")]])

    await message.answer(f"👤 Foydalanuvchilar soni:  <b>{y}</b>\n\n"
                         f"🚗 Haydovchilar soni:  <b>{x}</b>", reply_markup=keyboard)

@dp.callback_query(lambda c: c.data == "last_orders")
async def show_last_orders(callback: CallbackQuery):
    orders = db.get_last_10_orders()
    text = ""
    for order in orders:
        id = order[0]
        from_loc = order[1]
        to_loc = order[2]
        driver_id = order[3]
        distance = round(order[4], 2)
        price = order[5]
        created_at = order[6]
        text += (f"\n<b>📦 Buyurtma</b> №:{id}  | 💰 <b>Narx:</b> {price}\n\n"
                 f"📍 <b>Yo'nalish:</b> {from_loc}-->{to_loc}\n\n"
                 f"🛣 <b>Distance:</b> {distance}\n-----------------\n")

    await callback.message.answer(text)
    await callback.answer()
    await admin_panel(callback.message)

@dp.message(lambda message: message.text == "📋 Tariflar")
async def tariffs(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ Tarif qo'shish")],
            [KeyboardButton(text="📋 Tariflar ro'yxati")]
        ],
        resize_keyboard=True
    )
    await message.answer("Tariflarni boshqarish uchun quyidagilardan birini tanlang: ", reply_markup=keyboard)

@dp.message(lambda mes: mes.text == "➕ Tarif qo'shish")
async def tariff_name(message: Message, state: FSMContext):
    await message.answer("Tarif nomini kiriting: \n\n(Eslatib o'tamiz, tariflar soni 2 tadan: \n    econom va comfortdan oshmasligi kerak!)")
    await state.set_state(Tariffs.name)

@dp.message(Tariffs.name)
async def tariff_price(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Boshlang'ich narxini kiriting\nMasalan: 5000")
    await state.set_state(Tariffs.base_price)

@dp.message(Tariffs.base_price)
async def tariff_per_km(message: Message, state: FSMContext):
    await state.update_data(base_price=message.text)
    await message.answer("Km uchun narxni kiriting.\n\n<b>Yuqoridagidek!</b>")
    await state.set_state(Tariffs.km_price)

@dp.message(Tariffs.km_price)
async def add_tariff(message: Message, state: FSMContext):
    await state.update_data(km_price=message.text)
    data = await state.get_data()
    name = data["name"]
    base_price = data["base_price"]
    km_price = data["km_price"]

    db.add_tariff(name=name, base_price=base_price, km_price=km_price)
    await message.answer("Tarif muvafaqqiyatli saqlandi!")
    await state.clear()
    await admin_panel(message)

@dp.message(lambda mes: mes.text == "📋 Tariflar ro'yxati")
async def get_tariffs(message: Message):
    tariffs = db.get_tariffs()

    text = ""

    for tarif in tariffs:
        tarif_id = tarif[0]
        name = tarif[1]
        base_price = tarif[2]
        km_price = tarif[3]

        text += (f"\nTarif №: {tarif_id}\n"
                 f"Turi: {name}\n"
                 f"Boshlang'ich narxi: {base_price}\n"
                 f"Per_km: {km_price}\n_________________\n")

    await message.answer(text)
    await admin_panel(message)

async def main():
    create_table()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())