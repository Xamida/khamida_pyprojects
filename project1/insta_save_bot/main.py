import time

from telegram import Update
from telegram.ext import Updater, CallbackContext, Filters, MessageHandler
import os
import instaloader
import re

TOKEN = "8406102443:AAGhBx_pyiPpX8alUL2BfRxAnD1xoTjqQtU"

L = instaloader.Instaloader(
    download_comments=False,
    download_pictures=False,
    save_metadata=False,
    download_video_thumbnails=False
)

L.load_session_from_file("__kham1.da__")


def short_cut(url: str):
    match = re.search(r"instagram\.com/(?:p|reel|tv)/([^/?]+)", url)
    return match.group(1) if match else None


def handle_message(update: Update, context: CallbackContext):
    text = update.message.text

    if "instagram.com" not in text:
        update.message.reply_text("Intagram link to'g'ri yuboring!")
        return

    shortcode = short_cut(text)
    if not shortcode:
        update.message.reply_text("Link to'g'ri emas!")

    try:
        update.message.reply_text("Video yuklanmoqda...")

        time.sleep(10)

        post = instaloader.Post.from_shortcode(L.context, shortcode)
        L.download_post(post, target="download")

        for file in os.listdir("download"):
            if file.endswith(".mp4"):
                path = f"download/{file}"
                update.message.reply_video(video=open(path, "rb"))
                os.remove(path)

        update.message.reply_text("Tayyor !")

    except Exception as e:
        update.message.reply_text("Video olishda xatolik !")
        print(e)


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
