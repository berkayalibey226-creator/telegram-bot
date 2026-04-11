import telebot

TOKEN = "8542662196:AAFPxpjOZROlqeGvzdsjv8mRCeU6enLccFM"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Bot çalışıyor ✅")

print("Bot çalışıyor...")
bot.infinity_polling()
