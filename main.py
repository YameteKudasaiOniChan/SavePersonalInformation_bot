import telebot.types
from telebot import TeleBot, types
from dotenv import load_dotenv
import os
import SqlHandler
from person import Person, person_dict

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
    # creating new person to record information
    data = Person(message.from_user.id)
    person_dict[message.from_user.id] = data
    person = person_dict[message.from_user.id]
    # preparing for first step
    msg = bot.send_message(
        chat_id=message.from_user.id,
        text="What is first name?",
        reply_markup=types.ForceReply(),
        reply_to_message_id=None
    )
    bot.register_next_step_handler(msg, process_firstname_step)


def process_firstname_step(message):
    # set first name
    person = person_dict[message.from_user.id]
    person.first_name = message.text
    # preparing for next step
    msg = bot.send_message(
        chat_id=message.from_user.id,
        text="What is your last name?",
        reply_markup=types.ForceReply(),
        reply_to_message_id=None
    )
    bot.register_next_step_handler(msg, process_lastname_step)


def process_lastname_step(message):
    # set last name
    person = person_dict[message.from_user.id]
    person.last_name = message.text
    # preparing for next step
    msg = bot.send_message(
        chat_id=message.from_user.id,
        text="How old are you? (just numbers)",
        reply_markup=types.ForceReply(),
        reply_to_message_id=None
    )
    bot.register_next_step_handler(msg, process_age_step)


def process_age_step(message):
    # checking whether the age is numeric
    age = message.text
    if not age.isdigit():
        msg = bot.reply_to(message, 'Age should be a number. How old are you?')
        bot.register_next_step_handler(msg, process_age_step)
        return
    # set info, if the age is numer
    person = person_dict[message.from_user.id]
    person.age = age
    # preparing for next step
    # creating a markup keyboard for this step
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    keyboard.add('Male', 'Female')
    msg = bot.send_message(
        chat_id=message.from_user.id,
        text="What is your gender?",
        reply_markup=keyboard,
        reply_to_message_id=None
    )
    bot.register_next_step_handler(msg, process_gender_step)


def process_gender_step(message):
    gender = message.text
    person = person_dict[message.from_user.id]
    if (gender == u'Male') or (gender == u'Female'):
        # set gender
        person.gender = gender
        msg = bot.send_message(
            chat_id=message.from_user.id,
            text="What is your job?",
            reply_markup=types.ForceReply(),
            reply_to_message_id=None
        )
        bot.register_next_step_handler(msg, process_job_step)
    else:
        keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        keyboard.add('Male', 'Female')
        msg = bot.send_message(
            chat_id=message.from_user.id,
            text="Unknown gender, Please use bot keyboard",
            reply_markup=keyboard,
            reply_to_message_id=None
        )
        bot.register_next_step_handler(msg, process_gender_step)


def process_job_step(message):
    person = person_dict[message.from_user.id]
    person.job = message.text
    # finally
    person = person_dict[message.from_user.id]
    SqlHandler.update_user(message.from_user.id, person)


@bot.callback_query_handler(func=lambda call: call.data)
def callback_query(call):
    if call.data == "complete register":
        complete_register(call)


if __name__ == "__main__":
    SqlHandler.create_database()
    SqlHandler.create_table()
    bot.infinity_polling()
