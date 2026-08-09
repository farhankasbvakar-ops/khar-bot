import time

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

from config import BOT_TOKEN
from database import (
    init_db,
    get_user,
    get_group,
    update_user,
    add_group_money
)

from economy import (
    calculate_level,
    level_progress,
    aar_reward,
    transfer_allowed
)

from pets import (
    find_carrot,
    carrot_value,
    pet_income,
    pet_upgrade_cost,
    rename_cost
)

from games import (
    smuggle,
    rescue
)

from city import (
    rescue_cost,
    jail_job_income
)

from admin import admin_panel


# =========================
# START
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    get_user(
        user.id,
        user.first_name
    )

    keyboard = [
        [
            InlineKeyboardButton(
                "🫏 کره خر",
                callback_data="pet"
            ),
            InlineKeyboardButton(
                "🪙 کیف پول",
                callback_data="wallet"
            )
        ],
        [
            InlineKeyboardButton(
                "🥕 بازی هویج",
                callback_data="carrot"
            )
        ],
        [
            InlineKeyboardButton(
                "📖 راهنما",
                callback_data="help"
            )
        ]
    ]

    await update.message.reply_text(
        "🫏 به خر بات خوش آمدی!\n\n"
        "ربات را می‌توانی به گروهت اضافه کنی "
        "و امکانات بازی را آنجا فعال کنی.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# =========================
# PROFILE
# =========================

async def profile(update, user_id):

    user = get_user(user_id)

    if user["profile_private"]:

        await update.message.reply_text(
            "🔒 این بازیکن پروفایلش را بسته است."
        )

        return

    level = calculate_level(
        user["total_aar"]
    )

    _, current, needed = level_progress(
        user["total_aar"]
    )

    text = (
        f"🫏 پروفایل {user['name']}\n\n"

        f"⭐ سطح {level}: "
        f"{current}/{needed}\n\n"

        f"🫏 عرهای گفته‌شده: "
        f"{user['total_aar']}\n"

        f"🪙 عر کوین: "
        f"{user['coins']}\n\n"

        f"💼 شغل: "
        f"{user['job']}\n"

        f"🫏 کره خر: "
        f"{user['pet_name']}\n"

        f"⭐ سطح کره خر: "
        f"{user['pet_level']}\n"

        f"🪝 سطح قلاب: "
        f"{user['hook_level']}"
    )

    await update.message.reply_text(text)


# =========================
# AAR
# =========================

async def aar(update, context):

    user = update.effective_user

    data = get_user(
        user.id,
        user.first_name
    )

    now = int(time.time())

    last = data["jail_until"]

    if last > now:

        remaining = last - now

        await update.message.reply_text(
            f"🏚️ هنوز در زندان خرهای بی‌ادبی!\n"
            f"⏱️ {remaining // 60} دقیقه دیگر."
        )

        return

    level = calculate_level(
        data["total_aar"]
    )

    reward = aar_reward(level)

    total = data["total_aar"] + 1

    new_level = calculate_level(total)

    update_user(
        user.id,
        coins=data["coins"] + reward,
        total_aar=total,
        level=new_level
    )

    if update.effective_chat.type != "private":

        group = get_group(
            update.effective_chat.id
        )

        total_group_aar = (
            group["total_aar"] + 1
        )

        from database import db

        db.execute(
            """
            UPDATE groups
            SET total_aar=?
            WHERE chat_id=?
            """,
            (
                total_group_aar,
                update.effective_chat.id
            )
        )

        db.commit()

        if total_group_aar % 50 == 0:

            await update.message.reply_text(
                "🚨 رویداد ویژه!\n\n"
                "🫏 یک کره خر خیابانی گرفتار شده!\n"
                "🏃 فقط ۳ تلاش برای کل گروه وجود دارد.\n\n"
                "برای نجاتش بنویس:\n"
                "نجات کره خر"
            )

    await update.message.reply_text(
        f"🫏 عررررر!\n\n"
        f"🪙 +{reward} عر کوین\n"
        f"⭐ سطح: {new_level}\n"
        f"📊 عرها: {total}"
    )


# =========================
# CARROT
# =========================

async def carrot(update, context):

    user = update.effective_user

    data = get_user(user.id)

    result = find_carrot(
        data["hook_level"]
    )

    column = {
        "معمولی": "normal_carrot",
        "بزرگ": "big_carrot",
        "طلایی": "gold_carrot",
        "افسانه‌ای": "legendary_carrot"
    }[result]

    count = data[column]

    update_user(
        user.id,
        **{
            column: count + 1
        }
    )

    await update.message.reply_text(
        f"🥕 هویج پیدا کردی!\n\n"
        f"نوع: {result}\n"
        f"🍽️ ارزش غذایی: "
        f"{carrot_value(result)}"
    )


# =========================
# PET PANEL
# =========================

async def pet(update, context):

    user = update.effective_user

    data = get_user(user.id)

    keyboard = [
        [
            InlineKeyboardButton(
                "🥕 هویج‌ها",
                callback_data="carrots"
            )
        ],
        [
            InlineKeyboardButton(
                "🍽️ غذا دادن",
                callback_data="feed"
            )
        ],
        [
            InlineKeyboardButton(
                "📈 ارتقا",
                callback_data="upgrade_pet"
            )
        ],
        [
            InlineKeyboardButton(
                "💰 درآمد",
                callback_data="pet_income"
            )
        ]
    ]

    await update.message.reply_text(
        f"🫏 {data['pet_name']}\n\n"
        f"⭐ سطح: {data['pet_level']}\n"
        f"🥕 غذا: {data['pet_food']}/8\n"
        f"🪙 تولید ساعتی: "
        f"{pet_income(data['pet_level'], data['pet_food'])}",
        reply_markup=InlineKeyboardMarkup(
            keyboard
        )
    )


# =========================
# WALLET
# =========================

async def wallet(update, context):

    data = get_user(
        update.effective_user.id
    )

    await update.message.reply_text(
        f"🪙 کیف پول\n\n"
        f"موجودی: {data['coins']} عر کوین"
    )


# =========================
# SMUGGLE
# =========================

async def smuggle_command(update, context):

    data = get_user(
        update.effective_user.id
    )

    if data["level"] < 5:

        await update.message.reply_text(
            "🔒 قاچاق خر از سطح ۵ باز می‌شود."
        )

        return

    result, reward = smuggle()

    if result == "دستگیر":

        update_user(
            update.effective_user.id,
            jail_until=int(time.time()) + 600
        )

        await update.message.reply_text(
            "🚨 دستگیر شدی!\n\n"
            "🏚️ به زندان خرهای بی‌ادب رفتی."
        )

        return

    update_user(
        update.effective_user.id,
        coins=data["coins"] + reward
    )

    await update.message.reply_text(
        f"🫏 قاچاق خر {result} بود!\n\n"
        f"🪙 +{reward} عر کوین"
    )


# =========================
# RESCUE
# =========================

async def rescue_command(update, context):

    if update.effective_chat.type == "private":

        await update.message.reply_text(
            "این رویداد مخصوص گروه است."
        )

        return

    group = get_group(
        update.effective_chat.id
    )

    attempt = group["rescue_attempts"] + 1

    if attempt > 3:

        await update.message.reply_text(
            "❌ سه تلاش گروه تمام شده است."
        )

        return

    cost = rescue_cost(attempt)

    user = get_user(
        update.effective_user.id
    )

    if user["coins"] < cost:

        await update.message.reply_text(
            f"❌ عر کوین کافی نداری.\n"
            f"هزینه تلاش: {cost}"
        )

        return

    update_user(
        update.effective_user.id,
        coins=user["coins"] - cost
    )

    from database import db

    db.execute(
        """
        UPDATE groups
        SET rescue_attempts=?
        WHERE chat_id=?
        """,
        (
            attempt,
            update.effective_chat.id
        )
    )

    db.commit()

    result = rescue()

    if result == "موفق":

        await update.message.reply_text(
            "🎉 نجات موفق بود!\n\n"
            "🫏 کره خر خیابانی نجات پیدا کرد!"
        )

    elif result == "مرد":

        await update.message.reply_text(
            "💀 متأسفانه کره خر از دست رفت."
        )

    else:

        await update.message.reply_text(
            "😱 تلاش ناموفق بود!\n\n"
            "هنوز می‌توانید تلاش دیگری انجام دهید."
        )


# =========================
# TEXT
# =========================

async def text_handler(update, context):

    text = update.message.text.strip()

    if text == "عر":

        await aar(update, context)

    elif text in [
        "کره خر",
        "کره‌خر",
        "کرهخر"
    ]:

        await pet(update, context)

    elif text in [
        "هویج",
        "بازی هویج",
        "هویج یابی",
        "هویج‌یابی"
    ]:

        await carrot(update, context)

    elif text in [
        "موجودی",
        "کیف پول",
        "عر کوین"
    ]:

        await wallet(update, context)

    elif text == "قاچاق خر":

        await smuggle_command(
            update,
            context
        )

    elif text == "نجات کره خر":

        await rescue_command(
            update,
            context
        )

    elif text in [
        "پروفایل",
        "عرهاش"
    ]:

        await profile(
            update,
            update.effective_user.id
        )


# =========================
# CALLBACKS
# =========================

async def callbacks(update, context):

    query = update.callback_query

    await query.answer()

    user = get_user(
        query.from_user.id
    )

    if query.data == "wallet":

        await query.edit_message_text(
            f"🪙 موجودی شما:\n\n"
            f"{user['coins']} عر کوین"
        )

    elif query.data == "pet":

        await query.edit_message_text(
            f"🫏 {user['pet_name']}\n\n"
            f"⭐ سطح: {user['pet_level']}\n"
            f"🥕 غذا: {user['pet_food']}/8"
        )

    elif query.data == "carrot":

        await query.edit_message_text(
            "🥕 برای بازی هویج، بنویس:\n"
            "هویج"
        )

    elif query.data == "help":

        await query.edit_message_text(
            "📖 راهنمای خر بات\n\n"
            "🫏 عر\n"
            "🥕 هویج\n"
            "🫏 کره خر\n"
            "🪙 کیف پول\n"
            "🏴 قاچاق خر\n"
            "🆘 نجات کره خر\n"
            "👤 پروفایل"
        )


# =========================
# MAIN
# =========================

def main():

    init_db()

    app = (
        Application
        .builder()
        .token(BOT_TOKEN)
        .build()
    )

    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            callbacks
        )
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            text_handler
        )
    )

    print("خر بات روشن شد.")

    app.run_polling()


if __name__ == "__main__":
    main()
