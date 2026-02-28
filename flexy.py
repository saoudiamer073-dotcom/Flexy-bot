import os
import telebot
from telebot import types

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_ID = 123456789  # حط هنا رقمك من @userinfobot

bot = telebot.TeleBot(TOKEN)

user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "مرحبا بك في بوت Flexy 💳\nارسل رقم الهاتف:")

@bot.message_handler(func=lambda m: m.text.isdigit() and len(m.text) >= 8)
def get_phone(message):
    user_data[message.chat.id] = {"phone": message.text}

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("100 دج", "200 دج")
    markup.add("500 دج", "1000 دج")

    bot.send_message(message.chat.id, "اختر المبلغ:", reply_markup=markup)

@bot.message_handler(func=lambda m: "دج" in m.text)
def get_amount(message):
    phone = user_data.get(message.chat.id, {}).get("phone")
    amount = message.text

    if not phone:
        bot.send_message(message.chat.id, "ارسل رقم الهاتف أولاً.")
        return

    bot.send_message(message.chat.id, "✅ تم استلام طلبك وسيتم التحويل قريباً.",
                     reply_markup=types.ReplyKeyboardRemove())

    bot.send_message(ADMIN_ID,
                     f"📥 طلب جديد\n📱 رقم: {phone}\n💰 مبلغ: {amount}")

bot.polling()
