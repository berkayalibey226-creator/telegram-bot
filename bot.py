
import os
import json
import requests
from telegram import Update, ReplyKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "8542662196:AAFPxpjOZROlqeGvzdsjv8mRCeU6enLccFM"
START_IMAGE = "welcome.jpg"
API_URL = "https://finance.truncgil.com/api/gold-rates"

ADMIN_IDS = [5470933993]  # kendi Telegram sayısal ID'ni yaz
USERS_FILE = "users.json"
SETTINGS_FILE = "settings.json"
DEFAULT_START_BALANCE = 10
BOT_USERNAME = "W4NT_2D_bot"  # @ olmadan yaz
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
    settings = load_settings()
    return settings.get("vip_password", "1234")


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
    users = load_users()
    return users.get(str(user_id))


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
    new_refs = current_refs + int(amount)
    if new_refs < 0:
        new_refs = 0

    users[uid]["references"] = new_refs
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

    if inviter_id not in users:
        return False, None

    if inviter_id == new_user_id:
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


def kullanici_gosterimi(user) -> str:
    if user.username:
        return f"@{user.username}"
    if user.first_name:
        return user.first_name
    return "Kullanıcı"


async def dosya_gonder(update, path, caption=None, reply_markup=None):
    if os.path.exists(path):
        with open(path, "rb") as f:
            await update.message.reply_document(
                document=f,
                caption=caption,
                reply_markup=reply_markup
            )
    else:
        await update.message.reply_text(
            f"Dosya bulunamadı: {path}",
            reply_markup=reply_markup
        )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ensure_user_exists(update.effective_user)
    user = update.effective_user
    kullanici = kullanici_gosterimi(user)

    referral_added, inviter_id = process_referral(user, context.args)
    inviter_text = ""

    if referral_added and inviter_id:
        inviter_data = get_user_data(inviter_id)
        inviter_name = inviter_data.get("username", inviter_id) if inviter_data else inviter_id
        inviter_text = f"\n\n🎁 Bu kayıt bir referans üzerinden geldi.\nDavet eden: {inviter_name}"

    caption = (
        f"<b>W4NT2D BOTUNA HOŞ GELDİN</b>\n\n"
        f"{kullanici} gözümüz yolda kaldı 😁❤️"
        f"{inviter_text}"
    )

    if os.path.exists(START_IMAGE):
        with open(START_IMAGE, "rb") as photo:
            await update.message.reply_photo(
                photo=photo,
                caption=caption,
                parse_mode=ParseMode.HTML
            )
    else:
        await update.message.reply_text(
            caption,
            parse_mode=ParseMode.HTML
        )

    await update.message.reply_text(
        "Menü hazır 👇",
        reply_markup=ana_menu()
    )


async def mesaj_yakala(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

    if context.user_data.get("waiting_user_lookup"):
        if not is_admin(user.id):
            context.user_data["waiting_user_lookup"] = False
            await update.message.reply_text("Yetkin yok.", reply_markup=ana_menu())
            return

        hedef_id = text.strip()

        if not hedef_id.isdigit():
            await update.message.reply_text("Geçerli bir Telegram ID gönder.", reply_markup=admin_menu())
            return

        hedef = get_user_data(hedef_id)
        context.user_data["waiting_user_lookup"] = False

        if not hedef:
            await update.message.reply_text("Kullanıcı bulunamadı.", reply_markup=admin_menu())
            return

        mesaj = (
            "🔎 KULLANICI BİLGİSİ\n\n"
            f"Kullanıcı: {hedef.get('username', 'Yok')}\n"
            f"ID: {hedef.get('id')}\n"
            f"Ad: {hedef.get('first_name', '')} {hedef.get('last_name', '')}\n"
            f"Bakiye: {hedef.get('balance', 0)}\n"
            f"Referans: {hedef.get('references', 0)}\n"
            f"Kullanıcı Kodu: {hedef.get('user_code', '-')}\n"
            f"Davet Eden: {hedef.get('invited_by', '-')}"
        )
        await update.message.reply_text(mesaj, reply_markup=admin_menu())
        return

    if context.user_data.get("waiting_broadcast_message"):
        if not is_admin(user.id):
            context.user_data["waiting_broadcast_message"] = False
            await update.message.reply_text("Yetkin yok.", reply_markup=ana_menu())
            return

        broadcast_text = text
        users = load_users()
        sent_count = 0

        for uid in users.keys():
            try:
                await context.bot.send_message(
                    chat_id=int(uid),
                    text=f"📢 DUYURU\n\n{broadcast_text}"
                )
                sent_count += 1
            except Exception:
                pass

        context.user_data["waiting_broadcast_message"] = False
        await update.message.reply_text(
            f"✅ Toplu mesaj gönderildi.\nUlaşan kullanıcı sayısı: {sent_count}",
            reply_markup=admin_menu()
        )
        return

    if context.user_data.get("waiting_new_vip_password"):
        if not is_admin(user.id):
            context.user_data["waiting_new_vip_password"] = False
            await update.message.reply_text("Yetkin yok.", reply_markup=ana_menu())
            return

        yeni_sifre = text.strip()
        set_vip_password(yeni_sifre)
        context.user_data["waiting_new_vip_password"] = False

        await update.message.reply_text(
            f"✅ VIP şifre değiştirildi.\nYeni şifre: {yeni_sifre}",
            reply_markup=admin_menu()
        )
        return

    if context.user_data.get("waiting_admin_balance_target"):
        if not is_admin(user.id):
            context.user_data["waiting_admin_balance_target"] = False
            await update.message.reply_text("Yetkin yok.", reply_markup=ana_menu())
            return

        hedef_id = text.strip()

        if not hedef_id.isdigit():
            await update.message.reply_text("Geçerli bir Telegram ID gönder.", reply_markup=admin_menu())
            return

        hedef_user = get_user_data(hedef_id)
        if not hedef_user:
            context.user_data["waiting_admin_balance_target"] = False
            await update.message.reply_text(
                "Bu kullanıcı sistemde yok. Önce botu başlatmış olması gerekiyor.",
                reply_markup=admin_menu()
            )
            return

        context.user_data["admin_balance_target_id"] = hedef_id
        context.user_data["waiting_admin_balance_target"] = False
        context.user_data["waiting_admin_balance_amount"] = True

        await update.message.reply_text(
            f"Kullanıcı bulundu: {hedef_user.get('username', 'Yok')}\n"
            f"Mevcut bakiye: {hedef_user.get('balance', 0)}\n\n"
            "Şimdi eklenecek/çıkarılacak miktarı gönder.\n"
            "Örnek:\n"
            "50 -> 50 ekler\n"
            "-10 -> 10 düşer",
            reply_markup=admin_menu()
        )
        return

    if context.user_data.get("waiting_admin_balance_amount"):
        if not is_admin(user.id):
            context.user_data["waiting_admin_balance_amount"] = False
            await update.message.reply_text("Yetkin yok.", reply_markup=ana_menu())
            return

        try:
            miktar = int(text.strip())
        except ValueError:
            await update.message.reply_text(
                "Geçerli bir sayı gönder. Örnek: 50 veya -10",
                reply_markup=admin_menu()
            )
            return

        hedef_id = context.user_data.get("admin_balance_target_id")
        if not hedef_id:
            context.user_data["waiting_admin_balance_amount"] = False
            await update.message.reply_text(
                "Hedef kullanıcı bulunamadı. Baştan dene.",
                reply_markup=admin_menu()
            )
            return

        ok = update_user_balance(hedef_id, miktar)
        context.user_data["waiting_admin_balance_amount"] = False
        context.user_data["admin_balance_target_id"] = None

        if not ok:
            await update.message.reply_text("Bakiye güncellenemedi.", reply_markup=admin_menu())
            return

        yeni_veri = get_user_data(hedef_id)
        await update.message.reply_text(
            f"✅ Bakiye güncellendi.\n\n"
            f"Kullanıcı: {yeni_veri.get('username', 'Yok')}\n"
            f"ID: {yeni_veri.get('id')}\n"
            f"Yeni Bakiye: {yeni_veri.get('balance', 0)}",
            reply_markup=admin_menu()
        )
        return

    if context.user_data.get("waiting_admin_ref_target"):
        if not is_admin(user.id):
            context.user_data["waiting_admin_ref_target"] = False
            await update.message.reply_text("Yetkin yok.", reply_markup=ana_menu())
            return

        hedef_id = text.strip()

        if not hedef_id.isdigit():
            await update.message.reply_text("Geçerli bir Telegram ID gönder.", reply_markup=admin_menu())
            return

        hedef_user = get_user_data(hedef_id)
        if not hedef_user:
            context.user_data["waiting_admin_ref_target"] = False
            await update.message.reply_text(
                "Bu kullanıcı sistemde yok. Önce botu başlatmış olması gerekiyor.",
                reply_markup=admin_menu()
            )
            return

        context.user_data["admin_ref_target_id"] = hedef_id
        context.user_data["waiting_admin_ref_target"] = False
        context.user_data["waiting_admin_ref_amount"] = True

        await update.message.reply_text(
            f"Kullanıcı bulundu: {hedef_user.get('username', 'Yok')}\n"
            f"Mevcut referans: {hedef_user.get('references', 0)}\n\n"
            "Şimdi eklenecek/çıkarılacak referans miktarını gönder.\n"
            "Örnek:\n"
            "1 -> 1 ekler\n"
            "-1 -> 1 düşer",
            reply_markup=admin_menu()
        )
        return

    if context.user_data.get("waiting_admin_ref_amount"):
        if not is_admin(user.id):
            context.user_data["waiting_admin_ref_amount"] = False
            await update.message.reply_text("Yetkin yok.", reply_markup=ana_menu())
            return

        try:
            miktar = int(text.strip())
        except ValueError:
            await update.message.reply_text(
                "Geçerli bir sayı gönder. Örnek: 1 veya -1",
                reply_markup=admin_menu()
            )
            return

        hedef_id = context.user_data.get("admin_ref_target_id")
        if not hedef_id:
            context.user_data["waiting_admin_ref_amount"] = False
            await update.message.reply_text(
                "Hedef kullanıcı bulunamadı. Baştan dene.",
                reply_markup=admin_menu()
            )
            return

        ok = update_user_references(hedef_id, miktar)
        context.user_data["waiting_admin_ref_amount"] = False
        context.user_data["admin_ref_target_id"] = None

        if not ok:
            await update.message.reply_text("Referans güncellenemedi.", reply_markup=admin_menu())
            return

        yeni_veri = get_user_data(hedef_id)
        await update.message.reply_text(
            f"✅ Referans güncellendi.\n\n"
            f"Kullanıcı: {yeni_veri.get('username', 'Yok')}\n"
            f"ID: {yeni_veri.get('id')}\n"
            f"Yeni Referans: {yeni_veri.get('references', 0)}",
            reply_markup=admin_menu()
        )
        return

    if context.user_data.get("waiting_contact_message"):
        username = f"@{user.username}" if user.username else "Yok"
        telegram_id = user.id
        first_name = user.first_name or "Kullanıcı"
        last_name = user.last_name or ""
        full_name = f"{first_name} {last_name}".strip()

        kullanici_kodu = user_info.get("user_code", str(telegram_id))
        kullanici_mesaji = text

        admin_mesaj = (
            "📞 İ𝐋𝐄𝐓İŞİ𝐌 📮\n"
            f"Kullanıcı: {username}\n"
            f"#u{telegram_id} #answer\n"
            f"Kullanıcı Kodu / ID: {kullanici_kodu} / {telegram_id}\n"
            f"Referanslar: {user_info.get('references', 0)}\n"
            f"Bakiye: {user_info.get('balance', DEFAULT_START_BALANCE)}\n"
            f"Bot: @{BOT_USERNAME}\n"
            "📩 Soruya yeni cevap! 🔻\n\n"
            f"👤 Ad: {full_name}\n"
            f"💬 Mesaj: {kullanici_mesaji}"
        )

        for admin_id in ADMIN_IDS:
            try:
                await context.bot.send_message(chat_id=admin_id, text=admin_mesaj)
            except Exception as e:
                print(f"Admin mesajı gönderilemedi: {e}")

        context.user_data["waiting_contact_message"] = False

        await update.message.reply_text(
            "✅ Mesajınız yöneticilere iletildi.",
            reply_markup=ana_menu()
        )
        return

    if context.user_data.get("vip_waiting_password"):
        if text == get_vip_password():
            context.user_data["vip_waiting_password"] = False
            context.user_data["vip_unlocked"] = True
            await update.message.reply_text(
                "✅ Şifre doğru. VIP menü açıldı.",
                reply_markup=vip_menu()
            )
        else:
            await update.message.reply_text(
                f"❌ Şifre yanlış.\nDoğru şifre için: {OWNER_USERNAME}",
                reply_markup=ana_menu()
            )
        return

    if text in vip_buttons and not context.user_data.get("vip_unlocked"):
        await update.message.reply_text(
            f"🔐 Önce VIP şifresini girmen gerekiyor.\nŞifre için: {OWNER_USERNAME}",
            reply_markup=ana_menu()
        )
        return

    if text == "👾 HAKKIMDA💀":
        mesaj = (
            f"╰┈➤ Bu Bot {OWNER_USERNAME} Tarafından Yapılmıştır.\n"
            "İstek-Öneri-Şikayet İçin Bana Yazabilirsiniz."
        )
        await update.message.reply_text(mesaj, reply_markup=ana_menu())

    elif text == "💎 Vip Bölme 💎":
        context.user_data["vip_waiting_password"] = True
        await update.message.reply_text(
            f"🔐 VIP bölüme giriş için şifre gerekiyor.\n\n"
            f"Şifre almak için: {OWNER_USERNAME}\n"
            "Şifreyi aldıktan sonra buraya gönder.",
            reply_markup=ana_menu()
        )

    elif text == "🫣 BEYANNIM 🧑‍💼":
        mesaj = (
            "🚀 Aşağıdaki Linki Biyografinize Ekliyebilirsiniz 🚀\n"
            "https://telegra.ph/BEYANNIM-09-17"
        )
        await update.message.reply_text(mesaj, reply_markup=ana_menu())

    elif text == "📶 Bedava internet 💥":
        await update.message.reply_text("Bedava internet bölümü açıldı.", reply_markup=ana_menu())

    elif text == "🧑‍🏫 EĞİTİM SETLERİ 🧑‍🏫":
        await update.message.reply_text("📚 Eğitim Setleri Seç:", reply_markup=egitim_menu())

    elif text == "📸 Instagram İçin Eğitim Seti":
        await update.message.reply_text(
            "《İ𝐍𝐒𝐓𝐀𝐆𝐑𝐀𝐌 İÇİ𝐍 𝐄Ğİ𝐓İ𝐌 𝐒𝐄𝐓İ》",
            reply_markup=egitim_menu()
        )

    elif text == "🔥 Enes Turan Eğitim Seti":
        await update.message.reply_text(
            "📚 Enes Turan Eğitim Setleri:",
            reply_markup=enes_menu()
        )

    elif text == "⚡ Barış Reus Eğitim Seti":
        await update.message.reply_text(
            "📦 Barış Reus eğitim seti dosyaları gönderiliyor...",
            reply_markup=egitim_menu()
        )

        await dosya_gonder(
            update,
            "Barisreus_Egitim_Seti_V2.zip",
            caption="📁 Barış Reus Eğitim Seti V2",
            reply_markup=egitim_menu()
        )

        await dosya_gonder(
            update,
            "Barisreus Egitim Seti V3.zip",
            caption="📁 Barış Reus Eğitim Seti V3",
            reply_markup=egitim_menu()
        )

        await dosya_gonder(
            update,
            "Barisreus_arsiv.zip",
            caption="📁 Barış Reus Arşiv",
            reply_markup=egitim_menu()
        )

    elif text == "🔙 Geri":
        await update.message.reply_text("📚 Eğitim Setleri Seç:", reply_markup=egitim_menu())

    elif text.startswith("Enes Turan Eğitim Seti V"):
        await update.message.reply_text(
            f"{text} açıldı 📚",
            reply_markup=enes_menu()
        )

    elif text == "Referans 👥":
        ref_link = get_ref_link(user.id)
        mesaj = (
            "👥 REFERANS SİSTEMİ\n\n"
            f"Kullanıcı: {user_info.get('username', 'Yok')}\n"
            f"ID: {user_info.get('id')}\n"
            f"Referans Sayısı: {user_info.get('references', 0)}\n\n"
            "🔗 Özel Davet Linkin:\n"
            f"{ref_link}\n\n"
            "Bu link ile gelen ve botu ilk kez başlatan her kullanıcı, referansına eklenir."
        )
        await update.message.reply_text(mesaj, reply_markup=ana_menu())

    elif text == "Bakiye 💰":
        mesaj = (
            "💰 BAKİYE BİLGİNİZ\n\n"
            f"Kullanıcı: {user_info.get('username', 'Yok')}\n"
            f"ID: {user_info.get('id')}\n"
            f"Referanslar: {user_info.get('references', 0)}\n"
            f"Bakiye: {user_info.get('balance', DEFAULT_START_BALANCE)}"
        )
        await update.message.reply_text(mesaj, reply_markup=ana_menu())

    elif text == "📞 İLETİŞİM 📮":
        context.user_data["waiting_contact_message"] = True
        await update.message.reply_text(
            "Mesajınızı yazın 24 saat içersinde dönüş yapılacaktır.",
            reply_markup=ana_menu()
        )

    elif text == "🎛 Buton Düzenleyici":
        await update.message.reply_text("Buton Düzenleyici açıldı.", reply_markup=ana_menu())

    elif text == "📝 Gönderi Düzenleyici":
        await update.message.reply_text("Gönderi Düzenleyici açıldı.", reply_markup=ana_menu())

    elif text == "🔐 Admin":
        if not is_admin(user.id):
            await update.message.reply_text(
                "Bu bölüm sadece yöneticilere açıktır.",
                reply_markup=ana_menu()
            )
            return

        users = load_users()
        toplam_kullanici = len(users)

        await update.message.reply_text(
            f"🔐 Admin Paneli\n\n"
            f"Toplam kullanıcı: {toplam_kullanici}\n"
            f"Bot: @{BOT_USERNAME}\n\n"
            "Aşağıdan bir işlem seç.",
            reply_markup=admin_menu()
        )

    elif text == "👥 Kullanıcı Sayısı":
        if not is_admin(user.id):
            await update.message.reply_text("Yetkin yok.", reply_markup=ana_menu())
            return

        users = load_users()
        await update.message.reply_text(
            f"👥 Toplam kullanıcı sayısı: {len(users)}",
            reply_markup=admin_menu()
        )

    elif text == "📊 İstatistikler":
        if not is_admin(user.id):
            await update.message.reply_text("Yetkin yok.", reply_markup=ana_menu())
            return

        users = load_users()
        toplam_kullanici = len(users)
        toplam_bakiye = sum(int(v.get("balance", 0)) for v in users.values())
        toplam_referans = sum(int(v.get("references", 0)) for v in users.values())
        referansla_gelen = sum(1 for v in users.values() if v.get("joined_from_ref"))

        mesaj = (
            "📊 BOT İSTATİSTİKLERİ\n\n"
            f"Toplam Kullanıcı: {toplam_kullanici}\n"
            f"Toplam Bakiye: {toplam_bakiye}\n"
            f"Toplam Referans: {toplam_referans}\n"
            f"Referansla Gelen Kullanıcı: {referansla_gelen}"
        )
        await update.message.reply_text(mesaj, reply_markup=admin_menu())

    elif text == "💰 Bakiye Düzenle":
        if not is_admin(user.id):
            await update.message.reply_text("Yetkin yok.", reply_markup=ana_menu())
            return

        context.user_data["waiting_admin_balance_target"] = True
        await update.message.reply_text(
            "Bakiyesini düzenlemek istediğin kullanıcının Telegram ID'sini gönder.",
            reply_markup=admin_menu()
        )

    elif text == "👥 Referans Düzenle":
        if not is_admin(user.id):
            await update.message.reply_text("Yetkin yok.", reply_markup=ana_menu())
            return

        context.user_data["waiting_admin_ref_target"] = True
        await update.message.reply_text(
            "Referansını düzenlemek istediğin kullanıcının Telegram ID'sini gönder.",
            reply_markup=admin_menu()
        )

    elif text == "🔎 Kullanıcı Sorgula":
        if not is_admin(user.id):
            await update.message.reply_text("Yetkin yok.", reply_markup=ana_menu())
            return

        context.user_data["waiting_user_lookup"] = True
        await update.message.reply_text(
            "Bilgilerini görmek istediğin kullanıcının Telegram ID'sini gönder.",
            reply_markup=admin_menu()
        )

    elif text == "📩 Toplu Mesaj":
        if not is_admin(user.id):
            await update.message.reply_text("Yetkin yok.", reply_markup=ana_menu())
            return

        context.user_data["waiting_broadcast_message"] = True
        await update.message.reply_text(
            "Tüm kullanıcılara gönderilecek mesajı yaz.",
            reply_markup=admin_menu()
        )

    elif text == "🔐 VIP Şifre Değiştir":
        if not is_admin(user.id):
            await update.message.reply_text("Yetkin yok.", reply_markup=ana_menu())
            return

        context.user_data["waiting_new_vip_password"] = True
        await update.message.reply_text(
            "Yeni VIP şifresini gönder.",
            reply_markup=admin_menu()
        )

    elif text == "📬 Gelen Mesajlar":
        if not is_admin(user.id):
            await update.message.reply_text("Yetkin yok.", reply_markup=ana_menu())
            return

        await update.message.reply_text(
            "Kullanıcılardan gelen mesajlar doğrudan admin hesabına iletiliyor.",
            reply_markup=admin_menu()
        )

    elif text == "😈 Instagram Canlı Kapatma 🚷":
        await update.message.reply_text(
            "Bu bölüm şu an aktif değil.",
            reply_markup=vip_menu()
        )

    elif text == "🔇 INSTAGRAM BANNED":
        mesaj = (
            "📌 Instagram hesabın kapandıysa:\n\n"
            "• Giriş ekranından itiraz et\n"
            "• Kimlik doğrulama isteğini tamamla\n"
            "• Resmi destek formunu kullan"
        )
        await update.message.reply_text(mesaj, reply_markup=vip_menu())

    elif text == "🛄 GMAIL ONAY SİTELERİ 📥":
        mesaj = (
            "📧 4 Tane Gmail Onay Sitesi\n\n"
            "● https://tempail.com/\n\n"
            "● https://www.fakemail.net/\n\n"
            "● https://mail.tm/en/\n\n"
            "● https://temp-mail.org/\n\n"
            f"🔱 {OWNER_USERNAME} 🔱"
        )
        await update.message.reply_text(mesaj, reply_markup=vip_menu())

    elif text == "🚀 Sms Onay Siteleri 📩":
        mesaj = (
            "📱 5 Tane SMS Onay Sitesi\n\n"
            "● https://www.temp-phone-number.com/\n\n"
            "● https://tempsmss.com/\n\n"
            "● https://receive-smss.com/\n\n"
            "● https://temp-number.com/\n\n"
            "● https://online-sms.org/tr\n\n"
            f"🔱 {OWNER_USERNAME} 🔱"
        )
        await update.message.reply_text(mesaj, reply_markup=vip_menu())

    elif text == "📮 Anonim Mesaj Gönderme 📮":
        await update.message.reply_text(
            "Bu bölüm şu an aktif değil.",
            reply_markup=vip_menu()
        )

    elif text == "👨‍💻 REFERANS BOTU YAPMA 👾":
        mesaj = "🔱 TIKLA 👉 https://seonlyhaber.blogspot.com/2022/08/telefon-ile-telegram-botu-yapma-2022.html?m=1"
        await update.message.reply_text(mesaj, reply_markup=vip_menu())

    elif text == "🌹 Bedava İzlenme Ve Tepki 🌹":
        mesaj = (
            "Ücretsiz Telegram Kanallarınıza Görüntülenme ve İfade "
            "(Kalp, Beğeni vb.) gönderen bot\n\n"
            "İlk başta bonus olarak 300 görüntülenme veriyor.\n"
            "Referans yaparak kişi başı 300 görüntülenme alabilirsiniz.\n\n"
            "Görüntülenme atabilmeniz için size bir kanala katılmanız gerektiğini söyleyebilir. "
            "Oraya katılıp tekrar deneyin.\n\n"
            "LİNK = https://t.me/+Ltf05gYRRq8zNTdk\n\n"
            f"🔱 {OWNER_USERNAME} 🔱"
        )
        await update.message.reply_text(mesaj, reply_markup=vip_menu())

    elif text == "🟡 Altın Fiyatları 💰":
        try:
            gram, ceyrek, update_date = altin_fiyat_al()
            mesaj = (
                "🟡 Güncel Altın Fiyatları\n\n"
                "Gram Altın\n"
                f"Alış: {gram.get('Buying', '-')}\n"
                f"Satış: {gram.get('Selling', '-')}\n\n"
                "Çeyrek Altın\n"
                f"Alış: {ceyrek.get('Buying', '-')}\n"
                f"Satış: {ceyrek.get('Selling', '-')}\n\n"
                f"Güncelleme: {update_date}"
            )
            await update.message.reply_text(mesaj, reply_markup=ana_menu())
        except Exception as e:
            await update.message.reply_text(
                f"Fiyatlar alınırken hata oluştu: {e}",
                reply_markup=ana_menu()
            )

    else:
        await update.message.reply_text("Bu buton tanımlı değil.", reply_markup=ana_menu())


def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mesaj_yakala))

    print("Bot çalışıyor...")
    app.run_polling()


if __name__ == "__main__":
    main()
