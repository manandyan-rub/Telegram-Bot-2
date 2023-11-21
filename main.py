TOKEN = "YOUR_TOKEN"

from telebot import TeleBot
from get_comics import return_comics

bot = TeleBot(TOKEN)


@bot.message_handler(commands=['hello'])
def send_welcome(message):
    bot.reply_to(message, "Hi " + message.from_user.first_name + "!")


@bot.message_handler(commands=['start'])
def start(message):
    markup = create_markup()
    bot.send_message(message.chat.id, "Select 5 characters:", reply_markup=markup)


user_click_counts = {}
chose_heroes = []


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id
    user_name = call.from_user.username
    if user_id not in user_click_counts:
        user_click_counts[user_id] = 0

    if user_click_counts[user_id] >= 5:
        bot.answer_callback_query(call.id, text="You've reached the maximum allowed clicks (5).")
    else:
        bot.answer_callback_query(call.id, text=f"You selected: {call.data}")
        user_click_counts[user_id] += 1
        chose_heroes.append(call.data)
    if user_click_counts[user_id] == 5:
        bot.send_message(chat_id=user_id, text="Your request is in progress")
        bot.send_message(chat_id=user_id, text=f"{return_comics(chose_heroes)}")
        user_click_counts[user_id] = 0

    print(f"{user_name} ({user_id}) clicked {user_click_counts[user_id]} times.")
    print(chose_heroes)


def create_markup():
    from telebot import types
    most_popular_24_heroes = ["Scarlet Witch", "Valkyrie", "Jessica Jones", "Hawkeye", "Rocket", "Winter Soldier",
                              "Falcon",
                              "Nebula", "Gamora", "Phil Coulson", "Nick Fury", "Doctor Strange",
                              "Wong", "Star-Lord", "Daredevil", "Peggy" "Carter", "Ant-Man", "Hulk", "Black Panther",
                              "Black Widow", "Spider-Man", "Thor", "Iron Man", "Captain America"]
    markup = types.InlineKeyboardMarkup()
    array_of_options = []
    for i in most_popular_24_heroes:
        array_of_options.append(types.InlineKeyboardButton(f"{i}", callback_data=f"{i}"))
    markup.add(*array_of_options)
    return markup


if __name__ == "__main__":
    bot.polling()
