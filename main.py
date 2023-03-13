import os
import telebot
import qrcode
from io import BytesIO
import time
import validators
import re

print("Starting bot...")

# Define the Telegram bot token and create an Updater object
TOKEN = os.environ["URL2QR_BOT_TOKEN"]
bot = telebot.TeleBot(TOKEN)


def generate_qr_code(url):
    # Generate QR code
    img = qrcode.make(url)

    # Convert the image to a PNG file in memory
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    return buffer


def send_message(message, refined_message):
    if validators.url(refined_message):
        # Generate QR code from the URL in a separate thread
        qr_code = generate_qr_code(refined_message)

        # Send the QR code image back to the user
        bot.send_photo(message.chat.id, qr_code)
    else:
        bot.send_message(message.chat.id, "Invalid URL. Please enter a valid URL.")

# Start command
@bot.message_handler(commands=["start"])
def start_command(message):
    bot.send_message(message.chat.id, '''
Welcome, You can use this Bot to convert any valid url into a QR code.
Commands:
/help -> guidance on how to use the Bot
/creator -> get the name of the person who developed this Bot

Start by sending a url as text. If the URL is not valid you will be notified.
If using in a group make sure to add @url2qr_bot anywhere in your message.
Example URL: https://example.com
    ''')

#Creator command
@bot.message_handler(commands=["creator"])
def creator_command(message):
    bot.send_message(message.chat.id, '''
This Bot is built by Sahil Yadav.
Some links to get in touch:
Github : https://github.com/Sahil481
Linkedin : https://www.linkedin.com/in/sahil-yadav-970398246
    ''')

# Help command
@bot.message_handler(commands=["help"])
def help_command(message):
    bot.send_message(message.chat.id, '''
Commands:
/help -> guidance on how to use the Bot
/creator -> get the name of the person who developed this Bot

Start by sending a url as text. If the URL is not valid you will be notified.
If using in a group make sure to add @url2qr_bot anywhere in your message.
Example URL: https://example.com
    ''')


# Getting the url from text
@bot.message_handler(content_types=["text"])
def handle_message(message):
    # Get the message text from the user
    if message.chat.type == "private":
        if "@url2qr_bot" in message.text.lower():
            pattern = "@[Uu][Rr][Ll]2[Qq][Rr](?i)_bot\\s*"
            clean_text = re.sub(pattern, "", message.text)
            send_message(message, clean_text)
        else:
            send_message(message, message.text)
    elif "@url2qr_bot" in message.text.lower():
        pattern = "@[Uu][Rr][Ll]2[Qq][Rr](?i)_bot\\s*"
        clean_text = re.sub(pattern, "", message.text)
        send_message(message, clean_text)


# Create a MessageHandler that listens for text messages and calls the handle_message function
while True:
    try:
        bot.polling(non_stop=True, interval=1, timeout=0)
    except Exception as e:
        print(e)
        time.sleep(5)
