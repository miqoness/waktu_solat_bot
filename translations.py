translations = {
    'ms': {
        'welcome': "Selamat datang ke Bot Waktu Solat! Sila hantar lokasi anda untuk mendaftar peringatan waktu solat.",
        'choose_language': "Sila pilih bahasa anda:",
        'language_updated': "Bahasa telah dikemas kini ke Bahasa Melayu.",
        'location_updated': "Lokasi anda telah dikemas kini.",
        'zone_updated': "Zon waktu solat anda telah ditetapkan kepada {}.",
        'method_updated': "Kaedah pengiraan telah dikemas kini kepada: {}",
        'prayer_notification': "Telah masuk waktu {} solat. Waktu solat: {}",
        'next_prayer': "Waktu solat seterusnya adalah {} pada {}",
        'error_getting_prayer_times': "Maaf, tidak dapat mendapatkan waktu solat untuk lokasi anda.",
        'help_text': "Ini adalah bot waktu solat. Gunakan /start untuk memulakan, /language untuk menukar bahasa, /zone untuk memilih zon, dan /method untuk memilih kaedah pengiraan."
    },
    'en': {
        'welcome': "Welcome to the Prayer Time Bot! Please send your location to register for prayer time reminders.",
        'choose_language': "Please choose your language:",
        'language_updated': "Language has been updated to English.",
        'location_updated': "Your location has been updated.",
        'zone_updated': "Your prayer time zone has been set to {}.",
        'method_updated': "Calculation method has been updated to: {}",
        'prayer_notification': "It's time for {} prayer. Prayer time: {}",
        'next_prayer': "The next prayer time is {} at {}",
        'error_getting_prayer_times': "Sorry, unable to get prayer times for your location.",
        'help_text': "This is a prayer time bot. Use /start to begin, /language to change language, /zone to select zone, and /method to choose calculation method."
    }
}

def get_translation(lang, key):
    return translations.get(lang, translations['en']).get(key, f"Translation missing: {key}")