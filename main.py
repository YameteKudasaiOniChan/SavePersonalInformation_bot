from telebot import TeleBot, types
from dotenv import load_dotenv
import os
import SqlHandler

load_dotenv()
bot = TeleBot(os.getenv("bot_token"))


@bot.message_handler(commands=["start"])
def start_handler(message):
    bot.send_message(
        chat_id=message.from_user.id,
        text="welcome dear user",
        reply_markup=None,
        reply_to_message_id=message.id
    )
    SqlHandler.add_user(message.from_user.id)
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row_width = 1
    keyboard.add(
        types.InlineKeyboardButton("Complete register", callback_data="complete register")
    )
    bot.send_message(
        chat_id=message.from_user.id,
        text="please complete your registration",
        reply_markup=keyboard,
        reply_to_message_id=message.id
    )


def complete_register(message):
    bot.send_message(
        chat_id=message.from_user.id,
        text="please enter your",
        reply_markup=None,
        reply_to_message_id=None
    )


@bot.callback_query_handler(func=lambda call: call.data)
def callback_query(call):
    if call.data == "complete register":
        print("called")
        complete_register(call)
    else:
        print("call")


if __name__ == "__main__":
    SqlHandler.create_database()
    SqlHandler.create_table()
    bot.infinity_polling()
