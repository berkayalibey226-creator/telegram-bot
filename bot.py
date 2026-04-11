import telebot
from telebot.types import ReplyKeyboardMarkup

TOKEN = "BURAYA_TOKENINI_YAPISTIR"

bot = telebot.TeleBot(TOKEN)

VIP_PASSWORD = "1234"
vip_open_users = set()


def ana_menu():
    m = ReplyKeyboardMarkup(resize_keyboard=True)
    m.row("👾 HAKKIMDA💀")
    m.row("💎 Vip Bölme 💎")
    m.row("🫣 BEYANNIM 🧑‍💼", "📶 Bedava internet 💥")
    m.row("🧑‍🏫 EĞİTİM SETLERİ 🧑‍🏫")
    m.row("Referans 👥", "Bakiye 💰")
    m.row("📞 İLETİŞİM 📮")
    m.row("🟡 Altın Fiyatları 💰")
    return m


def vip_menu():
    m = ReplyKeyboardMarkup(resize_keyboard=True)
    m.row("😈 Instagram Canlı Kapatma 🚷")
    m.row("🔇 INSTAGRAM BANNED")
    m.row("🛄 GMAIL ONAY SİTELERİ 📥")
    m.row("🚀 Sms Onay Siteleri 📩")
    m.row("📮 Anonim Mesaj Gönderme 📮")
    m.row("👨‍💻 REFERANS BOTU YAPMA 👾")
    m.row("🌹 Bedava İzlenme Ve Tepki 🌹")
    m.row("🔙 Ana Menü")
    return m


def egitim_menu():
    m = ReplyKeyboardMarkup(resize_keyboard=True)
    m.row("📸 Instagram İçin Eğitim Seti")
    m.row("🔥 Enes Turan Eğitim Seti")
    m.row("⚡ Barış Reus Eğitim Seti")
    m.row("🔙 Ana Menü")
    return m


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "Bot çalışıyor ✅\n\nMenü hazır 👇",
        reply_markup=ana_menu()
    )


@bot.message_handler(func=lambda message: True)
def handle_all(message):
    text = message.text
    user_id = message.from_user.id

    if text == "👾 HAKKIMDA💀":
        bot.send_message(
            message.chat.id,
            "╰┈➤ Bu Bot @MTX_GLOBAL_TR Tarafından Yapılmıştır.\nİstek-Öneri-Şikayet İçin Bana Yazabilirsiniz.",
            reply_markup=ana_menu()
        )

    elif text == "💎 Vip Bölme 💎":
        bot.send_message(
            message.chat.id,
            "VIP bölümü için şifre gönder.",
            reply_markup=ana_menu()
        )

    elif text == VIP_PASSWORD:
        vip_open_users.add(user_id)
        bot.send_message(
            message.chat.id,
            "✅ Şifre doğru. VIP menü açıldı.",
            reply_markup=vip_menu()
        )

    elif text == "🔙 Ana Menü":
        bot.send_message(
            message.chat.id,
            "Ana menüye döndün.",
            reply_markup=ana_menu()
        )

    elif text == "🫣 BEYANNIM 🧑‍💼":
        bot.send_message(
            message.chat.id,
            "🚀 Aşağıdaki Linki Biyografinize Ekliyebilirsiniz 🚀\nhttps://telegra.ph/BEYANNIM-09-17",
            reply_markup=ana_menu()
        )

    elif text == "📶 Bedava internet 💥":
        bot.send_message(
            message.chat.id,
            "Bedava internet bölümü açıldı.",
            reply_markup=ana_menu()
        )

    elif text == "🧑‍🏫 EĞİTİM SETLERİ 🧑‍🏫":
        bot.send_message(
            message.chat.id,
            "📚 Eğitim setleri menüsü",
            reply_markup=egitim_menu()
        )

    elif text == "📸 Instagram İçin Eğitim Seti":
        bot.send_message(
            message.chat.id,
            "《İ𝐍𝐒𝐓𝐀𝐆𝐑𝐀𝐌 İÇİ𝐍 𝐄Ğİ𝐓İ𝐌 𝐒𝐄𝐓İ》",
            reply_markup=egitim_menu()
        )

    elif text == "🔥 Enes Turan Eğitim Seti":
        bot.send_message(
            message.chat.id,
            "Enes Turan eğitim setleri bölümü açıldı.",
            reply_markup=egitim_menu()
        )

    elif text == "⚡ Barış Reus Eğitim Seti":
        bot.send_message(
            message.chat.id,
            "Barış Reus eğitim seti bölümü açıldı.",
            reply_markup=egitim_menu()
        )

    elif text == "Referans 👥":
        bot.send_message(
            message.chat.id,
            "Referans sistemi yakında eklenecek.",
            reply_markup=ana_menu()
        )

    elif text == "Bakiye 💰":
        bot.send_message(
            message.chat.id,
            "Bakiyen: 10",
            reply_markup=ana_menu()
        )

    elif text == "📞 İLETİŞİM 📮":
        bot.send_message(
            message.chat.id,
            "Mesajınızı yazın 24 saat içersinde dönüş yapılacaktır.",
            reply_markup=ana_menu()
        )

    elif text == "🟡 Altın Fiyatları 💰":
        bot.send_message(
            message.chat.id,
            "Altın fiyat sistemi sonra eklenecek.",
            reply_markup=ana_menu()
        )

    elif text in [
        "😈 Instagram Canlı Kapatma 🚷",
        "🔇 INSTAGRAM BANNED",
        "🛄 GMAIL ONAY SİTELERİ 📥",
        "🚀 Sms Onay Siteleri 📩",
        "📮 Anonim Mesaj Gönderme 📮",
        "👨‍💻 REFERANS BOTU YAPMA 👾",
        "🌹 Bedava İzlenme Ve Tepki 🌹"
    ]:
        if user_id not in vip_open_users:
            bot.send_message(
                message.chat.id,
                "Önce VIP şifresini girmen gerekiyor.",
                reply_markup=ana_menu()
            )
            return

        if text == "😈 Instagram Canlı Kapatma 🚷":
            bot.send_message(message.chat.id, "Instagram Canlı Kapatma bölümü açıldı.", reply_markup=vip_menu())

        elif text == "🔇 INSTAGRAM BANNED":
            bot.send_message(message.chat.id, "Instagram Banned bölümü açıldı.", reply_markup=vip_menu())

        elif text == "🛄 GMAIL ONAY SİTELERİ 📥":
            bot.send_message(
                message.chat.id,
                "📧 4 Tane Gmail Onay Sitesi\n\n"
                "● https://tempail.com/\n\n"
                "● https://www.fakemail.net/\n\n"
                "● https://mail.tm/en/\n\n"
                "● https://temp-mail.org/",
                reply_markup=vip_menu()
            )

        elif text == "🚀 Sms Onay Siteleri 📩":
            bot.send_message(
                message.chat.id,
                "📱 5 Tane Sms Onay Sitesi\n\n"
                "● https://www.temp-phone-number.com/\n\n"
                "● https://tempsmss.com/\n\n"
                "● https://receive-smss.com/\n\n"
                "● https://temp-number.com/\n\n"
                "● https://online-sms.org/tr",
                reply_markup=vip_menu()
            )

        elif text == "📮 Anonim Mesaj Gönderme 📮":
            bot.send_message(message.chat.id, "Anonim Mesaj Gönderme bölümü açıldı.", reply_markup=vip_menu())

        elif text == "👨‍💻 REFERANS BOTU YAPMA 👾":
            bot.send_message(
                message.chat.id,
                "🔱 TIKLA 👉 https://seonlyhaber.blogspot.com/2022/08/telefon-ile-telegram-botu-yapma-2022.html?m=1",
                reply_markup=vip_menu()
            )

        elif text == "🌹 Bedava İzlenme Ve Tepki 🌹":
            bot.send_message(
                message.chat.id,
                "Ücretsiz Telegram Kanallarınıza Görüntülenme ve İfade gönderen bot\n\n"
                "LİNK = https://t.me/+Ltf05gYRRq8zNTdk",
                reply_markup=vip_menu()
            )

    else:
        bot.send_message(
            message.chat.id,
            "Bu buton için işlem tanımlı değil.",
            reply_markup=ana_menu()
        )


print("Bot çalışıyor...")
bot.infinity_polling()
