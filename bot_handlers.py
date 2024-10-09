from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from database import get_db_connection, update_user_location, update_user_language
from translations import get_translation
from prayer_times import MALAYSIA_ZONES, format_prayer_times, get_next_prayer
from zone_finder import get_malaysia_zone
from hadis_harian import send_daily_hadith  # Import fungsi hadis harian
from datetime import datetime

def register_handlers(bot: TeleBot):
    @bot.message_handler(commands=['start'])
    def start_command(message: Message):
        user_id = message.from_user.id
        lang = get_user_language(user_id)
        bot.reply_to(message, get_translation(lang, 'welcome'))
        send_main_menu(bot, message)

    @bot.message_handler(commands=['help'])
    def help_command(message: Message):
        user_id = message.from_user.id
        lang = get_user_language(user_id)
        help_text = get_translation(lang, 'help_text')
        bot.reply_to(message, help_text)

    @bot.message_handler(commands=['zone'])
    def zone_command(message: Message):
        send_state_selection(bot, message)

    @bot.message_handler(func=lambda message: message.text in MALAYSIA_ZONES.keys())
    def handle_state_selection(message: Message):
        user_id = message.from_user.id
        selected_state = message.text
        send_zone_selection(bot, message, selected_state)

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
            
            prayer_times = format_prayer_times(zone_code)
            if prayer_times:
                bot.send_message(user_id, prayer_times, parse_mode='Markdown')
            else:
                bot.send_message(user_id, get_translation(lang, 'error_getting_prayer_times'))

            print(f"User {user_id} selected zone {zone_code} ({selected_zone_name}). Prayer times: {prayer_times}")  # Debug print
        else:
            bot.reply_to(message, "Maaf, zon yang dipilih tidak sah.")
        send_main_menu(bot, message)

    @bot.message_handler(commands=['language'])
    def language_command(message: Message):
        markup = ReplyKeyboardMarkup(row_width=2)
        markup.add(KeyboardButton("Bahasa Melayu"), KeyboardButton("English"))
        bot.reply_to(message, "Please select your language / Sila pilih bahasa anda:", reply_markup=markup)

    @bot.message_handler(content_types=['location'])
    def handle_location(message: Message):
        user_id = message.from_user.id
        lat = message.location.latitude
        lon = message.location.longitude
        
        zone = get_malaysia_zone(lat, lon)
        if zone:
            update_user_location(user_id, zone=zone, lat=lat, lon=lon)
            lang = get_user_language(user_id)
            zone_name = get_zone_name(zone)
            bot.reply_to(message, get_translation(lang, 'location_updated').format(zone_name))
            
            prayer_times = format_prayer_times(zone)
            if prayer_times:
                bot.send_message(user_id, prayer_times, parse_mode='Markdown')
            else:
                bot.send_message(user_id, get_translation(lang, 'error_getting_prayer_times'))
        else:
            lang = get_user_language(user_id)
            bot.reply_to(message, get_translation(lang, 'location_out_of_malaysia'))
        
        send_main_menu(bot, message)

    @bot.message_handler(func=lambda message: message.text in ["Bahasa Melayu", "English"])
    def handle_language_selection(message: Message):
        user_id = message.from_user.id
        lang = 'ms' if message.text == "Bahasa Melayu" else 'en'
        update_user_language(user_id, lang)
        bot.reply_to(message, get_translation(lang, 'language_updated'), reply_markup=ReplyKeyboardRemove())
        send_main_menu(bot, message)

    @bot.message_handler(func=lambda message: message.text in ["📅 Waktu Solat Hari Ini", "📚 Hadith Harian", "⚙️ Tetapan", "❓ Bantuan", "Kembali ke Menu Utama"])
    def handle_main_menu(message: Message):
        if message.text == "📅 Waktu Solat Hari Ini":
            send_today_prayer_times(bot, message)
        elif message.text == "📚 Hadith Harian":
            send_daily_hadith(bot, message)
        elif message.text == "⚙️ Tetapan":
            send_settings_menu(bot, message)
        elif message.text == "❓ Bantuan":
            help_command(message)
        elif message.text == "Kembali ke Menu Utama":
            send_main_menu(bot, message)

    @bot.message_handler(func=lambda message: message.text in ["Pilih Zon Malaysia", "Tukar Bahasa"])
    def process_choice(message: Message):
        if message.text == "Pilih Zon Malaysia":
            send_state_selection(bot, message)
        elif message.text == "Tukar Bahasa":
            language_command(message)

    @bot.message_handler(commands=['times'])
    def times_command(message: Message):
        send_today_prayer_times(bot, message)

    @bot.message_handler(commands=['next'])
    def next_prayer_command(message: Message):
        user_id = message.from_user.id
        zone, lat, lon = get_user_location_info(user_id)
        if zone or (lat and lon):
            next_prayer, next_time, location_type = get_next_prayer(zone, lat, lon)
            lang = get_user_language(user_id)
            response = get_translation(lang, 'next_prayer').format(next_prayer, next_time)
            bot.reply_to(message, response)
        else:
            send_location_request(bot, message)

    @bot.message_handler(commands=['hadith'])
    def hadith_command(message: Message):
        send_daily_hadith(bot, message)

    @bot.message_handler(func=lambda message: True)
    def handle_all_messages(message: Message):
        bot.reply_to(message, "Maaf, saya tidak memahami mesej anda. Sila gunakan butang yang disediakan.")
        send_main_menu(bot, message)

def send_main_menu(bot, message: Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('📅 Waktu Solat Hari Ini')
    markup.row('📚 Hadith Harian')
    markup.row('⚙️ Tetapan', '❓ Bantuan')
    bot.send_message(message.chat.id, "Sila pilih:", reply_markup=markup)

def send_settings_menu(bot, message: Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Hantar Lokasi", request_location=True))
    markup.add(KeyboardButton("Pilih Zon Malaysia"))
    markup.add(KeyboardButton("Tukar Bahasa"))
    markup.add(KeyboardButton("Kembali ke Menu Utama"))
    bot.reply_to(message, "Sila pilih satu pilihan:", reply_markup=markup)

def send_location_request(bot, message: Message):
    markup = ReplyKeyboardMarkup(row_width=2)
    markup.add(KeyboardButton("Hantar Lokasi", request_location=True))
    markup.add(KeyboardButton("Pilih Zon Malaysia"))
    bot.reply_to(message, "Sila pilih satu pilihan:", reply_markup=markup)

def send_state_selection(bot: TeleBot, message: Message):
    markup = ReplyKeyboardMarkup(row_width=2)
    for state in MALAYSIA_ZONES.keys():
        markup.add(KeyboardButton(state))
    bot.reply_to(message, "Sila pilih negeri:", reply_markup=markup)

def send_zone_selection(bot: TeleBot, message: Message, selected_state: str):
    markup = ReplyKeyboardMarkup(row_width=1)
    for zone_name in MALAYSIA_ZONES[selected_state].values():
        markup.add(KeyboardButton(zone_name))
    bot.reply_to(message, f"Sila pilih zon untuk {selected_state}:", reply_markup=markup)

def send_today_prayer_times(bot, message: Message):
    user_id = message.from_user.id
    zone, lat, lon = get_user_location_info(user_id)
    if zone or (lat and lon):
        prayer_times = format_prayer_times(zone, lat, lon)
        bot.send_message(message.chat.id, prayer_times, parse_mode='Markdown')
    else:
        lang = get_user_language(user_id)
        bot.reply_to(message, get_translation(lang, 'location_not_set'))
        send_location_request(bot, message)

def get_user_language(user_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT language FROM users WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else 'ms'  # Default ke Bahasa Melayu jika tiada pilihan

def get_user_location_info(user_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT zone, latitude, longitude FROM users WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    conn.close()
    return result if result else (None, None, None)

def get_zone_name(zone):
    for state, zones in MALAYSIA_ZONES.items():
        if zone in zones:
            return zones[zone]
    return zone  # Return the zone code if not found