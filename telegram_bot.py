#!/usr/bin/python


import sys
import json
import telebot  # Telegram bot library
import Adafruit_BMP.BMP085 as BMP085  # Sensor library
import messages_en as custom_messages  # Import the messages module ("messages_es" for spanish)
import logger

BOT_TOKEN = '_INTRODUCE_YOUR_BOT_TOKEN_HERE'
DEVELOPER_PASSWORD = "YOUR_DEVELOPER_PASSWORD"

DEVELOPERS_FILE = "developers.json"
LOG_FILE = "bot_history.log"

sensor = BMP085.BMP085()
developers = []
waiting_for_password = {}

# Initialize bot
bot = telebot.TeleBot(BOT_TOKEN)

# Logging function
def log_event(message):
    log_message = f"{message}"
    logger.log(log_message, LOG_FILE)

# Send message without parsing
def send_user_no_parse(message, chat_id):
    bot.send_message(chat_id, text=message)
    log_event(f"Sent message: {message} to {chat_id}")

# Send message with MarkdownV2 parsing
def send_user(message, chat_id):
    bot.send_message(chat_id, text=message, parse_mode='MarkdownV2')
    log_event(f"Sent message: {message} to {chat_id}")

# Send a file to the user
def send_file(file_path, chat_id):
    with open(file_path, 'rb') as f:
        bot.send_document(chat_id, f)
    log_event(f"Sent file: {file_path} to {chat_id}")

# Measure temperature and returns it formatted to two decimal places.
def measure_temp():
    temp = sensor.read_temperature()
    return f"{temp:.2f}"

# Measure pressure and returns it formatted to two decimal places.
def measure_pressure():
    pressure = sensor.read_pressure() / 100.0  # Convert to millibars
    return f"{pressure:.2f}"

# Load developers from file
def load_developers():
    global developers
    try:
        with open(DEVELOPERS_FILE, 'r') as f:
            developers = json.load(f)
    except FileNotFoundError:
        developers = []

# Save developers to file
def save_developers():
    with open(DEVELOPERS_FILE, 'w') as f:
        json.dump(developers, f)

# Handler for text commands
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global waiting_for_password
    chat_id = message.chat.id
    command = message.text.lower()
    message_id = message.message_id

    # Log every command if not waiting for password
    if waiting_for_password.get(chat_id) is None:
        log_event(f"Received command: {command} from {chat_id}")

    # If waiting for password for developer mode. If the correct password is given, add to developers.
    # Delete the message with the password when done.
    if waiting_for_password.get(chat_id):
        if command == DEVELOPER_PASSWORD:
            if chat_id not in developers:
                developers.append(chat_id)
                save_developers()
            send_user(custom_messages.dev_mode_on, chat_id)
            send_user(custom_messages.help_developer, chat_id)
            log_event(f"Developer added: {chat_id}")
        else:
            send_user(custom_messages.wrong_password, chat_id)

        waiting_for_password[chat_id] = None

        try:
            bot.delete_message(chat_id, message_id)
        except Exception:
            pass
        return

    # Handle commands
    if command == 'hello':
        send_user(custom_messages.hello, chat_id)

    elif command == 'help':
        if chat_id in developers:
            send_user(custom_messages.help_developer, chat_id)
        else:
            send_user(custom_messages.help, chat_id)

    elif command == 'temperature':
        send_user_no_parse(measure_temp() + " ºC", chat_id)

    elif command == 'pressure':
        send_user_no_parse(measure_pressure() + " mbar", chat_id)

    elif command == 'developer':
        if chat_id in developers:
            send_user(custom_messages.dev_mode_already_active, chat_id)
        else:
            send_user(custom_messages.input_password, chat_id)
            waiting_for_password[chat_id] = True

    elif command == 'logout':
        if chat_id in developers:
            developers.remove(chat_id)
            save_developers()
            send_user(custom_messages.dev_mode_off, chat_id)
            send_user(custom_messages.help, chat_id)

    elif command == 'log' and chat_id in developers:
        send_file(LOG_FILE, chat_id)

    else:
        if chat_id in developers:
            send_user(custom_messages.help_developer, chat_id)
        else:
            send_user(custom_messages.help, chat_id)


if __name__ == '__main__':
    print(">>> Starting system")
    load_developers()
    print(">>> Developers loaded")
    print("\n")
    print('I am listening...')
    try:
        bot.infinity_polling()
    except KeyboardInterrupt:
        print('\n Program interrupted')
        sys.exit(0)