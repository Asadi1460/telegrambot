import telebot

API_TOKEN = '7136642440:AAFHEj4dbLprbHUJdVLxgMU6ku2WWw1WRyQ'
bot = telebot.TeleBot(API_TOKEN)

# List to store students' info
students = []

# Card number to show
CARD_NUMBER = '6037 9975 3223 2908'

# Command handler for /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "به ربات ثبت‌نام کلاس پایتون خوش آمدید.")
    # bot.reply_to(message, "Welcome to the Python course registration bot!")
    # time.sleep(1)  # Short delay to ensure messages are read sequentially
    bot.reply_to(message, "لطفا نام و نام خانوادگی خود را وارد نمایید:")

# State to track registration process
user_state = {}

# Message handler for collecting user info
@bot.message_handler(func=lambda message: True)
def collect_info(message):
    user_id = message.from_user.id

    if user_id not in user_state:
        user_state[user_id] = 'name'
        bot.reply_to(message, "Please enter your name:")
        return

    if user_state[user_id] == 'name':
        name = message.text
        user_state[user_id] = {'name': name, 'phone': None}
        bot.reply_to(message, f"Thank you, {name}! Now, please enter your phone number:")

    elif isinstance(user_state[user_id], dict) and user_state[user_id]['phone'] is None:
        phone = message.text
        user_state[user_id]['phone'] = phone
        name = user_state[user_id]['name']
        students.append({'name': name, 'phone': phone})
        bot.reply_to(message, f"Registration complete!\nName: {name}\nPhone: {phone}\n\nPlease use the following card number for payment:\n{CARD_NUMBER}")
        del user_state[user_id]

# Start polling
print('Starting bot ...')
bot.polling()
