from telegram import (
    Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
)
from telegram.ext import (
    Updater, CommandHandler, MessageHandler,
    Filters, ConversationHandler, CallbackContext, CallbackQueryHandler
)

import db

TOKEN = '8406102443:AAECpk644W2D7LjB8qyP1xttV6s03CKKojI'
ADMIN_PASSWORD = "111"
ADMIN_IDS = set()

(
    NAME,
    PHONE,
    LOCATION,
    MAIN_MENU,
    EDIT_NAME,
    EDIT_PHONE,
    SETTINGS_MENU,
    FOOD_MENU,
) = range(8)

(
    ADD_CATEGORY_NAME,
    ADD_CATEGORY_EMOJI,
    ADD_PRODUCT_CATEGORY,
    ADD_PRODUCT_NAME,
    ADD_PRODUCT_PRICE,
    ADD_PRODUCT_DESC,
    ADD_PRODUCT_IMAGE,
    ADMIN_MENU,
) = range(8, 16)

CARD = {}
BOUND_GROUP_ID = None


def start(update: Update, context: CallbackContext):
    user = db.get_user(update.effective_user.id)
    if user:
        return main_menu(update, context)

    update.message.reply_text("👤️ Ism-Familyangizni kiriting: ")
    return NAME


def get_name(update, context):
    context.user_data["name"] = update.message.text
    update.message.reply_text(
        "🤙 Telefon raqamingizni yuboring: ",
        reply_markup=ReplyKeyboardMarkup(
            [[KeyboardButton("📞 Raqamni yuborish", request_contact=True)]],
            resize_keyboard=True
        )
    )
    return PHONE


def get_phone(update, context):
    context.user_data["phone"] = update.message.contact.phone_number
    update.message.reply_text(
        "👇 Locatsiyani yuboring",
        reply_markup=ReplyKeyboardMarkup(
            [[KeyboardButton("📍 Locatsiya", request_location=True)]],
            resize_keyboard=True
        )
    )
    return LOCATION


def get_location(update, context):
    loc = update.message.location

    db.add_user(
        update.effective_user.id,
        context.user_data["name"],
        context.user_data["phone"],
        loc.latitude,
        loc.longitude
    )

    update.message.reply_text("☑️ Ro'yxatdan o'tdingiz")
    return main_menu(update, context)


def main_menu(update, context):
    update.message.reply_text(
        "🏠 Asosiy sahifa:",
        reply_markup=ReplyKeyboardMarkup(
            [
                ["📝 Menu", "🛒 Savat"],
                ["⚙️ Sozlamalar"],
                ["💬 Izoh qoldirish"],
            ],
            resize_keyboard=True
        )
    )
    return MAIN_MENU


def main_menu_select(update, context):
    text = update.message.text

    if text == "📝 Menu":
        return food_menu(update, context)

    if text == "🛒 Savat":
        show_card_button(update, context)
        return MAIN_MENU

    if text == "⚙️ Sozlamalar":
        return settings_menu(update, context)
    return MAIN_MENU


def show_card_button(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    items = CARD.get(user_id)

    if not items:
        update.message.reply_text("Savat bo'sh")
        return

    text = "🛒 Savatingiz:\n\n"
    total = 0

    for i in items:
        item_total = i['qty'] * i['price']
        text += f"{i['name']} x{i['qty']} — {i['price']} so'm\n"
        total += item_total

    text += f"\n Jami: {total} so'm"

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🗑 Bekor qilish", callback_data="card_cancel")],
        [InlineKeyboardButton("📦 Buyurtma qilish", callback_data="card_confirm")],
    ])

    update.message.reply_text(text, reply_markup=keyboard)


def cart_action(update: Update, context: CallbackContext):
    global BOUND_GROUP_ID

    query = update.callback_query
    query.answer()
    user_id = query.from_user.id

    if query.data == "card_cancel":
        CARD.pop(user_id, None)
        query.edit_message_text("Savat tozalandi 🧹")
        return

    if query.data == "card_confirm":
        if not BOUND_GROUP_ID:
            query.edit_message_text(
                "⚠️ Guruh ulanmagan.\n"
                "Botni guruhga qo‘shib, u yerda /bind yozing."
            )
            return

        items = CARD.get(user_id)
        if not items:
            query.edit_message_text("❌ Savat bo'sh")
            return

        user = db.get_user(user_id)
        if not user:
            query.edit_message_text("❌ Foydalanuvchi topilmadi")
            return

        full_name = query.from_user.full_name
        phone = user[2]
        lat = user[3]
        lon = user[4]

        total = 0
        text = (
            "🆕 YANGI BUYURTMA\n\n"
            f"👤 {full_name}\n"
            f"📞 {phone}\n\n"
            "📦 Mahsulotlar:\n"
        )

        for item in items:
            text += (f"• {item['name']} — {item['price']} so‘m\n"
                     f"• {item['qty']} dona\n")
            total += int(item['price']) * int(item['qty'])

        text += f"\n💰 Jami: {total} so‘m"

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "📍 Location",
                    url=f"https://yandex.com/maps/?pt={lon},{lat}&z=16&l=map"
                )
            ]
        ])

        context.bot.send_photo(
            chat_id=BOUND_GROUP_ID,
            photo=items[0]['image'],
            caption=text,
            reply_markup=keyboard
        )

        CARD.pop(user_id, None)

        query.edit_message_text("✅ Buyurtmangiz qabul qilindi")


def bind_group(update: Update, context: CallbackContext):
    global BOUND_GROUP_ID

    if update.message.chat.type not in ['group', 'supergroup']:
        update.message.reply_text("Bu buyruq faqat guruhlar uchun ishlaydi")

    BOUND_GROUP_ID = update.message.chat.id
    update.message.reply_text("Guruh buyurtmalar uchun ulandi !")


def settings_menu(update, context):
    update.message.reply_text(
        "✏️ Ma'lumotlarni tahrirlash",
        reply_markup=ReplyKeyboardMarkup(
            [
                ["✏️ Ism-Familiya"],
                ["📞 Telefon raqami"],
                ["🔙 Orqaga"],
            ],
            resize_keyboard=True
        )
    )
    return SETTINGS_MENU


def settings_select(update, context):
    text = update.message.text

    if text == "✏️ Ism-Familiya":
        update.message.reply_text("📝 Yangi ism-familiyani kiriting: ")
        return EDIT_NAME

    if text == "📞 Telefon raqami":
        update.message.reply_text(
            "📞 Yangi telefon raqamni yuboring: ",
            reply_markup = ReplyKeyboardMarkup(
                [[KeyboardButton("Raqamni yuborish", request_contact=True)]],
                resize_keyboard=True)
            )
        return EDIT_PHONE

    if text == "🔙 Orqaga":
        return main_menu(update, context)


def edit_name(update, context):
    db.update_name(update.effective_user.id, update.message.text)
    update.message.reply_text("✅ Ism-Familiya muvafaqiyatli yangilandi")
    return main_menu(update, context)


def edit_phone(update, context):
    db.update_phone(update.effective_user.id, update.message.contact.phone_number)
    update.message.reply_text("✅ Telefon raqam muvafaqqiyatli yangilandi")
    return main_menu(update, context)


def food_menu(update, context):
    categories = db.get_category()

    keyboard = []
    row = []
    for cat_id, name, emoji in categories:
        row.append(f"{emoji} {name}")
        context.user_data[f"cat_{emoji} {name}"] = cat_id

        if len(row) == 2:
            keyboard.append(row)
            row = []

    if row:
        keyboard.append(row)

    keyboard.append(["🔙 Orqaga"])

    update.message.reply_text(
        "📋 Menyulardan birini tanlang: ",
        reply_markup=ReplyKeyboardMarkup(keyboard,resize_keyboard=True)
    )

    return FOOD_MENU


def food_menu_select(update, context):
    text = update.message.text

    if text == "🔙 Orqaga":
        return main_menu(update, context)

    category_id = context.user_data.get(f"cat_{text}")
    if not category_id:
        return FOOD_MENU

    products = db.get_products_by_category(category_id)
    if not products:
        update.message.reply_text("Bu categoryda mahsulot yo'q!")
        return FOOD_MENU


    for name, price, desc, image in products:
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("1", callback_data="qty_1"),
                InlineKeyboardButton("2", callback_data="qty_2"),
                InlineKeyboardButton("3", callback_data="qty_3"),
                InlineKeyboardButton("4", callback_data="qty_4"),
                InlineKeyboardButton("5", callback_data="qty_5"),
            ],
            [InlineKeyboardButton("Buyurtma qilish", callback_data=f"add_cart|{name}|{price}")]
        ])
        update.message.reply_photo(
            photo=image,
            caption=f"📜 {name}\n"
                    f"💰 {price}\n"
                    f"👆 {desc}",
            reply_markup=keyboard
        )
    return FOOD_MENU


def add_to_cart(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    data = query.data
    msg_id = query.message.message_id

    if data.startswith("qty_"):
        qty = int(data.split("_")[1])
        context.user_data[f"qty_{msg_id}"] = qty

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("1", callback_data="qty_1"),
                InlineKeyboardButton("2", callback_data="qty_2"),
                InlineKeyboardButton("3", callback_data="qty_3"),
                InlineKeyboardButton("4", callback_data="qty_4"),
                InlineKeyboardButton("5", callback_data="qty_5"),
            ],
            [
                InlineKeyboardButton(
                    "🛒 Buyurtma qilish",
                    callback_data=query.message.reply_markup.inline_keyboard[1][0].callback_data
                )
            ]
        ])

        base_caption = query.message.caption.split("\n\n🧮")[0]

        query.edit_message_caption(
            caption=base_caption + f"\n\n🧮 Tanlangan miqdor: {qty} dona",
            reply_markup=keyboard
        )
        return

    qty = context.user_data.get(f"qty_{msg_id}", 1)

    _, name, price = data.split('|')
    user_id = query.from_user.id

    try:
        price = int(price)
    except ValueError:
        query.answer("❌ Narx noto‘g‘ri", show_alert=True)
        return

    CARD.setdefault(user_id, []).append({
        'name': name,
        'price': price,
        'qty': qty,
        'image': query.message.photo[-1].file_id,
    })

    query.edit_message_caption(
        query.message.caption + f"\n\n🛒 Savatga qo‘shildi: {qty} dona"
    )


def admin_login(update, context):
    if not context.args or context.args[0] != ADMIN_PASSWORD:
        update.message.reply_text("❌ /admin parol")
        return ConversationHandler.END

    ADMIN_IDS.add(update.effective_user.id)
    update.message.reply_text(
        "🔐 Admin panelga hush kelibsiz",
        reply_markup=ReplyKeyboardMarkup(
            [
                ["➕ Kategoriya"],
                ["➕ Mahsulot"]
            ],
            resize_keyboard=True
        )
    )
    return ADMIN_MENU


def admin_menu_select(update, context):
    text = update.message.text

    if text == "➕ Kategoriya":
        update.message.reply_text("Kategoriya nomini kiriting: ")
        return ADD_CATEGORY_NAME

    if text == "➕ Mahsulot":
        categories = db.get_category()
        keyboard = []

        for cat_id, name, emoji in categories:
            key = f"{emoji} {name}"
            keyboard.append([key])
            context.user_data[f"admin_cat_{key}"] = cat_id

        keyboard.append(["🔙 Orqaga"])
        update.message.reply_text("Kategoriya tanlang",
                                  reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
        return ADD_PRODUCT_CATEGORY

    return ADMIN_MENU


def add_category_name(update, context):
    context.user_data["new_cat_name"] = update.message.text
    update.message.reply_text("Emoji yuboring")
    return ADD_CATEGORY_EMOJI


def add_category_emoji(update, context):
    name = context.user_data["new_cat_name"]
    emoji = update.message.text

    db.add_category(name, emoji)

    update.message.reply_text(
        "✅ Kategoriya qo‘shildi",
        reply_markup=ReplyKeyboardMarkup(
            [
                ["➕ Kategoriya"],
                ["➕ Mahsulot"]
            ],
            resize_keyboard=True
        )
    )

    update.message.reply_text("✅ Kategoriya qo‘shildi")
    return ADMIN_MENU


def add_product_category(update, context):
    text = update.message.text

    if text == "🔙 Orqaga":
        return ADMIN_MENU

    category_id = None
    for key, value in context.user_data.items():
        if key.startswith("admin_cat_") and text in key:
            category_id = value
            break

    if not category_id:
        return ADD_PRODUCT_CATEGORY

    context.user_data["product_category"] = category_id
    update.message.reply_text("Mahsulot nomini kiriting: ")
    return ADD_PRODUCT_NAME


def add_product_name(update, context):
    context.user_data["product_name"] = update.message.text
    update.message.reply_text("Narxini kiriting: ")
    return ADD_PRODUCT_PRICE


def add_product_price(update, context):
    try:
        context.user_data["product_price"] = int(update.message.text)
    except ValueError:
        update.message.reply_text("❌ Faqat raqam kiriting (masalan: 25000)")
        return ADD_PRODUCT_PRICE

    update.message.reply_text("Mahsulot rasmini yuboring: ")
    return ADD_PRODUCT_IMAGE


def add_product_image(update, context):
    photo = update.message.photo[-1]
    context.user_data["product_image"] = photo.file_id
    update.message.reply_text("Mahsulotga qisqacha izoh kiriting: ")
    return ADD_PRODUCT_DESC


def add_product_desc(update, context):
    db.add_products(
        context.user_data["product_category"],
        context.user_data["product_name"],
        context.user_data["product_price"],
        update.message.text,
        context.user_data["product_image"]
    )

    update.message.reply_text(
        "✅ Mahsulot qo'shildi\n"
        "➕ Qo'shish uchun bosing: ",
        reply_markup=ReplyKeyboardMarkup(
            [
                ["➕ Kategoriya"], ["➕ Mahsulot"]
            ],
            resize_keyboard=True
        )
    )
    return ADMIN_MENU


def main():
    db.create_table()

    updater = Updater(TOKEN)
    dp = updater.dispatcher


    conv = ConversationHandler(
        entry_points=[
            CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(Filters.text & ~Filters.command, get_name)],
            PHONE: [MessageHandler(Filters.contact & ~Filters.command, get_phone)],
            LOCATION: [MessageHandler(Filters.location & ~Filters.command, get_location)],

            MAIN_MENU: [MessageHandler(Filters.text & ~Filters.command, main_menu_select)],
            SETTINGS_MENU: [MessageHandler(Filters.text & ~Filters.command, settings_select)],
            FOOD_MENU: [MessageHandler(Filters.text & ~Filters.command, food_menu_select)],

            EDIT_NAME: [MessageHandler(Filters.text & ~Filters.command, edit_name)],
            EDIT_PHONE: [MessageHandler(Filters.contact & ~Filters.command, edit_phone)],

        },
        fallbacks=[]
    )

    admin_conv = ConversationHandler(
        entry_points=[CommandHandler("admin", admin_login)],
        states={
            ADMIN_MENU: [
                MessageHandler(Filters.text & ~Filters.command, admin_menu_select)
            ],
            ADD_CATEGORY_NAME: [
                MessageHandler(Filters.text & ~Filters.command, add_category_name)
            ],
            ADD_CATEGORY_EMOJI: [
                MessageHandler(Filters.text & ~Filters.command, add_category_emoji)
            ],
            ADD_PRODUCT_CATEGORY: [
                MessageHandler(Filters.text & ~Filters.command, add_product_category)
            ],
            ADD_PRODUCT_NAME: [
                MessageHandler(Filters.text & ~Filters.command, add_product_name)
            ],
            ADD_PRODUCT_PRICE: [
                MessageHandler(Filters.text & ~Filters.command, add_product_price)
            ],
            ADD_PRODUCT_IMAGE: [
                MessageHandler(Filters.photo, add_product_image)
            ],
            ADD_PRODUCT_DESC: [
                MessageHandler(Filters.text & ~Filters.command, add_product_desc)
            ],
        },
        fallbacks=[]
    )


    dp.add_handler(CommandHandler("bind", bind_group))
    dp.add_handler(CallbackQueryHandler(add_to_cart, pattern="^(qty_|add_cart)"))
    dp.add_handler(CallbackQueryHandler(cart_action))

    dp.add_handler(admin_conv)
    dp.add_handler(conv)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()