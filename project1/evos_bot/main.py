from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

TOKEN = '8536341146:AAE7HFq6gEBhO-OvOzWpz3bybE_ZElCLHzA'

user_cart = {}
user_address = {}
waiting_for_address = {}
waiting_for_feedback_contact = {}
user_language = {}

TEXT = {
    "start": {
        "uz": "Quyidagilardan birini tanlang:",
        "ru": "Выберите одно из следующего:",
        "en": "Please select one of the following:"
    },
    "settings_language": {
        "uz": "Tilni tanlang:",
        "ru": "Выберите язык:",
        "en": "Choose a language:"
    },
    "order_empty": {
        "uz": "Siz hech narsa buyurtma bermagansiz 🤷‍♂️",
        "ru": "Вы ещё ничего не заказали 🤷‍♂️",
        "en": "You haven't ordered anything 🤷‍♂️"
    },
    "address_saved": {
        "uz": "✅ Manzilingiz saqlandi: {}",
        "ru": "✅ Ваш адрес сохранен: {}",
        "en": "✅ Your address has been saved: {}"
    },
    "feedback_received": {
        "uz": "✅ Qabul qilindi, rahmat! 😊",
        "ru": "✅ Получено, спасибо! 😊",
        "en": "✅ Received, thank you! 😊"
    },
    "address_change":{
        "uz": "✏️ O‘zgartirish",
        "ru": "✏️ Изменения",
        "en": "✏️ Change"
    },
    "adress_ask":{
        "uz": "📍 Iltimos, manzilingizni matn ko‘rinishida kiriting (masalan: Chilonzor-17).",
        "ru": "📍 Пожалуйста, введите свой адрес в текстовом формате (например: Chilanzor-17).",
        "en": "📍 Please enter your address in text format (for example: Chilanzor-17)."
    },
    "choose_from_menu":{
        "uz": "Menyudan bo‘lim tanlang:",
        "ru": "Выберите раздел из меню:",
        "en": "Select a section from the menu:"
    },
    "your_cart":{
        "uz": "🛍 Sizning savatingiz:\n\n",
        "ru": "🛍 Ваша корзина:\n\n",
        "en": "🛍 Your cart:\n\n"
    },
    "empty_cart":{
        "uz": "🛍 Savatingiz bo‘sh 🤷‍♂️",
        "ru": "🛍 Ваша корзина пуста 🤷‍♂️",
        "en": "🛍 Your cart is empty 🤷‍♂️"
    },
    "send_address":{
        "uz": "📍 Yangi manzil yuborish",
        "ru": "📍 Отправить новый адрес",
        "en": "📍 Send new address"
    },
    "no_address":{
        "uz": "Manzil hali kiritilmagan",
        "ru": "Адрес еще не введен",
        "en": "Address not yet entered"
    },
    "send_number":{
        "uz": "📱 Telefon raqamni yuborish",
        "ru": "📱 Отправьте номер телефона",
        "en": "📱 Send phone number"
    },
    "ask_feedback":{
        "uz": "🧑‍🍳 Sizning har bir fikringiz biz uchun muhim!\n"
                "📞 Bog‘lanishimiz uchun iltimos, telefon raqamingizni yuboring:",
        "ru": "🧑‍🍳 Ваше мнение важно для нас!\n"
                "📞 Пожалуйста, пришлите нам свой номер телефона, чтобы мы могли с вами связаться.",
        "en": "🧑‍🍳 Your every opinion is important to us!\n"
                "📞 Please send us your phone number so we can contact you:"
    },
    "product_not_found":{
        "uz": "❌ Mahsulot topilmadi",
        "ru": "❌ Товар не найден",
        "en": "❌ Product not found"
    }
}

MENU_BUTTON = {
    "uz": ['🍴Menyu', '🛍Mening buyurtmalarim', '📍Manzilni sozlash', '✍️Izoh qoldirish', '⚙️Sozlamalar'],
    "ru": ['🍴Меню', '🛍Мои заказы', '📍Настройки адреса', '✍️Оставить комментарий', '⚙️Настройки'],
    "eng": ['🍴Menu', '🛍My Orders', '📍Address Settings', '✍️Leave a Comment', '⚙️Settings'],
}

LANGUAGE_BUTTON = {
    "uz": [("🇺🇿 O'zbekcha",'lang_uz'), ("🇷🇺 Ruscha",'lang_ru'), ("🇺🇸 Inglizcha",'lang_eng')],
    "ru": [("🇺🇿 узбекский",'lang_uz'), ("🇷🇺 Русский",'lang_ru'), ("🇺🇸 Английский",'lang_eng')],
    "eng": [("🇺🇿 Uzbek",'lang_uz'), ("🇷🇺 Russian",'lang_ru'), ("🇺🇸 English",'lang_eng')],
}

def get_text(chat_id, key):
    lang = user_language.get(chat_id, "uz")
    return TEXT[key][lang]

def start(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    lang = user_language.get(chat_id, "uz")
    buttons = MENU_BUTTON[lang]
    keyboard = [
        [KeyboardButton(buttons[0])],
        [KeyboardButton(buttons[1])], [KeyboardButton(buttons[2])],
        [KeyboardButton(buttons[3])], [KeyboardButton(buttons[4])]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text(get_text(chat_id, "start"), reply_markup=reply_markup)

def show_language_keyboard(chat_id):
    buttons = LANGUAGE_BUTTON.get(user_language.get(chat_id, "uz"))
    keyboard = [[InlineKeyboardButton(text, callback_data=data)] for text, data in buttons]
    return InlineKeyboardMarkup(keyboard)

def handle_message(update: Update, context: CallbackContext):
    text = update.message.text
    chat_id = update.message.chat.id

    if waiting_for_address.get(chat_id):
        user_address[chat_id] = text
        waiting_for_address[chat_id] = False
        update.message.reply_text(get_text(chat_id, "address_saved").format(text))
        start(update, context)
        return

    lang = user_language.get(chat_id, "uz")
    buttons = MENU_BUTTON[lang]

    if text == buttons[0]:
        keyboard = [
            [KeyboardButton("🍔 Burgerlar"), KeyboardButton("🌯 Lavashlar")],
            [KeyboardButton("🥙 Shaurma"), KeyboardButton("🌭 XotDog")],
            [KeyboardButton("⬅️ Ortga")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        update.message.reply_text(get_text(chat_id, "choose_from_menu"), reply_markup=reply_markup)

    elif text == "⬅️ Ortga":
        start(update, context)

    elif text == buttons[1]:
        cart = user_cart.get(chat_id, [])
        if not cart:
            update.message.reply_text(get_text(chat_id, "order_empty"))
        else:
            msg = get_text(chat_id, "your_cart")
            total = 0
            for item in cart:
                total += item['price'] * item['qyt']
                msg += f"{item['name']} x{item['qyt']} = {item['price'] * item['qyt']} so'm\n"
            msg += f"\n💰 Jami: {total} so'm"
            update.message.reply_text(msg)

    elif text == buttons[2]:
        old_address = user_address.get(chat_id, get_text(chat_id, "no_address"))
        keyboard = [
            [InlineKeyboardButton(get_text(chat_id, "address_change"), callback_data="change_address")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            f"📍 Sizning manzilingiz: {old_address}",
            reply_markup=reply_markup
        )

    elif text == buttons[3]:
        keyboard = [[KeyboardButton(get_text(chat_id, "send_number"), request_contact=True)]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        waiting_for_feedback_contact[chat_id] = True
        update.message.reply_text(
            get_text(chat_id, "ask_feedback"),
            reply_markup=reply_markup
        )
        return

    elif text == buttons[4]:
        reply_markup = show_language_keyboard(chat_id)
        update.message.reply_text(get_text(chat_id, "settings_language"), reply_markup=reply_markup)

    elif text == "🍔 Burgerlar":
        show_burgers(update, context)

    elif text == "🌯 Lavashlar":
        show_lavash(update, context)

    elif text == "🥙 Shaurma":
        show_shaurma(update, context)

    elif text == "🌭 XotDog":
        show_xotdog(update, context)

def show_burgers(update: Update, context: CallbackContext):
    keyboard = [
        [
            InlineKeyboardButton("1", callback_data="qyt_1"),
            InlineKeyboardButton("2", callback_data="qyt_2"),
            InlineKeyboardButton("3", callback_data="qyt_3"),
            InlineKeyboardButton("4", callback_data="qyt_4"),
            InlineKeyboardButton("5", callback_data="qyt_5"),
        ],
        [InlineKeyboardButton("🛒 Savatga qo‘shish", callback_data="add_SirliBurger")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    with open("burger.png", "rb") as burger:
        update.message.reply_photo(
            photo=burger,
            caption="<b>🍔 Chizburger</b>\n\n"
                    "Yumshoq bulochkada grill sous ostida shirali kotlet, "
                    "Chedder pishlog‘i, pomidor, bodring, piyoz va aysberg salati.\n\n"
                    "<b>💰 Narxi: 38 000 so'm</b>",
            reply_markup=reply_markup,
            parse_mode="HTML"
        )

def show_lavash(update: Update, context: CallbackContext):
    keyboard = [
        [
            InlineKeyboardButton("1", callback_data="qyt_1"),
            InlineKeyboardButton("2", callback_data="qyt_2"),
            InlineKeyboardButton("3", callback_data="qyt_3"),
            InlineKeyboardButton("4", callback_data="qyt_4"),
            InlineKeyboardButton("5", callback_data="qyt_5"),
        ],
        [InlineKeyboardButton("🛒 Savatga qo‘shish", callback_data="add_lavash")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    with open("lavash.png", "rb") as lavash:
        update.message.reply_photo(
            photo=lavash,
            caption="<b>🌯 Lavashello</b>\n\n"
                    "Mayin tovuq bo‘laklari, yangi pomidorlar, "
                    "qarsildoq karam va xushbo‘y sarimsoqli sous bilan uyg‘unlashib, "
                    "har qanday tushlik uchun eng maqbul tanlov hisoblanadi."
                    "<b> Narxi: 37000 so'm </b>",
            reply_markup=reply_markup,
            parse_mode="HTML"
        )

def show_shaurma(update: Update, context: CallbackContext):
    keyboard = [
        [
            InlineKeyboardButton("1", callback_data="qyt_1"),
            InlineKeyboardButton("2", callback_data="qyt_2"),
            InlineKeyboardButton("3", callback_data="qyt_3"),
            InlineKeyboardButton("4", callback_data="qyt_4"),
            InlineKeyboardButton("5", callback_data="qyt_5"),
        ],
        [InlineKeyboardButton("🛒 Savatga qo‘shish", callback_data="add_shaurma")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    with open("shaurma.jpg", "rb") as shaurma:
        update.message.reply_photo(
            photo=shaurma,
            caption="<b>🥙 Shaurmito</b>\n\n"
                    "Qizarib pishgan tovuq go'shti-grill, "
                    "yangi bodring va shirali pomidor bo'laklari, "
                    "kunjut urug'lari sepilgan, yarim doira shaklli, "
                    "shirin iforga ega bulochkada yangi piyoz va ko'katlar bilan sharqona sarimsoq sousi"
                    "<b> Narxi: 34000 so'm </b>",
            reply_markup=reply_markup,
            parse_mode="HTML"
        )

def show_xotdog(update: Update, context: CallbackContext):
    keyboard = [
        [
            InlineKeyboardButton("1", callback_data="qyt_1"),
            InlineKeyboardButton("2", callback_data="qyt_2"),
            InlineKeyboardButton("3", callback_data="qyt_3"),
            InlineKeyboardButton("4", callback_data="qyt_4"),
            InlineKeyboardButton("5", callback_data="qyt_5"),
        ],
        [InlineKeyboardButton("🛒 Savatga qo‘shish", callback_data="add_xotdog")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    with open("xotdog.jpg", "rb") as xotdog:
        update.message.reply_photo(
            photo=xotdog,
            caption="<b>🌭 Hot-Dog</b>\n\n"
                    "Ishtahaochar sosiska, yangi pomidor va marinadlangan karsildoq "
                    "bodring bo'lakchalari, mayin kunjutli bagetdagi maxsus qaymoqli sous ostida "
                    "Aysberg salat bargi"
                    "<b> Narxi: 20000 so'm </b>",
            reply_markup=reply_markup,
            parse_mode="HTML"
        )

def handle_location(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    update.message.reply_text(get_text(chat_id, "adress_ask"))
    waiting_for_address[chat_id] = True

def handle_contact(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    if waiting_for_feedback_contact.get(chat_id):
        waiting_for_feedback_contact[chat_id] = False
        update.message.reply_text(get_text(chat_id, "feedback_received"))
        start(update, context)

def button_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat.id
    data = query.data

    query.answer()

    if data == "change_address":
        keyboard = [
            [KeyboardButton(get_text(chat_id, "send_address"), request_location=True)], [KeyboardButton("⬅️ Ortga")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        query.message.reply_text(get_text(chat_id, "send_address"), reply_markup=reply_markup)

    elif data.startswith("lang_"):
        lang = data.split("_")[1]
        user_language[chat_id] = lang
        query.message.reply_text(f"Til o'zgartirildi ✅ ({lang}) \n\nQayta /start bosing 😊")
        start(update, context)

    elif data.startswith("qty_"):
        qyt = int(data.split("_")[1])
        context.user_data["selected_qyt"] = qyt
        query.message.reply_text(f"{qyt} dona tanlandi ✅")

    elif data.startswith("add_"):
        product_key = data.split("_")[1]
        qyt = context.user_data.get("selected_qyt", 1)

        products = {
            "SirliBurger": {"name": "🍔 Chizburger", "price": 38000},
            "Lavash": {"name": "🌯 Lavash", "price": 37000},
            "Shaurma": {"name": "🥙 Shaurma", "price": 34000},
            "XotDog": {"name": "🌭 XotDog", "price": 20000},
        }

        product = products.get(product_key)
        if product:
            cart = user_cart.get(chat_id, [])
            cart.append({"name": product["name"], "price": product["price"], "qyt": qyt})
            user_cart[chat_id] = cart

            total_items = sum(item["qyt"] for item in cart)

            keyboard = [
                [InlineKeyboardButton(f"🛍 Savatni ko‘rish ({total_items} ta mahsulot)", callback_data="view_card")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            query.message.reply_text(
                f"{product['name']} x{qyt} savatga qo‘shildi ✅",
                reply_markup=reply_markup
            )
        else:
            query.message.reply_text(get_text(chat_id, "product_not_found"))


    elif data == "view_card":
        cart = user_cart.get(chat_id, [])
        if not cart:
            query.message.reply_text(get_text(chat_id, "empty_cart"))
        else:
            msg = get_text(chat_id, "your_cart")
            total = 0
            total_items = 0
            for item in cart:
                total += item["price"] * item["qyt"]
                total_items += item["qyt"]
                msg += f"{item['name']} x{item['qyt']} = {item['price'] * item['qyt']} so‘m\n"
            msg += f"\n📦 Umumiy: {total_items} ta mahsulot\n💰 Jami: {total} so‘m"
            query.message.reply_text(msg)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.location, handle_location))
    dp.add_handler(MessageHandler(Filters.contact, handle_contact))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dp.add_handler(CallbackQueryHandler(button_callback))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()