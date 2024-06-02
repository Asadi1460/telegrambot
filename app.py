import telebot
import csv
from datetime import datetime

API_TOKEN = '7266022641:AAHuP-4oy9D7MTpU0IfzxGVsI3HGy0gCcXw'
bot = telebot.TeleBot(API_TOKEN)

# Set to store registered user IDs
registered_users = set()

# List to store students' info
students = []

# Card number to show
CARD_NUMBER = '6037 9975 3223 2908'
PHONE_NUMBER = '0939-333-8100'


# State to track registration process
user_state = {}

# Function to save student data to CSV
def save_to_csv(username, name, phone, registration_time):
    with open('students.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([username, name, phone, registration_time])

# Function to update student data in CSV
def update_csv(username, name, phone):
    registration_time = None
    # Read existing data and update the corresponding record
    with open('students.csv', mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        rows = list(reader)
        for row in rows:
            if row[0] == username:
                row[1] = name
                row[2] = phone
                registration_time = row[3]
                break
    # Write the updated data back to CSV
    with open('students.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(rows)
    return registration_time

# Command handler for /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    if user_id in registered_users:
        bot.reply_to(message, "شما قبلا ثبت‌نام کرده‌اید.")
    else:
        bot.reply_to(message, "به ربات ثبت‌نام کلاس پایتون خوش آمدید\n\n لطفا نام خود را وارد نمایید:")
        user_state[user_id] = {'state': 'waiting_for_first_name'}

# Command handler for /revise
@bot.message_handler(commands=['revise'])
def revise_registration(message):
    user_id = message.from_user.id
    if user_id not in registered_users:
        bot.reply_to(message, "شما هنوز ثبت‌نام نکرده‌اید. لطفاً ابتدا ثبت‌نام کنید.")
    else:
        bot.reply_to(message, "لطفاً نام خود را وارد کنید:")
        user_state[user_id] = {'state': 'waiting_for_revised_name'}

# Message handler for collecting user info
@bot.message_handler(func=lambda message: True)
def collect_info(message):
    user_id = message.from_user.id
    if user_id in user_state:
        current_state = user_state[user_id]['state']

        if current_state == 'waiting_for_first_name':
            user_state[user_id]['first_name'] = message.text
            bot.reply_to(message, "لطفا نام خانوادگی خود را وارد نمایید:")
            user_state[user_id]['state'] = 'waiting_for_last_name'

        elif current_state == 'waiting_for_last_name':
            user_state[user_id]['last_name'] = message.text
            bot.reply_to(message, "لطفا شماره تلفن خود را وارد نمایید:")
            user_state[user_id]['state'] = 'waiting_for_phone'

        elif current_state == 'waiting_for_phone':
            user_state[user_id]['phone'] = message.text
            first_name = user_state[user_id]['first_name']
            last_name = user_state[user_id]['last_name']
            phone = user_state[user_id]['phone']
            username = message.from_user.username if message.from_user.username else f"User ID {user_id}"
            registration_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            save_to_csv(username, f"{first_name} {last_name}", phone, registration_time)
            registered_users.add(user_id)
            bot.reply_to(message, f"ثبت نام شما کامل شد!\nنام: {first_name} {last_name}\nتلفن: {phone}\n\nجهت کسب اطلاعات بیشتر با شماره زیر تماس بگیرید:\n{PHONE_NUMBER}\n\n")
            del user_state[user_id]

        elif current_state == 'waiting_for_revised_name':
            user_state[user_id]['first_name'] = message.text
            bot.reply_to(message, "لطفاً نام خانوادگی خود را وارد کنید:")
            user_state[user_id]['state'] = 'waiting_for_revised_last_name'

        elif current_state == 'waiting_for_revised_last_name':
            user_state[user_id]['last_name'] = message.text
            bot.reply_to(message, "لطفاً شماره تلفن خود را وارد کنید:")
            user_state[user_id]['state'] = 'waiting_for_revised_phone'

        elif current_state == 'waiting_for_revised_phone':
            new_name = user_state[user_id]['first_name'] + ' ' + user_state[user_id]['last_name']
            new_phone = message.text
            username = message.from_user.username if message.from_user.username else f"User ID {user_id}"
            registration_time = update_csv(username, new_name, new_phone)
            bot.reply_to(message, f"اطلاعات شما با موفقیت به‌روز شد!\nنام: {new_name}\nتلفن: {new_phone}\n\nجهت کسب اطلاعات بیشتر با شماره زیر تماس بگیرید:\n{PHONE_NUMBER}")

            del user_state[user_id]

# Start polling
print('Starting bot ...')
bot.polling()

