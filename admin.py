from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def admin_panel():
    keyboard = [
        [
            InlineKeyboardButton(
                "💰 خزانه",
                callback_data="admin_treasury"
            )
        ],
        [
            InlineKeyboardButton(
                "⚙️ تنظیمات اقتصاد",
                callback_data="admin_economy"
            )
        ],
        [
            InlineKeyboardButton(
                "🏭 کارخانه‌ها",
                callback_data="admin_factories"
            )
        ],
        [
            InlineKeyboardButton(
                "🏚️ زندان",
                callback_data="admin_jail"
            )
        ],
        [
            InlineKeyboardButton(
                "📊 آمار گروه",
                callback_data="admin_stats"
            )
        ]
    ]

    return InlineKeyboardMarkup(keyboard)
