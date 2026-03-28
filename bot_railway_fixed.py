import os
import json
import requests
from telegram import Update, ReplyKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

TOKEN = os.getenv("TOKEN", "BURAYA_BOT_TOKENINI_YAPISTIR")
START_IMAGE = "welcome.jpg"
API_URL = "https://finance.truncgil.com/api/gold-rates"

ADMIN_IDS = [5470933993]
USERS_FILE = "users.json"
SETTINGS_FILE = "settings.json"
DEFAULT_START_BALANCE = 10
BOT_USERNAME = "W4NT_2D_bot"
OWNER_USERNAME = "@MTX_GLOBAL_TR"


def load_users():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)


def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"vip_password": "1234"}
    return {"vip_password": "1234"}


def save_settings(settings):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)


def get_vip_password():
    return load_settings().get("vip_password", "1234")


def set_vip_password(new_password):
    settings = load_settings()
    settings["vip_password"] = new_password
    save_settings(settings)


def ensure_user_exists(user):
    users = load_users()
    user_id = str(user.id)

    if user_id not in users:
        users[user_id] = {
            "id": user.id,
            "username": f"@{user.username}" if user.username else "Yok",
            "first_name": user.first_name or "",
            "last_name": user.last_name or "",
            "balance": DEFAULT_START_BALANCE,
            "references": 0,
            "user_code": str(user.id),
            "invited_by": None,
            "joined_from_ref": False
        }
    else:
        users[user_id]["username"] = f"@{user.username}" if user.username else "Yok"
        users[user_id]["first_name"] = user.first_name or ""
        users[user_id]["last_name"] = user.last_name or ""

    save_users(users)
    return users[user_id]


def get_user_data(user_id):
    return load_users().get(str(user_id))


def update_user_balance(user_id, amount):
    users = load_users()
    uid = str(user_id)
    if uid not in users:
        return False
    users[uid]["balance"] = int(users[uid].get("balance", 0)) + int(amount)
    save_users(users)
    return True


def update_user_references(user_id, amount):
    users = load_users()
    uid = str(user_id)
    if uid not in users:
        return False
    current_refs = int(users[uid].get("references", 0))
    users[uid]["references"] = max(0, current_refs + int(amount))
    save_users(users)
    return True


def is_admin(user_id):
    return user_id in ADMIN_IDS


def get_ref_link(user_id):
    return f"https://t.me/{BOT_USERNAME}?start=ref_{user_id}"


def process_referral(new_user, start_args):
    if not start_args:
        return False, None

    payload = start_args[0].strip()
    if not payload.startswith("ref_"):
        return False, None

    inviter_id = payload.replace("ref_", "").strip()
    if not inviter_id.isdigit():
        return False, None

    inviter_id = str(inviter_id)
    new_user_id = str(new_user.id)
    users = load_users()

    if new_user_id not in users:
        ensure_user_exists(new_user)
        users = load_users()

    if inviter_id not in users or inviter_id == new_user_id:
        return False, None

    if users[new_user_id].get("joined_from_ref"):
        return False, inviter_id

    users[inviter_id]["references"] = int(users[inviter_id].get("references", 0)) + 1
    users[new_user_id]["invited_by"] = inviter_id
    users[new_user_id]["joined_from_ref"] = True
    save_users(users)
    return True, inviter_id


def ana_menu():
    keyboard = [
        ["👾 HAKKIMDA💀"],
        ["💎 Vip Bölme 💎"],
        ["🫣 BEYANNIM 🧑‍💼", "📶 Bedava internet 💥"],
        ["🧑‍🏫 EĞİTİM SETLERİ 🧑‍🏫"],
        ["Referans 👥", "Bakiye 💰"],
        ["📞 İLETİŞİM 📮"],
        ["🎛 Buton Düzenleyici", "📝 Gönderi Düzenleyici"],
        ["🔐 Admin"],
        ["🟡 Altın Fiyatları 💰"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def vip_menu():
    keyboard = [
        ["😈 Instagram Canlı Kapatma 🚷"],
        ["🔇 INSTAGRAM BANNED"],
        ["🛄 GMAIL ONAY SİTELERİ 📥"],
        ["🚀 Sms Onay Siteleri 📩"],
        ["📮 Anonim Mesaj Gönderme 📮"],
        ["👨‍💻 REFERANS BOTU YAPMA 👾"],
        ["🌹 Bedava İzlenme Ve Tepki 🌹"],
        ["🔙 Ana Menü"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def egitim_menu():
    keyboard = [
        ["📸 Instagram İçin Eğitim Seti"],
        ["🔥 Enes Turan Eğitim Seti"],
        ["⚡ Barış Reus Eğitim Seti"],
        ["🔙 Ana Menü"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def enes_menu():
    keyboard = [
        ["Enes Turan Eğitim Seti V1 📚", "Enes Turan Eğitim Seti V2 📚"],
        ["Enes Turan Eğitim Seti V3 📚", "Enes Turan Eğitim Seti V4 📚"],
        ["Enes Turan Eğitim Seti V5 📚", "Enes Turan Eğitim Seti V6 📚"],
        ["Enes Turan Eğitim Seti V7 📚", "Enes Turan Eğitim Seti V8 📚"],
        ["Enes Turan Eğitim Seti V9 📚", "Enes Turan Eğitim Seti V10 📚"],
        ["Enes Turan Eğitim Seti V11 📚", "Enes Turan Eğitim Seti V12 📚"],
        ["Enes Turan Eğitim Seti V13 📚"],
        ["🔙 Geri"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def admin_menu():
    keyboard = [
        ["👥 Kullanıcı Sayısı", "📊 İstatistikler"],
        ["💰 Bakiye Düzenle", "👥 Referans Düzenle"],
        ["🔎 Kullanıcı Sorgula", "📩 Toplu Mesaj"],
        ["🔐 VIP Şifre Değiştir", "📬 Gelen Mesajlar"],
        ["🔙 Ana Menü"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def altin_fiyat_al():
    r = requests.get(API_URL, timeout=10)
    r.raise_for_status()
    data = r.json()
    rates = data.get("Rates", {})
    gram = rates.get("GRA")
    ceyrek = rates.get("CEYREKALTIN")
    update_date = data.get("Meta_Data", {}).get("Update_Date", "-")
    if not gram or not ceyrek:
        raise ValueError("Gram veya çeyrek altın verisi bulunamadı.")
    return gram, ceyrek, update_date


def kullanici_gosterimi(user):
    if user.username:
        return f"@{user.username}"
    if user.first_name:
        return user.first_name
    return "Kullanıcı"


def dosya_gonder(update, path, caption=None, reply_markup=None):
    if os.path.exists(path):
        with open(path, "rb") as f:
            update.message.reply_document(document=f, caption=caption, reply_markup=reply_markup)
    else:
        update.message.reply_text(f"Dosya bulunamadı: {path}", reply_markup=reply_markup)


def start(update: Update, context: CallbackContext):
    ensure_user_exists(update.effective_user)
    user = update.effective_user
    kullanici = kullanici_gosterimi(user)

    referral_added, inviter_id = process_referral(user, context.args)
    inviter_text = ""
    if referral_added and inviter_id:
        inviter_data = get_user_data(inviter_id)
        inviter_name = inviter_data.get("username", inviter_id) if inviter_data else inviter_id
        inviter_text = f"\n\n🎁 Bu kayıt bir referans üzerinden geldi.\nDavet eden: {inviter_name}"

    caption = f"<b>W4NT2D BOTUNA HOŞ GELDİN</b>\n\n{kullanici} gözümüz yolda kaldı 😁❤️{inviter_text}"

    if os.path.exists(START_IMAGE):
        with open(START_IMAGE, "rb") as photo:
            update.message.reply_photo(photo=photo, caption=caption, parse_mode=ParseMode.HTML)
    else:
        update.message.reply_text(caption, parse_mode=ParseMode.HTML)

    update.message.reply_text("Menü hazır 👇", reply_markup=ana_menu())


def mesaj_yakala(update: Update, context: CallbackContext):
    text = update.message.text
    user = update.effective_user
    user_info = ensure_user_exists(user)

    vip_buttons = [
        "😈 Instagram Canlı Kapatma 🚷",
        "🔇 INSTAGRAM BANNED",
        "🛄 GMAIL ONAY SİTELERİ 📥",
        "🚀 Sms Onay Siteleri 📩",
        "📮 Anonim Mesaj Gönderme 📮",
        "👨‍💻 REFERANS BOTU YAPMA 👾",
        "🌹 Bedava İzlenme Ve Tepki 🌹",
    ]

    if context.user_data.get("waiting_contact_message"):
        username = f"@{user.username}" if user.username else "Yok"
        telegram_id = user.id
        full_name = f"{user.first_name or 'Kullanıcı'} {user.last_name or ''}".strip()
        admin_mesaj = (
            "📞 İLETİŞİM 📮\n"
            f"Kullanıcı: {username}\n"
            f"#u{telegram_id} #answer\n"
            f"Kullanıcı Kodu / ID: {user_info.get('user_code', telegram_id)} / {telegram_id}\n"
            f"Referanslar: {user_info.get('references', 0)}\n"
            f"Bakiye: {user_info.get('balance', DEFAULT_START_BALANCE)}\n"
            f"Bot: @{BOT_USERNAME}\n"
            "📩 Soruya yeni cevap! 🔻\n\n"
            f"👤 Ad: {full_name}\n"
            f"💬 Mesaj: {text}"
        )
        for admin_id in ADMIN_IDS:
            try:
                context.bot.send_message(chat_id=admin_id, text=admin_mesaj)
            except Exception:
                pass
        context.user_data["waiting_contact_message"] = False
        update.message.reply_text("✅ Mesajınız yöneticilere iletildi.", reply_markup=ana_menu())
        return

    if context.user_data.get("vip_waiting_password"):
        if text == get_vip_password():
            context.user_data["vip_waiting_password"] = False
            context.user_data["vip_unlocked"] = True
            update.message.reply_text("✅ Şifre doğru. VIP menü açıldı.", reply_markup=vip_menu())
        else:
            update.message.reply_text(f"❌ Şifre yanlış.\nDoğru şifre için: {OWNER_USERNAME}", reply_markup=ana_menu())
        return

    if text in vip_buttons and not context.user_data.get("vip_unlocked"):
        update.message.reply_text(
            f"🔐 Önce VIP şifresini girmen gerekiyor.\nŞifre için: {OWNER_USERNAME}",
            reply_markup=ana_menu()
        )
        return

    if text == "👾 HAKKIMDA💀":
        update.message.reply_text(
            f"╰┈➤ Bu Bot {OWNER_USERNAME} Tarafından Yapılmıştır.\nİstek-Öneri-Şikayet İçin Bana Yazabilirsiniz.",
            reply_markup=ana_menu()
        )

    elif text == "💎 Vip Bölme 💎":
        context.user_data["vip_waiting_password"] = True
        update.message.reply_text(
            f"🔐 VIP bölüme giriş için şifre gerekiyor.\n\nŞifre almak için: {OWNER_USERNAME}\nŞifreyi aldıktan sonra buraya gönder.",
            reply_markup=ana_menu()
        )

    elif text == "🫣 BEYANNIM 🧑‍💼":
        update.message.reply_text(
            "🚀 Aşağıdaki Linki Biyografinize Ekliyebilirsiniz 🚀\nhttps://telegra.ph/BEYANNIM-09-17",
            reply_markup=ana_menu()
        )

    elif text == "📶 Bedava internet 💥":
        update.message.reply_text("Bedava internet bölümü açıldı.", reply_markup=ana_menu())

    elif text == "🧑‍🏫 EĞİTİM SETLERİ 🧑‍🏫":
        update.message.reply_text("📚 Eğitim Setleri Seç:", reply_markup=egitim_menu())

    elif text == "📸 Instagram İçin Eğitim Seti":
        update.message.reply_text("《İ𝐍𝐒𝐓𝐀𝐆𝐑𝐀𝐌 İÇİ𝐍 𝐄Ğİ𝐓İ𝐌 𝐒𝐄𝐓İ》", reply_markup=egitim_menu())

    elif text == "🔥 Enes Turan Eğitim Seti":
        update.message.reply_text("📚 Enes Turan Eğitim Setleri:", reply_markup=enes_menu())

    elif text == "⚡ Barış Reus Eğitim Seti":
        update.message.reply_text("📦 Barış Reus eğitim seti dosyaları gönderiliyor...", reply_markup=egitim_menu())
        dosya_gonder(update, "Barisreus_Egitim_Seti_V2.zip", caption="📁 Barış Reus Eğitim Seti V2", reply_markup=egitim_menu())
        dosya_gonder(update, "Barisreus Egitim Seti V3.zip", caption="📁 Barış Reus Eğitim Seti V3", reply_markup=egitim_menu())
        dosya_gonder(update, "Barisreus_arsiv.zip", caption="📁 Barış Reus Arşiv", reply_markup=egitim_menu())

    elif text == "🔙 Geri":
        update.message.reply_text("📚 Eğitim Setleri Seç:", reply_markup=egitim_menu())

    elif text.startswith("Enes Turan Eğitim Seti V"):
        update.message.reply_text(f"{text} açıldı 📚", reply_markup=enes_menu())

    elif text == "Referans 👥":
        ref_link = get_ref_link(user.id)
        update.message.reply_text(
            "👥 REFERANS SİSTEMİ\n\n"
            f"Kullanıcı: {user_info.get('username', 'Yok')}\n"
            f"ID: {user_info.get('id')}\n"
            f"Referans Sayısı: {user_info.get('references', 0)}\n\n"
            f"🔗 Özel Davet Linkin:\n{ref_link}\n\n"
            "Bu link ile gelen ve botu ilk kez başlatan her kullanıcı, referansına eklenir.",
            reply_markup=ana_menu()
        )

    elif text == "Bakiye 💰":
        update.message.reply_text(
            "💰 BAKİYE BİLGİNİZ\n\n"
            f"Kullanıcı: {user_info.get('username', 'Yok')}\n"
            f"ID: {user_info.get('id')}\n"
            f"Referanslar: {user_info.get('references', 0)}\n"
            f"Bakiye: {user_info.get('balance', DEFAULT_START_BALANCE)}",
            reply_markup=ana_menu()
        )

    elif text == "📞 İLETİŞİM 📮":
        context.user_data["waiting_contact_message"] = True
        update.message.reply_text("Mesajınızı yazın 24 saat içersinde dönüş yapılacaktır.", reply_markup=ana_menu())

    elif text == "🎛 Buton Düzenleyici":
        update.message.reply_text("Buton Düzenleyici açıldı.", reply_markup=ana_menu())

    elif text == "📝 Gönderi Düzenleyici":
        update.message.reply_text("Gönderi Düzenleyici açıldı.", reply_markup=ana_menu())

    elif text == "🔐 Admin":
        if not is_admin(user.id):
            update.message.reply_text("Bu bölüm sadece yöneticilere açıktır.", reply_markup=ana_menu())
            return
        update.message.reply_text(
            f"🔐 Admin Paneli\n\nToplam kullanıcı: {len(load_users())}\nBot: @{BOT_USERNAME}\n\nAşağıdan bir işlem seç.",
            reply_markup=admin_menu()
        )

    elif text == "👥 Kullanıcı Sayısı":
        update.message.reply_text(f"👥 Toplam kullanıcı sayısı: {len(load_users())}", reply_markup=admin_menu())

    elif text == "📊 İstatistikler":
        users = load_users()
        update.message.reply_text(
            "📊 BOT İSTATİSTİKLERİ\n\n"
            f"Toplam Kullanıcı: {len(users)}\n"
            f"Toplam Bakiye: {sum(int(v.get('balance', 0)) for v in users.values())}\n"
            f"Toplam Referans: {sum(int(v.get('references', 0)) for v in users.values())}\n"
            f"Referansla Gelen Kullanıcı: {sum(1 for v in users.values() if v.get('joined_from_ref'))}",
            reply_markup=admin_menu()
        )

    elif text == "😈 Instagram Canlı Kapatma 🚷":
        update.message.reply_text("Bu bölüm şu an aktif değil.", reply_markup=vip_menu())

    elif text == "🔇 INSTAGRAM BANNED":
        update.message.reply_text(
            "📌 Instagram hesabın kapandıysa:\n\n• Giriş ekranından itiraz et\n• Kimlik doğrulama isteğini tamamla\n• Resmi destek formunu kullan",
            reply_markup=vip_menu()
        )

    elif text == "🛄 GMAIL ONAY SİTELERİ 📥":
        update.message.reply_text(
            "📧 4 Tane Gmail Onay Sitesi\n\n● https://tempail.com/\n\n● https://www.fakemail.net/\n\n● https://mail.tm/en/\n\n● https://temp-mail.org/\n\n"
            f"🔱 {OWNER_USERNAME} 🔱",
            reply_markup=vip_menu()
        )

    elif text == "🚀 Sms Onay Siteleri 📩":
        update.message.reply_text(
            "📱 5 Tane SMS Onay Sitesi\n\n● https://www.temp-phone-number.com/\n\n● https://tempsmss.com/\n\n● https://receive-smss.com/\n\n● https://temp-number.com/\n\n● https://online-sms.org/tr\n\n"
            f"🔱 {OWNER_USERNAME} 🔱",
            reply_markup=vip_menu()
        )

    elif text == "📮 Anonim Mesaj Gönderme 📮":
        update.message.reply_text("Bu bölüm şu an aktif değil.", reply_markup=vip_menu())

    elif text == "👨‍💻 REFERANS BOTU YAPMA 👾":
        update.message.reply_text(
            "🔱 TIKLA 👉 https://seonlyhaber.blogspot.com/2022/08/telefon-ile-telegram-botu-yapma-2022.html?m=1",
            reply_markup=vip_menu()
        )

    elif text == "🌹 Bedava İzlenme Ve Tepki 🌹":
        update.message.reply_text(
            "Ücretsiz Telegram Kanallarınıza Görüntülenme ve İfade (Kalp, Beğeni vb.) gönderen bot\n\n"
            "İlk başta bonus olarak 300 görüntülenme veriyor.\n"
            "Referans yaparak kişi başı 300 görüntülenme alabilirsiniz.\n\n"
            "Görüntülenme atabilmeniz için size bir kanala katılmanız gerektiğini söyleyebilir. Oraya katılıp tekrar deneyin.\n\n"
            "LİNK = https://t.me/+Ltf05gYRRq8zNTdk\n\n"
            f"🔱 {OWNER_USERNAME} 🔱",
            reply_markup=vip_menu()
        )

    elif text == "🟡 Altın Fiyatları 💰":
        try:
            gram, ceyrek, update_date = altin_fiyat_al()
            update.message.reply_text(
                "🟡 Güncel Altın Fiyatları\n\n"
                f"Gram Altın\nAlış: {gram.get('Buying', '-')}\nSatış: {gram.get('Selling', '-')}\n\n"
                f"Çeyrek Altın\nAlış: {ceyrek.get('Buying', '-')}\nSatış: {ceyrek.get('Selling', '-')}\n\n"
                f"Güncelleme: {update_date}",
                reply_markup=ana_menu()
            )
        except Exception as e:
            update.message.reply_text(f"Fiyatlar alınırken hata oluştu: {e}", reply_markup=ana_menu())

    else:
        update.message.reply_text("Bu buton tanımlı değil.", reply_markup=ana_menu())


def main():
    if not TOKEN or TOKEN == "BURAYA_BOT_TOKENINI_YAPISTIR":
        raise RuntimeError("TOKEN ayarlanmadı.")
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start, pass_args=True))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, mesaj_yakala))
    print("Bot calisiyor...")
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
