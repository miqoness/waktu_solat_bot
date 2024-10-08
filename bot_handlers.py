from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from database import get_db_connection, update_user_location, update_user_method, update_user_language
from translations import get_translation
from prayer_times import MALAYSIA_ZONES, format_prayer_times, get_next_prayer, get_calculation_methods

def register_handlers(bot: TeleBot):
    @bot.message_handler(commands=['start'])
    def start_command(message: Message):
        user_id = message.from_user.id
        lang = get_user_language(user_id)
        bot.reply_to(message, get_translation(lang, 'welcome'))
        send_location_request(bot, message)

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
                bot.send_message(user_id, prayer_times)
            else:
                bot.send_message(user_id, get_translation(lang, 'error_getting_prayer_times'))

            print(f"User {user_id} selected zone {zone_code} ({selected_zone_name}). Prayer times: {prayer_times}")  # Debug print
        else:
            bot.reply_to(message, "Maaf, zon yang dipilih tidak sah.")

    @bot.message_handler(commands=['method'])
    def method_command(message: Message):
        send_method_selection(bot, message)

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
        update_user_location(user_id, lat, lon)
        
        lang = get_user_language(user_id)
        bot.reply_to(message, get_translation(lang, 'location_updated'))
        
        method = get_user_method(user_id)
        prayer_times = format_prayer_times(None, lat, lon, method)
        bot.send_message(user_id, prayer_times)

    @bot.message_handler(func=lambda message: message.text.isdigit() and int(message.text) in get_calculation_methods())
    def handle_method_selection(message: Message):
        user_id = message.from_user.id
        selected_method = int(message.text)
        update_user_method(user_id, selected_method)
        
        lang = get_user_language(user_id)
        method_name = get_calculation_methods()[selected_method]
        bot.reply_to(message, get_translation(lang, 'method_updated').format(method_name), reply_markup=ReplyKeyboardRemove())
        
        lat, lon = get_user_location(user_id)
        if lat and lon:
            prayer_times = format_prayer_times(None, lat, lon, selected_method)
            bot.send_message(user_id, prayer_times)

    @bot.message_handler(func=lambda message: message.text in ["Bahasa Melayu", "English"])
    def handle_language_selection(message: Message):
        user_id = message.from_user.id
        lang = 'ms' if message.text == "Bahasa Melayu" else 'en'
        update_user_language(user_id, lang)
        bot.reply_to(message, get_translation(lang, 'language_updated'), reply_markup=ReplyKeyboardRemove())

    @bot.message_handler(func=lambda message: message.text in ["Pilih Zon Malaysia", "Pilih Kaedah Pengiraan"])
    def process_choice(message: Message):
        if message.text == "Pilih Zon Malaysia":
            send_state_selection(bot, message)
        elif message.text == "Pilih Kaedah Pengiraan":
            send_method_selection(bot, message)

    @bot.message_handler(commands=['times'])
    def times_command(message: Message):
        user_id = message.from_user.id
        zone, lat, lon = get_user_location_info(user_id)
        method = get_user_method(user_id)
        if zone or (lat and lon):
            prayer_times = format_prayer_times(zone, lat, lon, method)
            bot.reply_to(message, prayer_times)
        else:
            send_location_request(bot, message)

    @bot.message_handler(commands=['next'])
    def next_prayer_command(message: Message):
        user_id = message.from_user.id
        zone, lat, lon = get_user_location_info(user_id)
        method = get_user_method(user_id)
        if zone or (lat and lon):
            next_prayer, next_time, location_type = get_next_prayer(zone, lat, lon, method)
            lang = get_user_language(user_id)
            response = get_translation(lang, 'next_prayer').format(next_prayer, next_time)
            bot.reply_to(message, response)
        else:
            send_location_request(bot, message)

def send_location_request(bot, message: Message):
    markup = ReplyKeyboardMarkup(row_width=2)
    markup.add(KeyboardButton("Hantar Lokasi", request_location=True))
    markup.add(KeyboardButton("Pilih Zon Malaysia"))
    markup.add(KeyboardButton("Pilih Kaedah Pengiraan"))
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

def send_method_selection(bot, message: Message):
    markup = ReplyKeyboardMarkup(row_width=2)
    methods = get_calculation_methods()
    for method_id, method_name in methods.items():
        markup.add(KeyboardButton(str(method_id)))
    bot.reply_to(message, "Sila pilih kaedah pengiraan waktu solat:", reply_markup=markup)

def get_user_language(user_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT language FROM users WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else 'ms'  # Default ke Bahasa Melayu jika tiada pilihan

def get_user_method(user_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT calculation_method FROM users WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else 2  # Default ke ISNA jika tiada pilihan

def get_user_location_info(user_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT zone, latitude, longitude FROM users WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    conn.close()
    return result if result else (None, None, None)

def get_user_location(user_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT latitude, longitude FROM users WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    conn.close()
    return result if result else (None, None)