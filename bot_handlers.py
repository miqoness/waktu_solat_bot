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
from translations import get_translation, get_all_texts_for_key, detect_language, SUPPORTED_LANGUAGES
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


_MAIN_MENU_ACTIONS = {}
for _btn_key, _action in [
    ('btn_prayer_times', 'prayer_times'),
    ('btn_hadith', 'hadith'),
    ('btn_doa', 'doa'),
    ('btn_qiblat', 'qiblat'),
    ('btn_stats', 'stats'),
    ('btn_settings', 'settings'),
    ('btn_help', 'help'),
    ('btn_back', 'back'),
]:
    for _text in get_all_texts_for_key(_btn_key):
        _MAIN_MENU_ACTIONS[_text] = _action

_SETTINGS_ACTIONS = {}
for _btn_key, _action in [
    ('btn_select_zone', 'select_zone'),
    ('btn_change_language', 'change_language'),
    ('btn_pre_notification', 'pre_notification'),
    ('btn_weekly', 'weekly'),
    ('btn_monthly', 'monthly'),
]:
    for _text in get_all_texts_for_key(_btn_key):
        _SETTINGS_ACTIONS[_text] = _action


def register_handlers(bot: TeleBot):

    @bot.message_handler(commands=['start'])
    def start_command(message: Message):
        user_id = message.from_user.id
        lang = _get_or_detect_language(user_id, message.from_user.language_code)
        bot.reply_to(message, get_translation(lang, 'welcome'))
        send_main_menu(bot, message, lang)

    @bot.message_handler(commands=['help'])
    def help_command(message: Message):
        lang = get_user_language(message.from_user.id)
        bot.reply_to(message, get_translation(lang, 'help_text'), parse_mode='Markdown')

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
            next_prayer, next_time, location_type, remaining_mins = get_next_prayer(zone, lat, lon)
            lang = get_user_language(user_id)
            if next_prayer and remaining_mins is not None:
                if remaining_mins >= 60:
                    cd = get_translation(lang, 'countdown_hours_mins').format(
                        h=remaining_mins // 60, m=remaining_mins % 60)
                else:
                    cd = get_translation(lang, 'countdown_mins').format(m=remaining_mins)
                response = get_translation(lang, 'next_prayer_countdown').format(next_prayer, next_time, cd)
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
        lang = get_user_language(user_id)
        if not zone and lat and lon:
            zone = get_malaysia_zone(lat, lon)
        if zone or (lat and lon):
            result = format_weekly_prayer_times(zone, lat, lon, lang)
            if result:
                bot.send_message(message.chat.id, result, parse_mode='Markdown')
            else:
                bot.reply_to(message, get_translation(lang, 'weekly_not_available'))
        else:
            send_location_request(bot, message)

    @bot.message_handler(commands=['monthly'])
    def monthly_command(message: Message):
        user_id = message.from_user.id
        zone, lat, lon = get_user_location_info(user_id)
        lang = get_user_language(user_id)
        if not zone and lat and lon:
            zone = get_malaysia_zone(lat, lon)
        if zone or (lat and lon):
            msgs = format_monthly_prayer_times(zone, lat, lon, lang)
            if msgs:
                for msg in msgs:
                    bot.send_message(message.chat.id, msg, parse_mode='Markdown')
            else:
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
        send_language_selection(bot, message)

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
            bot.reply_to(message, get_translation(lang, 'zone_updated').format(selected_zone_name),
                         reply_markup=ReplyKeyboardRemove())
            prayer_times_text = format_prayer_times(zone_code, lang=lang)
            if prayer_times_text:
                bot.send_message(user_id, prayer_times_text, parse_mode='Markdown',
                                 reply_markup=_prayer_log_keyboard(user_id))
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
            bot.send_message(user_id, prayer_times_text, parse_mode='Markdown',
                             reply_markup=_prayer_log_keyboard(user_id))
        else:
            bot.send_message(user_id, get_translation(lang, 'error_getting_prayer_times'))

        send_main_menu(bot, message, lang)

    # --- Language callback (InlineKeyboard) ---

    @bot.callback_query_handler(func=lambda call: call.data.startswith('lang_'))
    def handle_language_callback(call):
        user_id = call.from_user.id
        lang = call.data.split('_', 1)[1]
        if lang not in SUPPORTED_LANGUAGES:
            lang = 'en'
        update_user_language(user_id, lang)
        bot.answer_callback_query(call.id, get_translation(lang, 'language_updated'))
        bot.edit_message_text(get_translation(lang, 'language_updated'),
                              call.message.chat.id, call.message.message_id)
        send_main_menu(bot, call.message, lang)

    # --- Main menu buttons (all 7 languages) ---

    @bot.message_handler(func=lambda message: message.text in _MAIN_MENU_ACTIONS)
    def handle_main_menu(message: Message):
        action = _MAIN_MENU_ACTIONS[message.text]
        if action == 'prayer_times':
            send_today_prayer_times(bot, message)
        elif action == 'hadith':
            send_daily_hadith(bot, message)
        elif action == 'doa':
            send_daily_doa(bot, message)
        elif action == 'qiblat':
            qiblat_command(message)
        elif action == 'stats':
            send_prayer_stats(bot, message)
        elif action == 'settings':
            send_settings_menu(bot, message)
        elif action == 'help':
            help_command(message)
        elif action == 'back':
            lang = get_user_language(message.from_user.id)
            send_main_menu(bot, message, lang)

    # --- Settings submenu (all 7 languages) ---

    @bot.message_handler(func=lambda message: message.text in _SETTINGS_ACTIONS)
    def handle_settings(message: Message):
        action = _SETTINGS_ACTIONS[message.text]
        if action == 'select_zone':
            send_state_selection(bot, message)
        elif action == 'change_language':
            send_language_selection(bot, message)
        elif action == 'pre_notification':
            send_pre_notification_menu(bot, message)
        elif action == 'weekly':
            weekly_command(message)
        elif action == 'monthly':
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
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                          reply_markup=new_markup)
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
                emojis = {'Subuh': '🌄', 'Syuruk': '🌅', 'Zohor': '☀️',
                          'Asar': '🌇', 'Maghrib': '🌆', 'Isyak': '🌙'}
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

def _get_or_detect_language(user_id, telegram_lang_code=None):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT language FROM users WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    conn.close()
    if result:
        return result[0]
    lang = detect_language(telegram_lang_code)
    update_user_language(user_id, lang)
    return lang


def send_main_menu(bot, message: Message, lang=None):
    if lang is None:
        lang = get_user_language(message.from_user.id)
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(get_translation(lang, 'btn_prayer_times'))
    markup.row(get_translation(lang, 'btn_hadith'), get_translation(lang, 'btn_doa'))
    markup.row(get_translation(lang, 'btn_qiblat'), get_translation(lang, 'btn_stats'))
    markup.row(get_translation(lang, 'btn_settings'), get_translation(lang, 'btn_help'))
    bot.send_message(message.chat.id, get_translation(lang, 'select_option'), reply_markup=markup)


def send_settings_menu(bot, message: Message):
    lang = get_user_language(message.from_user.id)
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton(get_translation(lang, 'btn_send_location'), request_location=True))
    markup.add(KeyboardButton(get_translation(lang, 'btn_select_zone')))
    markup.add(KeyboardButton(get_translation(lang, 'btn_change_language')))
    markup.add(KeyboardButton(get_translation(lang, 'btn_pre_notification')))
    markup.row(get_translation(lang, 'btn_weekly'), get_translation(lang, 'btn_monthly'))
    markup.add(KeyboardButton(get_translation(lang, 'btn_back')))
    bot.reply_to(message, get_translation(lang, 'select_setting'), reply_markup=markup)


def send_location_request(bot, message: Message):
    lang = get_user_language(message.from_user.id)
    markup = ReplyKeyboardMarkup(row_width=2)
    markup.add(KeyboardButton(get_translation(lang, 'btn_send_location'), request_location=True))
    markup.add(KeyboardButton(get_translation(lang, 'btn_select_zone')))
    bot.reply_to(message, get_translation(lang, 'select_setting'), reply_markup=markup)


def send_language_selection(bot, message: Message):
    lang = get_user_language(message.from_user.id)
    markup = InlineKeyboardMarkup(row_width=2)
    buttons = []
    for code, name in SUPPORTED_LANGUAGES.items():
        buttons.append(InlineKeyboardButton(name, callback_data=f"lang_{code}"))
    markup.add(*buttons)
    bot.reply_to(message, get_translation(lang, 'select_language'), reply_markup=markup)


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
        bot.send_message(message.chat.id, prayer_times_text, parse_mode='Markdown',
                         reply_markup=_prayer_log_keyboard(user_id))
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
        (get_translation(lang, 'prenotify_off'), 0),
        (get_translation(lang, 'prenotify_min').format(5), 5),
        (get_translation(lang, 'prenotify_min').format(10), 10),
        (get_translation(lang, 'prenotify_min').format(15), 15),
        (get_translation(lang, 'prenotify_min').format(20), 20),
        (get_translation(lang, 'prenotify_min').format(30), 30),
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
