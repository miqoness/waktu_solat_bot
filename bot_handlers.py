from telebot import TeleBot
from telebot.types import (
    Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove,
    InlineKeyboardMarkup, InlineKeyboardButton,
    InlineQueryResultArticle, InputTextMessageContent,
)
from database import (
    get_db_connection, update_user_location, update_user_language,
    update_user_pre_notification, get_user_pre_notification,
    log_prayer, get_today_prayers, get_prayer_stats, get_user_location_info as db_get_user_location_info,
)
from translations import get_translation
from prayer_times import (
    MALAYSIA_ZONES, FARD_PRAYERS,
    format_prayer_times, format_weekly_prayer_times, format_monthly_prayer_times,
    get_next_prayer, get_prayer_times, parse_time,
)
from zone_finder import get_malaysia_zone, get_location_name
from hadis_harian import send_daily_hadith
from doa_harian import send_daily_doa
from qiblat import format_qiblat_info
from datetime import datetime
from pytz import timezone
import hashlib


def register_handlers(bot: TeleBot):

    # --- Commands ---

    @bot.message_handler(commands=['start'])
    def start_command(message: Message):
        lang = get_user_language(message.from_user.id)
        bot.reply_to(message, get_translation(lang, 'welcome'))
        send_main_menu(bot, message, lang)

    @bot.message_handler(commands=['help'])
    def help_command(message: Message):
        lang = get_user_language(message.from_user.id)
        bot.reply_to(message, get_translation(lang, 'help_text'))

    @bot.message_handler(commands=['zone'])
    def zone_command(message: Message):
        send_state_selection(bot, message)

    @bot.message_handler(commands=['times'])
    def times_command(message: Message):
        send_today_prayer_times(bot, message)

    @bot.message_handler(commands=['next'])
    def next_prayer_command(message: Message):
        user_id = message.from_user.id
        zone, lat, lon = get_user_location_info(user_id)
        if zone or (lat and lon):
            next_prayer, next_time, location_type, countdown = get_next_prayer(zone, lat, lon)
            lang = get_user_language(user_id)
            if next_prayer and countdown:
                response = get_translation(lang, 'next_prayer_countdown').format(next_prayer, next_time, countdown)
            elif next_prayer:
                response = get_translation(lang, 'next_prayer').format(next_prayer, next_time)
            else:
                response = get_translation(lang, 'error_getting_prayer_times')
            bot.reply_to(message, response, parse_mode='Markdown')
        else:
            send_location_request(bot, message)

    @bot.message_handler(commands=['hadith'])
    def hadith_command(message: Message):
        send_daily_hadith(bot, message)

    @bot.message_handler(commands=['doa'])
    def doa_command(message: Message):
        send_daily_doa(bot, message)

    @bot.message_handler(commands=['qiblat'])
    def qiblat_command(message: Message):
        user_id = message.from_user.id
        _, lat, lon = get_user_location_info(user_id)
        if lat and lon:
            result = format_qiblat_info(lat, lon)
            bot.reply_to(message, result, parse_mode='Markdown')
        else:
            lang = get_user_language(user_id)
            bot.reply_to(message, get_translation(lang, 'qiblat_need_location'))
            send_location_request(bot, message)

    @bot.message_handler(commands=['weekly'])
    def weekly_command(message: Message):
        user_id = message.from_user.id
        zone, lat, lon = get_user_location_info(user_id)
        if not zone and lat and lon:
            zone = get_malaysia_zone(lat, lon)
        if zone or (lat and lon):
            result = format_weekly_prayer_times(zone, lat, lon)
            if result:
                bot.send_message(message.chat.id, result, parse_mode='Markdown')
            else:
                lang = get_user_language(user_id)
                bot.reply_to(message, get_translation(lang, 'weekly_not_available'))
        else:
            send_location_request(bot, message)

    @bot.message_handler(commands=['monthly'])
    def monthly_command(message: Message):
        user_id = message.from_user.id
        zone, lat, lon = get_user_location_info(user_id)
        if not zone and lat and lon:
            zone = get_malaysia_zone(lat, lon)
        if zone or (lat and lon):
            msgs = format_monthly_prayer_times(zone, lat, lon)
            if msgs:
                for msg in msgs:
                    bot.send_message(message.chat.id, msg, parse_mode='Markdown')
            else:
                lang = get_user_language(user_id)
                bot.reply_to(message, get_translation(lang, 'monthly_not_available'))
        else:
            send_location_request(bot, message)

    @bot.message_handler(commands=['stats'])
    def stats_command(message: Message):
        send_prayer_stats(bot, message)

    @bot.message_handler(commands=['prenotify'])
    def prenotify_command(message: Message):
        send_pre_notification_menu(bot, message)

    @bot.message_handler(commands=['language'])
    def language_command(message: Message):
        markup = ReplyKeyboardMarkup(row_width=2)
        markup.add(KeyboardButton("Bahasa Melayu"), KeyboardButton("English"))
        bot.reply_to(message, "Please select your language / Sila pilih bahasa anda:", reply_markup=markup)

    # --- State/Zone selection ---

    @bot.message_handler(func=lambda message: message.text in MALAYSIA_ZONES.keys())
    def handle_state_selection(message: Message):
        send_zone_selection(bot, message, message.text)

    @bot.message_handler(func=lambda message: any(message.text in zones.values() for zones in MALAYSIA_ZONES.values()))
    def handle_zone_selection(message: Message):
        user_id = message.from_user.id
        selected_zone_name = message.text
        zone_code = None
        for state, zones in MALAYSIA_ZONES.items():
            for code, name in zones.items():
                if name == selected_zone_name:
                    zone_code = code
                    break
            if zone_code:
                break

        if zone_code:
            update_user_location(user_id, zone=zone_code)
            lang = get_user_language(user_id)
            bot.reply_to(message, get_translation(lang, 'zone_updated').format(selected_zone_name), reply_markup=ReplyKeyboardRemove())

            prayer_times_text = format_prayer_times(zone_code, lang=lang)
            if prayer_times_text:
                bot.send_message(user_id, prayer_times_text, parse_mode='Markdown', reply_markup=_prayer_log_keyboard(user_id))
            else:
                bot.send_message(user_id, get_translation(lang, 'error_getting_prayer_times'))
        else:
            lang = get_user_language(user_id)
            bot.reply_to(message, get_translation(lang, 'invalid_zone'))

        lang = get_user_language(user_id)
        send_main_menu(bot, message, lang)

    # --- Location handler ---

    @bot.message_handler(content_types=['location'])
    def handle_location(message: Message):
        user_id = message.from_user.id
        lat = message.location.latitude
        lon = message.location.longitude
        lang = get_user_language(user_id)

        zone = get_malaysia_zone(lat, lon)

        if zone:
            update_user_location(user_id, zone=zone, lat=lat, lon=lon)
            zone_name = get_zone_name(zone)
            bot.reply_to(message, get_translation(lang, 'location_updated').format(zone_name))
        else:
            update_user_location(user_id, lat=lat, lon=lon)
            loc_name = get_location_name(lat, lon)
            bot.reply_to(message, get_translation(lang, 'location_updated_intl').format(loc_name))

        prayer_times_text = format_prayer_times(zone, lat, lon, lang)
        if prayer_times_text:
            bot.send_message(user_id, prayer_times_text, parse_mode='Markdown', reply_markup=_prayer_log_keyboard(user_id))
        else:
            bot.send_message(user_id, get_translation(lang, 'error_getting_prayer_times'))

        send_main_menu(bot, message, lang)

    # --- Language selection ---

    @bot.message_handler(func=lambda message: message.text in ["Bahasa Melayu", "English"])
    def handle_language_selection(message: Message):
        user_id = message.from_user.id
        lang = 'ms' if message.text == "Bahasa Melayu" else 'en'
        update_user_language(user_id, lang)
        bot.reply_to(message, get_translation(lang, 'language_updated'), reply_markup=ReplyKeyboardRemove())
        send_main_menu(bot, message, lang)

    # --- Main menu buttons ---

    @bot.message_handler(func=lambda message: message.text in [
        "📅 Waktu Solat Hari Ini", "📚 Hadith Harian", "🕋 Arah Kiblat",
        "🤲 Doa Harian", "📊 Statistik Solat", "⚙️ Tetapan", "❓ Bantuan",
        "Kembali ke Menu Utama",
    ])
    def handle_main_menu(message: Message):
        text = message.text
        if text == "📅 Waktu Solat Hari Ini":
            send_today_prayer_times(bot, message)
        elif text == "📚 Hadith Harian":
            send_daily_hadith(bot, message)
        elif text == "🕋 Arah Kiblat":
            qiblat_command(message)
        elif text == "🤲 Doa Harian":
            send_daily_doa(bot, message)
        elif text == "📊 Statistik Solat":
            send_prayer_stats(bot, message)
        elif text == "⚙️ Tetapan":
            send_settings_menu(bot, message)
        elif text == "❓ Bantuan":
            help_command(message)
        elif text == "Kembali ke Menu Utama":
            lang = get_user_language(message.from_user.id)
            send_main_menu(bot, message, lang)

    # --- Settings submenu ---

    @bot.message_handler(func=lambda message: message.text in [
        "Pilih Zon Malaysia", "Tukar Bahasa", "Peringatan Awal",
        "📅 Mingguan", "📅 Bulanan",
    ])
    def process_choice(message: Message):
        text = message.text
        if text == "Pilih Zon Malaysia":
            send_state_selection(bot, message)
        elif text == "Tukar Bahasa":
            language_command(message)
        elif text == "Peringatan Awal":
            send_pre_notification_menu(bot, message)
        elif text == "📅 Mingguan":
            weekly_command(message)
        elif text == "📅 Bulanan":
            monthly_command(message)

    # --- Pre-notification callback ---

    @bot.callback_query_handler(func=lambda call: call.data.startswith('prenotify_'))
    def handle_prenotify_callback(call):
        user_id = call.from_user.id
        minutes = int(call.data.split('_')[1])
        update_user_pre_notification(user_id, minutes)
        lang = get_user_language(user_id)

        if minutes == 0:
            text = get_translation(lang, 'pre_notification_off')
        else:
            text = get_translation(lang, 'pre_notification_set').format(minutes)

        bot.answer_callback_query(call.id, text)
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id)

    # --- Prayer log callback ---

    @bot.callback_query_handler(func=lambda call: call.data.startswith('log_'))
    def handle_prayer_log_callback(call):
        user_id = call.from_user.id
        prayer_name = call.data.split('_', 1)[1]
        lang = get_user_language(user_id)
        today = datetime.now(timezone('Asia/Kuala_Lumpur')).strftime('%Y-%m-%d')

        inserted = log_prayer(user_id, prayer_name, today)
        if inserted:
            text = get_translation(lang, 'prayer_logged').format(prayer_name)
        else:
            text = get_translation(lang, 'prayer_already_logged').format(prayer_name)

        bot.answer_callback_query(call.id, text)

        try:
            new_markup = _prayer_log_keyboard(user_id)
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=new_markup)
        except Exception:
            pass

    # --- Inline query handler ---

    @bot.inline_handler(lambda query: True)
    def handle_inline_query(inline_query):
        query_text = inline_query.query.strip().upper()
        results = []

        matched_zones = []
        for state, zones in MALAYSIA_ZONES.items():
            for code, name in zones.items():
                if not query_text or query_text in code or query_text in name.upper() or query_text in state.upper():
                    matched_zones.append((code, name, state))

        for code, name, state in matched_zones[:20]:
            prayer_times_data, _ = get_prayer_times(code)
            if prayer_times_data:
                lines = [f"🕌 Waktu Solat — {name} ({code})"]
                emojis = {'Subuh': '🌄', 'Syuruk': '🌅', 'Zohor': '☀️', 'Asar': '🌇', 'Maghrib': '🌆', 'Isyak': '🌙'}
                for prayer, time_val in prayer_times_data.items():
                    parsed = parse_time(time_val)
                    lines.append(f"{emojis.get(prayer, '')} {prayer}: {parsed or 'N/A'}")
                content = "\n".join(lines)
            else:
                content = f"Waktu solat tidak tersedia untuk {name} ({code})"

            result_id = hashlib.md5(code.encode()).hexdigest()
            results.append(InlineQueryResultArticle(
                id=result_id,
                title=f"{code} — {name}",
                description=state,
                input_message_content=InputTextMessageContent(content),
            ))

        try:
            bot.answer_inline_query(inline_query.id, results, cache_time=300)
        except Exception as e:
            print(f"Inline query error: {e}")

    # --- Catch-all ---

    @bot.message_handler(func=lambda message: True)
    def handle_all_messages(message: Message):
        lang = get_user_language(message.from_user.id)
        bot.reply_to(message, get_translation(lang, 'unknown_message'))
        send_main_menu(bot, message, lang)


# --- Helper functions ---

def send_main_menu(bot, message: Message, lang=None):
    if lang is None:
        lang = get_user_language(message.from_user.id)
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('📅 Waktu Solat Hari Ini')
    markup.row('📚 Hadith Harian', '🤲 Doa Harian')
    markup.row('🕋 Arah Kiblat', '📊 Statistik Solat')
    markup.row('⚙️ Tetapan', '❓ Bantuan')
    bot.send_message(message.chat.id, get_translation(lang, 'select_option'), reply_markup=markup)


def send_settings_menu(bot, message: Message):
    lang = get_user_language(message.from_user.id)
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Hantar Lokasi", request_location=True))
    markup.add(KeyboardButton("Pilih Zon Malaysia"))
    markup.add(KeyboardButton("Tukar Bahasa"))
    markup.add(KeyboardButton("Peringatan Awal"))
    markup.row("📅 Mingguan", "📅 Bulanan")
    markup.add(KeyboardButton("Kembali ke Menu Utama"))
    bot.reply_to(message, get_translation(lang, 'select_setting'), reply_markup=markup)


def send_location_request(bot, message: Message):
    markup = ReplyKeyboardMarkup(row_width=2)
    markup.add(KeyboardButton("Hantar Lokasi", request_location=True))
    markup.add(KeyboardButton("Pilih Zon Malaysia"))
    lang = get_user_language(message.from_user.id)
    bot.reply_to(message, get_translation(lang, 'select_setting'), reply_markup=markup)


def send_state_selection(bot: TeleBot, message: Message):
    lang = get_user_language(message.from_user.id)
    markup = ReplyKeyboardMarkup(row_width=2)
    for state in MALAYSIA_ZONES.keys():
        markup.add(KeyboardButton(state))
    bot.reply_to(message, get_translation(lang, 'select_state'), reply_markup=markup)


def send_zone_selection(bot: TeleBot, message: Message, selected_state: str):
    lang = get_user_language(message.from_user.id)
    markup = ReplyKeyboardMarkup(row_width=1)
    for zone_name in MALAYSIA_ZONES[selected_state].values():
        markup.add(KeyboardButton(zone_name))
    bot.reply_to(message, get_translation(lang, 'select_zone').format(selected_state), reply_markup=markup)


def send_today_prayer_times(bot, message: Message):
    user_id = message.from_user.id
    zone, lat, lon = get_user_location_info(user_id)
    lang = get_user_language(user_id)
    if zone or (lat and lon):
        prayer_times_text = format_prayer_times(zone, lat, lon, lang)
        bot.send_message(message.chat.id, prayer_times_text, parse_mode='Markdown', reply_markup=_prayer_log_keyboard(user_id))
    else:
        bot.reply_to(message, get_translation(lang, 'location_not_set'))
        send_location_request(bot, message)


def send_prayer_stats(bot, message: Message):
    user_id = message.from_user.id
    lang = get_user_language(user_id)
    stats = get_prayer_stats(user_id)

    if stats['total'] == 0:
        bot.reply_to(message, get_translation(lang, 'stats_empty'))
        return

    today = datetime.now(timezone('Asia/Kuala_Lumpur')).strftime('%Y-%m-%d')
    today_prayers = get_today_prayers(user_id, today)

    text = get_translation(lang, 'stats_header')
    text += get_translation(lang, 'stats_streak').format(stats['streak'])
    text += get_translation(lang, 'stats_total').format(stats['total'])
    text += get_translation(lang, 'stats_week').format(stats['week_total'])
    text += get_translation(lang, 'stats_month').format(stats['month_total'])
    text += get_translation(lang, 'stats_today')

    for prayer in FARD_PRAYERS:
        check = "✅" if prayer in today_prayers else "⬜"
        text += f"  {check} {prayer}\n"

    bot.reply_to(message, text, parse_mode='Markdown')


def send_pre_notification_menu(bot, message: Message):
    user_id = message.from_user.id
    lang = get_user_language(user_id)
    current = get_user_pre_notification(user_id)

    markup = InlineKeyboardMarkup(row_width=3)
    options = [
        ("Matikan", 0), ("5 minit", 5), ("10 minit", 10),
        ("15 minit", 15), ("20 minit", 20), ("30 minit", 30),
    ]

    buttons = []
    for label, mins in options:
        indicator = " ✓" if mins == current else ""
        buttons.append(InlineKeyboardButton(f"{label}{indicator}", callback_data=f"prenotify_{mins}"))

    markup.add(*buttons)
    bot.reply_to(message, get_translation(lang, 'select_pre_notification'), reply_markup=markup)


def _prayer_log_keyboard(user_id):
    today = datetime.now(timezone('Asia/Kuala_Lumpur')).strftime('%Y-%m-%d')
    logged = get_today_prayers(user_id, today)

    markup = InlineKeyboardMarkup(row_width=3)
    buttons = []
    for prayer in FARD_PRAYERS:
        check = "✅ " if prayer in logged else ""
        buttons.append(InlineKeyboardButton(f"{check}{prayer}", callback_data=f"log_{prayer}"))
    markup.add(*buttons)
    return markup


def get_user_language(user_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT language FROM users WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else 'ms'


def get_user_location_info(user_id):
    return db_get_user_location_info(user_id)


def get_zone_name(zone):
    for state, zones in MALAYSIA_ZONES.items():
        if zone in zones:
            return zones[zone]
    return zone
