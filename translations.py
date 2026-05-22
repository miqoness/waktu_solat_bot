SUPPORTED_LANGUAGES = {
    'ms': 'Bahasa Melayu',
    'en': 'English',
    'ar': 'العربية',
    'tr': 'Türkçe',
    'ur': 'اردو',
    'id': 'Bahasa Indonesia',
    'fr': 'Français',
}

TELEGRAM_LANG_MAP = {
    'ms': 'ms', 'en': 'en', 'ar': 'ar', 'tr': 'tr',
    'ur': 'ur', 'id': 'id', 'fr': 'fr',
    'en-us': 'en', 'en-gb': 'en', 'pt-br': 'en',
    'zh': 'en', 'ja': 'en', 'ko': 'en', 'de': 'en',
    'es': 'en', 'it': 'en', 'ru': 'en', 'hi': 'ur',
    'fa': 'ar', 'bn': 'en',
}

translations = {
    'ms': {
        'welcome': "Selamat datang ke SalatTime Bot! 🕌\nSila hantar lokasi anda atau pilih zon untuk mula.",
        'language_updated': "Bahasa telah dikemas kini ke Bahasa Melayu. ✅",
        'location_updated': "Lokasi anda telah dikemas kini ke zon {}. ✅",
        'location_updated_intl': "Lokasi anda telah dikemas kini ke {}. ✅",
        'zone_updated': "Zon waktu solat anda telah ditetapkan kepada {}. ✅",
        'prayer_notification': "Telah masuk waktu solat {}. Waktu solat: {}",
        'pre_notification': "Lagi {minutes} minit untuk waktu solat {prayer}. Sila bersiap!",
        'next_prayer': "Waktu solat seterusnya adalah {} pada {}",
        'next_prayer_countdown': "Waktu solat seterusnya adalah *{}* pada *{}*\n⏳ Lagi *{}*",
        'error_getting_prayer_times': "Maaf, tidak dapat mendapatkan waktu solat untuk lokasi anda.",
        'help_text': (
            "🕌 *SalatTime Bot — Bantuan*\n\n"
            "/start — Mulakan bot\n"
            "/times — Waktu solat hari ini\n"
            "/next — Waktu solat seterusnya\n"
            "/weekly — Waktu solat mingguan\n"
            "/monthly — Waktu solat bulanan\n"
            "/zone — Pilih zon Malaysia\n"
            "/qiblat — Arah kiblat\n"
            "/doa — Doa harian\n"
            "/hadith — Hadith harian\n"
            "/stats — Statistik solat\n"
            "/prenotify — Peringatan awal\n"
            "/language — Tukar bahasa\n"
            "/help — Bantuan"
        ),
        'location_not_set': "Anda belum menetapkan lokasi atau zon. Sila hantar lokasi anda atau pilih zon.",
        'location_out_of_malaysia': "Maaf, lokasi yang anda hantar berada di luar Malaysia. Sila pilih zon secara manual.",
        'prayer_logged': "Solat {} telah direkodkan. Alhamdulillah! ✅",
        'prayer_already_logged': "Solat {} sudah direkodkan untuk hari ini.",
        'stats_header': "📊 *Statistik Solat Anda*\n",
        'stats_streak': "🔥 *Streak semasa:* {} hari berturut-turut (5/5 solat)\n",
        'stats_total': "📈 *Jumlah solat direkod:* {}\n",
        'stats_week': "📅 *Minggu ini:* {} solat\n",
        'stats_month': "🗓 *Bulan ini:* {} solat\n",
        'stats_today': "\n*Solat hari ini:*\n",
        'stats_empty': "Belum ada rekod solat. Tekan butang ✅ selepas solat untuk merekod!",
        'pre_notification_set': "Peringatan awal ditetapkan kepada {} minit sebelum waktu solat. ✅",
        'pre_notification_off': "Peringatan awal dimatikan. ✅",
        'select_pre_notification': "Pilih masa peringatan awal sebelum waktu solat:",
        'weekly_not_available': "Maaf, tidak dapat mendapatkan waktu solat mingguan.",
        'monthly_not_available': "Maaf, tidak dapat mendapatkan waktu solat bulanan.",
        'qiblat_need_location': "Sila hantar lokasi anda untuk mendapatkan arah kiblat.",
        'unknown_message': "Maaf, saya tidak memahami mesej anda. Sila gunakan butang yang disediakan.",
        'select_option': "Sila pilih:",
        'select_state': "Sila pilih negeri:",
        'select_zone': "Sila pilih zon untuk {}:",
        'select_setting': "Sila pilih satu pilihan:",
        'invalid_zone': "Maaf, zon yang dipilih tidak sah.",
        'select_language': "Sila pilih bahasa / Please select your language:",
        'countdown_hours_mins': "{h} jam {m} minit",
        'countdown_mins': "{m} minit",
        'prenotify_off': "Matikan",
        'prenotify_min': "{} minit",
        'btn_prayer_times': "📅 Waktu Solat Hari Ini",
        'btn_hadith': "📚 Hadith Harian",
        'btn_doa': "🤲 Doa Harian",
        'btn_qiblat': "🕋 Arah Kiblat",
        'btn_stats': "📊 Statistik Solat",
        'btn_settings': "⚙️ Tetapan",
        'btn_help': "❓ Bantuan",
        'btn_back': "↩️ Menu Utama",
        'btn_send_location': "📍 Hantar Lokasi",
        'btn_select_zone': "🇲🇾 Pilih Zon Malaysia",
        'btn_change_language': "🌐 Tukar Bahasa",
        'btn_pre_notification': "🔔 Peringatan Awal",
        'btn_weekly': "📅 Mingguan",
        'btn_monthly': "📅 Bulanan",
        'btn_donate': "❤️ Derma",
        'donate_message': "Sokong pembangunan SalatTime Bot! 🕌\n\nDerma anda membantu menampung kos server dan pembangunan fitur baru.\n\nPilih jumlah derma:",
        'donate_title': "Derma untuk SalatTime Bot",
        'donate_description': "Sokong pembangunan bot ini. Jazakallahu Khairan!",
        'donate_thanks': "Jazakallahu Khairan! ❤️ Terima kasih atas derma {amount} bintang anda. Semoga Allah membalas kebaikan anda.",
        'donate_star': "{} Bintang",
        'prayer_header_zone': '🕌 *Waktu Solat — {name} ({code}):*',
        'prayer_header_location': '🕌 *Waktu Solat — {name}:*',
        'label_method': '📐 *Kaedah:* {method}',
        'label_school': '📖 *Mazhab:* {school}',
        'label_date': '\n📅 *Tarikh:* {date}',
        'label_timezone': '\n🕰 *Zon Waktu:* {tz}',
        'weekly_title': '📅 *Waktu Solat Mingguan — {title}*',
        'monthly_title': '📅 *Waktu Solat Bulanan — {title}*',
        'monthly_part': '_(Bahagian {part}/{total})_',
    },
    'en': {
        'welcome': "Welcome to the SalatTime Bot! 🕌\nPlease send your location or choose a zone to start.",
        'language_updated': "Language has been updated to English. ✅",
        'location_updated': "Your location has been updated to zone {}. ✅",
        'location_updated_intl': "Your location has been updated to {}. ✅",
        'zone_updated': "Your prayer time zone has been set to {}. ✅",
        'prayer_notification': "It's time for {} prayer. Prayer time: {}",
        'pre_notification': "{minutes} minutes until {prayer} prayer. Please get ready!",
        'next_prayer': "The next prayer is {} at {}",
        'next_prayer_countdown': "The next prayer is *{}* at *{}*\n⏳ *{}* remaining",
        'error_getting_prayer_times': "Sorry, unable to get prayer times for your location.",
        'help_text': (
            "🕌 *SalatTime Bot — Help*\n\n"
            "/start — Start the bot\n"
            "/times — Today's prayer times\n"
            "/next — Next prayer time\n"
            "/weekly — Weekly prayer times\n"
            "/monthly — Monthly prayer times\n"
            "/zone — Select Malaysia zone\n"
            "/qiblat — Qiblat direction\n"
            "/doa — Daily dua\n"
            "/hadith — Daily hadith\n"
            "/stats — Prayer statistics\n"
            "/prenotify — Pre-notification settings\n"
            "/language — Change language\n"
            "/help — Help"
        ),
        'location_not_set': "You haven't set your location or zone yet. Please send your location or choose a zone.",
        'location_out_of_malaysia': "Sorry, the location you sent is outside Malaysia. Please choose a zone manually.",
        'prayer_logged': "{} prayer has been logged. Alhamdulillah! ✅",
        'prayer_already_logged': "{} prayer has already been logged for today.",
        'stats_header': "📊 *Your Prayer Statistics*\n",
        'stats_streak': "🔥 *Current streak:* {} consecutive days (5/5 prayers)\n",
        'stats_total': "📈 *Total prayers logged:* {}\n",
        'stats_week': "📅 *This week:* {} prayers\n",
        'stats_month': "🗓 *This month:* {} prayers\n",
        'stats_today': "\n*Today's prayers:*\n",
        'stats_empty': "No prayer records yet. Tap the ✅ button after praying to record!",
        'pre_notification_set': "Pre-notification set to {} minutes before prayer time. ✅",
        'pre_notification_off': "Pre-notification has been turned off. ✅",
        'select_pre_notification': "Select pre-notification time before prayer:",
        'weekly_not_available': "Sorry, unable to get weekly prayer times.",
        'monthly_not_available': "Sorry, unable to get monthly prayer times.",
        'qiblat_need_location': "Please send your location to get the Qiblat direction.",
        'unknown_message': "Sorry, I don't understand your message. Please use the provided buttons.",
        'select_option': "Please choose:",
        'select_state': "Please select a state:",
        'select_zone': "Please select a zone for {}:",
        'select_setting': "Please select an option:",
        'invalid_zone': "Sorry, the selected zone is invalid.",
        'select_language': "Please select your language / Sila pilih bahasa:",
        'countdown_hours_mins': "{h}h {m}min",
        'countdown_mins': "{m} min",
        'prenotify_off': "Off",
        'prenotify_min': "{} min",
        'btn_prayer_times': "📅 Prayer Times",
        'btn_hadith': "📚 Daily Hadith",
        'btn_doa': "🤲 Daily Dua",
        'btn_qiblat': "🕋 Qiblat",
        'btn_stats': "📊 Prayer Stats",
        'btn_settings': "⚙️ Settings",
        'btn_help': "❓ Help",
        'btn_back': "↩️ Main Menu",
        'btn_send_location': "📍 Send Location",
        'btn_select_zone': "🇲🇾 Select Malaysia Zone",
        'btn_change_language': "🌐 Change Language",
        'btn_pre_notification': "🔔 Pre-notification",
        'btn_weekly': "📅 Weekly",
        'btn_monthly': "📅 Monthly",
        'btn_donate': "❤️ Donate",
        'donate_message': "Support the SalatTime Bot! 🕌\n\nYour donation helps cover server costs and development of new features.\n\nChoose a donation amount:",
        'donate_title': "Donate to SalatTime Bot",
        'donate_description': "Support the development of this bot. Jazakallahu Khairan!",
        'donate_thanks': "Jazakallahu Khairan! ❤️ Thank you for your donation of {amount} stars. May Allah reward your generosity.",
        'donate_star': "{} Stars",
        'prayer_header_zone': '🕌 *Prayer Times — {name} ({code}):*',
        'prayer_header_location': '🕌 *Prayer Times — {name}:*',
        'label_method': '📐 *Method:* {method}',
        'label_school': '📖 *School:* {school}',
        'label_date': '\n📅 *Date:* {date}',
        'label_timezone': '\n🕰 *Timezone:* {tz}',
        'weekly_title': '📅 *Weekly Prayer Times — {title}*',
        'monthly_title': '📅 *Monthly Prayer Times — {title}*',
        'monthly_part': '_(Part {part}/{total})_',
    },
    'ar': {
        'welcome': "مرحباً بك في SalatTime Bot! 🕌\nأرسل موقعك أو اختر منطقة للبدء.",
        'language_updated': "تم تحديث اللغة إلى العربية. ✅",
        'location_updated': "تم تحديث موقعك إلى منطقة {}. ✅",
        'location_updated_intl': "تم تحديث موقعك إلى {}. ✅",
        'zone_updated': "تم تحديد منطقة أوقات الصلاة إلى {}. ✅",
        'prayer_notification': "حان وقت صلاة {}. الوقت: {}",
        'pre_notification': "بقي {minutes} دقيقة على صلاة {prayer}. استعد!",
        'next_prayer': "الصلاة التالية هي {} في {}",
        'next_prayer_countdown': "الصلاة التالية *{}* في *{}*\n⏳ متبقي *{}*",
        'error_getting_prayer_times': "عذراً، لا يمكن الحصول على أوقات الصلاة لموقعك.",
        'help_text': (
            "🕌 *SalatTime Bot — المساعدة*\n\n"
            "/start — بدء البوت\n"
            "/times — أوقات صلاة اليوم\n"
            "/next — وقت الصلاة التالي\n"
            "/weekly — أوقات الصلاة الأسبوعية\n"
            "/monthly — أوقات الصلاة الشهرية\n"
            "/zone — اختيار منطقة ماليزيا\n"
            "/qiblat — اتجاه القبلة\n"
            "/doa — دعاء اليوم\n"
            "/hadith — حديث اليوم\n"
            "/stats — إحصائيات الصلاة\n"
            "/prenotify — إعدادات التنبيه المسبق\n"
            "/language — تغيير اللغة\n"
            "/help — المساعدة"
        ),
        'location_not_set': "لم تقم بتحديد موقعك أو منطقتك بعد. أرسل موقعك أو اختر منطقة.",
        'location_out_of_malaysia': "عذراً، الموقع خارج ماليزيا. اختر منطقة يدوياً.",
        'prayer_logged': "تم تسجيل صلاة {}. الحمد لله! ✅",
        'prayer_already_logged': "صلاة {} مسجلة بالفعل لهذا اليوم.",
        'stats_header': "📊 *إحصائيات صلاتك*\n",
        'stats_streak': "🔥 *السلسلة الحالية:* {} أيام متتالية (5/5 صلوات)\n",
        'stats_total': "📈 *إجمالي الصلوات المسجلة:* {}\n",
        'stats_week': "📅 *هذا الأسبوع:* {} صلاة\n",
        'stats_month': "🗓 *هذا الشهر:* {} صلاة\n",
        'stats_today': "\n*صلوات اليوم:*\n",
        'stats_empty': "لا توجد سجلات صلاة بعد. اضغط زر ✅ بعد الصلاة للتسجيل!",
        'pre_notification_set': "تم تحديد التنبيه المسبق {} دقيقة قبل وقت الصلاة. ✅",
        'pre_notification_off': "تم إيقاف التنبيه المسبق. ✅",
        'select_pre_notification': "اختر وقت التنبيه المسبق قبل الصلاة:",
        'weekly_not_available': "عذراً، لا يمكن الحصول على أوقات الصلاة الأسبوعية.",
        'monthly_not_available': "عذراً، لا يمكن الحصول على أوقات الصلاة الشهرية.",
        'qiblat_need_location': "أرسل موقعك للحصول على اتجاه القبلة.",
        'unknown_message': "عذراً، لم أفهم رسالتك. استخدم الأزرار المتاحة.",
        'select_option': "اختر:",
        'select_state': "اختر الولاية:",
        'select_zone': "اختر المنطقة لـ {}:",
        'select_setting': "اختر:",
        'invalid_zone': "عذراً، المنطقة المختارة غير صالحة.",
        'select_language': "اختر لغتك / Select your language:",
        'countdown_hours_mins': "{h} ساعة {m} دقيقة",
        'countdown_mins': "{m} دقيقة",
        'prenotify_off': "إيقاف",
        'prenotify_min': "{} دقيقة",
        'btn_prayer_times': "📅 أوقات الصلاة",
        'btn_hadith': "📚 حديث اليوم",
        'btn_doa': "🤲 دعاء اليوم",
        'btn_qiblat': "🕋 القبلة",
        'btn_stats': "📊 الإحصائيات",
        'btn_settings': "⚙️ الإعدادات",
        'btn_help': "❓ المساعدة",
        'btn_back': "↩️ القائمة الرئيسية",
        'btn_send_location': "📍 إرسال الموقع",
        'btn_select_zone': "🇲🇾 اختيار منطقة ماليزيا",
        'btn_change_language': "🌐 تغيير اللغة",
        'btn_pre_notification': "🔔 تنبيه مسبق",
        'btn_weekly': "📅 أسبوعي",
        'btn_monthly': "📅 شهري",
        'btn_donate': "❤️ تبرع",
        'donate_message': "ادعم SalatTime Bot! 🕌\n\nتبرعك يساعد في تغطية تكاليف الخادم وتطوير ميزات جديدة.\n\nاختر مبلغ التبرع:",
        'donate_title': "تبرع لSalatTime Bot",
        'donate_description': "ادعم تطوير هذا البوت. جزاك الله خيراً!",
        'donate_thanks': "جزاك الله خيراً! ❤️ شكراً لتبرعك بـ {amount} نجمة. جعله الله في ميزان حسناتك.",
        'donate_star': "{} نجمة",
        'prayer_header_zone': '🕌 *مواقيت الصلاة — {name} ({code}):*',
        'prayer_header_location': '🕌 *مواقيت الصلاة — {name}:*',
        'label_method': '📐 *الطريقة:* {method}',
        'label_school': '📖 *المذهب:* {school}',
        'label_date': '\n📅 *التاريخ:* {date}',
        'label_timezone': '\n🕰 *المنطقة الزمنية:* {tz}',
        'weekly_title': '📅 *مواقيت الصلاة الأسبوعية — {title}*',
        'monthly_title': '📅 *مواقيت الصلاة الشهرية — {title}*',
        'monthly_part': '_(الجزء {part}/{total})_',
    },
    'tr': {
        'welcome': "SalatTime Bot'a hoş geldiniz! 🕌\nKonumunuzu gönderin veya başlamak için bir bölge seçin.",
        'language_updated': "Dil Türkçe olarak güncellendi. ✅",
        'location_updated': "Konumunuz {} bölgesine güncellendi. ✅",
        'location_updated_intl': "Konumunuz {} olarak güncellendi. ✅",
        'zone_updated': "Namaz vakti bölgeniz {} olarak ayarlandı. ✅",
        'prayer_notification': "{} namazı vakti geldi. Namaz vakti: {}",
        'pre_notification': "{prayer} namazına {minutes} dakika kaldı. Hazırlanın!",
        'next_prayer': "Sıradaki namaz {} saat {}",
        'next_prayer_countdown': "Sıradaki namaz *{}* saat *{}*\n⏳ *{}* kaldı",
        'error_getting_prayer_times': "Üzgünüz, konumunuz için namaz vakitleri alınamadı.",
        'help_text': (
            "🕌 *SalatTime Bot — Yardım*\n\n"
            "/start — Botu başlat\n"
            "/times — Bugünün namaz vakitleri\n"
            "/next — Sıradaki namaz vakti\n"
            "/weekly — Haftalık namaz vakitleri\n"
            "/monthly — Aylık namaz vakitleri\n"
            "/zone — Malezya bölgesi seç\n"
            "/qiblat — Kıble yönü\n"
            "/doa — Günün duası\n"
            "/hadith — Günün hadisi\n"
            "/stats — Namaz istatistikleri\n"
            "/prenotify — Ön bildirim ayarları\n"
            "/language — Dil değiştir\n"
            "/help — Yardım"
        ),
        'location_not_set': "Henüz konum veya bölge ayarlamadınız. Konumunuzu gönderin veya bir bölge seçin.",
        'location_out_of_malaysia': "Üzgünüz, konum Malezya dışında. Manuel olarak bölge seçin.",
        'prayer_logged': "{} namazı kaydedildi. Elhamdülillah! ✅",
        'prayer_already_logged': "{} namazı bugün için zaten kaydedilmiş.",
        'stats_header': "📊 *Namaz İstatistikleriniz*\n",
        'stats_streak': "🔥 *Mevcut seri:* {} gün üst üste (5/5 namaz)\n",
        'stats_total': "📈 *Toplam kaydedilen namaz:* {}\n",
        'stats_week': "📅 *Bu hafta:* {} namaz\n",
        'stats_month': "🗓 *Bu ay:* {} namaz\n",
        'stats_today': "\n*Bugünün namazları:*\n",
        'stats_empty': "Henüz namaz kaydı yok. Namazdan sonra ✅ düğmesine basarak kaydedin!",
        'pre_notification_set': "Ön bildirim namaz vaktinden {} dakika önce olarak ayarlandı. ✅",
        'pre_notification_off': "Ön bildirim kapatıldı. ✅",
        'select_pre_notification': "Namaz öncesi ön bildirim süresini seçin:",
        'weekly_not_available': "Üzgünüz, haftalık namaz vakitleri alınamadı.",
        'monthly_not_available': "Üzgünüz, aylık namaz vakitleri alınamadı.",
        'qiblat_need_location': "Kıble yönünü öğrenmek için konumunuzu gönderin.",
        'unknown_message': "Üzgünüz, mesajınızı anlamadım. Lütfen mevcut düğmeleri kullanın.",
        'select_option': "Seçiniz:",
        'select_state': "Eyalet seçin:",
        'select_zone': "{} için bölge seçin:",
        'select_setting': "Bir seçenek belirleyin:",
        'invalid_zone': "Üzgünüz, seçilen bölge geçersiz.",
        'select_language': "Dilinizi seçin / Select your language:",
        'countdown_hours_mins': "{h} saat {m} dakika",
        'countdown_mins': "{m} dakika",
        'prenotify_off': "Kapat",
        'prenotify_min': "{} dk",
        'btn_prayer_times': "📅 Namaz Vakitleri",
        'btn_hadith': "📚 Günün Hadisi",
        'btn_doa': "🤲 Günün Duası",
        'btn_qiblat': "🕋 Kıble",
        'btn_stats': "📊 İstatistikler",
        'btn_settings': "⚙️ Ayarlar",
        'btn_help': "❓ Yardım",
        'btn_back': "↩️ Ana Menü",
        'btn_send_location': "📍 Konum Gönder",
        'btn_select_zone': "🇲🇾 Malezya Bölgesi Seç",
        'btn_change_language': "🌐 Dil Değiştir",
        'btn_pre_notification': "🔔 Ön Bildirim",
        'btn_weekly': "📅 Haftalık",
        'btn_monthly': "📅 Aylık",
        'btn_donate': "❤️ Bağış",
        'donate_message': "SalatTime Bot'u destekleyin! 🕌\n\nBağışınız sunucu maliyetlerini ve yeni özellik geliştirmesini destekler.\n\nBağış miktarını seçin:",
        'donate_title': "SalatTime Bot'a Bağış",
        'donate_description': "Bu botun geliştirilmesini destekleyin. Allah razı olsun!",
        'donate_thanks': "Allah razı olsun! ❤️ {amount} yıldız bağışınız için teşekkürler. Allah iyiliğinizi kabul etsin.",
        'donate_star': "{} Yıldız",
        'prayer_header_zone': '🕌 *Namaz Vakitleri — {name} ({code}):*',
        'prayer_header_location': '🕌 *Namaz Vakitleri — {name}:*',
        'label_method': '📐 *Hesaplama:* {method}',
        'label_school': '📖 *Mezhep:* {school}',
        'label_date': '\n📅 *Tarih:* {date}',
        'label_timezone': '\n🕰 *Saat Dilimi:* {tz}',
        'weekly_title': '📅 *Haftalık Namaz Vakitleri — {title}*',
        'monthly_title': '📅 *Aylık Namaz Vakitleri — {title}*',
        'monthly_part': '_(Bölüm {part}/{total})_',
    },
    'ur': {
        'welcome': "SalatTime Bot میں خوش آمدید! 🕌\nشروع کرنے کے لیے اپنا مقام بھیجیں یا زون منتخب کریں۔",
        'language_updated': "زبان اردو میں تبدیل کر دی گئی۔ ✅",
        'location_updated': "آپ کا مقام زون {} میں اپ ڈیٹ کر دیا گیا۔ ✅",
        'location_updated_intl': "آپ کا مقام {} میں اپ ڈیٹ کر دیا گیا۔ ✅",
        'zone_updated': "آپ کا نماز کے اوقات کا زون {} مقرر کر دیا گیا۔ ✅",
        'prayer_notification': "نماز {} کا وقت ہو گیا ہے۔ وقت: {}",
        'pre_notification': "نماز {prayer} میں {minutes} منٹ باقی ہیں۔ تیار ہو جائیں!",
        'next_prayer': "اگلی نماز {} وقت {} پر ہے",
        'next_prayer_countdown': "اگلی نماز *{}* وقت *{}* پر ہے\n⏳ *{}* باقی",
        'error_getting_prayer_times': "معذرت، آپ کے مقام کے لیے نماز کے اوقات حاصل نہیں ہو سکے۔",
        'help_text': (
            "🕌 *SalatTime Bot — مدد*\n\n"
            "/start — بوٹ شروع کریں\n"
            "/times — آج کے نماز کے اوقات\n"
            "/next — اگلی نماز کا وقت\n"
            "/weekly — ہفتہ وار نماز کے اوقات\n"
            "/monthly — ماہانہ نماز کے اوقات\n"
            "/zone — ملائیشیا زون منتخب کریں\n"
            "/qiblat — قبلہ کی سمت\n"
            "/doa — آج کی دعا\n"
            "/hadith — آج کی حدیث\n"
            "/stats — نماز کے اعداد و شمار\n"
            "/prenotify — پیشگی اطلاع کی ترتیبات\n"
            "/language — زبان تبدیل کریں\n"
            "/help — مدد"
        ),
        'location_not_set': "آپ نے ابھی تک اپنا مقام یا زون مقرر نہیں کیا۔ اپنا مقام بھیجیں یا زون منتخب کریں۔",
        'location_out_of_malaysia': "معذرت، یہ مقام ملائیشیا سے باہر ہے۔ دستی طور پر زون منتخب کریں۔",
        'prayer_logged': "نماز {} ریکارڈ ہو گئی۔ الحمد للہ! ✅",
        'prayer_already_logged': "نماز {} آج کے لیے پہلے سے ریکارڈ ہے۔",
        'stats_header': "📊 *آپ کے نماز کے اعداد و شمار*\n",
        'stats_streak': "🔥 *موجودہ سلسلہ:* {} مسلسل دن (5/5 نمازیں)\n",
        'stats_total': "📈 *کل ریکارڈ شدہ نمازیں:* {}\n",
        'stats_week': "📅 *اس ہفتے:* {} نمازیں\n",
        'stats_month': "🗓 *اس مہینے:* {} نمازیں\n",
        'stats_today': "\n*آج کی نمازیں:*\n",
        'stats_empty': "ابھی تک کوئی نماز ریکارڈ نہیں۔ نماز کے بعد ✅ بٹن دبائیں!",
        'pre_notification_set': "پیشگی اطلاع نماز سے {} منٹ پہلے مقرر کر دی گئی۔ ✅",
        'pre_notification_off': "پیشگی اطلاع بند کر دی گئی۔ ✅",
        'select_pre_notification': "نماز سے پہلے پیشگی اطلاع کا وقت منتخب کریں:",
        'weekly_not_available': "معذرت، ہفتہ وار نماز کے اوقات دستیاب نہیں۔",
        'monthly_not_available': "معذرت، ماہانہ نماز کے اوقات دستیاب نہیں۔",
        'qiblat_need_location': "قبلہ کی سمت جاننے کے لیے اپنا مقام بھیجیں۔",
        'unknown_message': "معذرت، میں آپ کا پیغام سمجھ نہیں سکا۔ دستیاب بٹن استعمال کریں۔",
        'select_option': "منتخب کریں:",
        'select_state': "ریاست منتخب کریں:",
        'select_zone': "{} کے لیے زون منتخب کریں:",
        'select_setting': "ایک آپشن منتخب کریں:",
        'invalid_zone': "معذرت، منتخب زون درست نہیں ہے۔",
        'select_language': "اپنی زبان منتخب کریں / Select your language:",
        'countdown_hours_mins': "{h} گھنٹے {m} منٹ",
        'countdown_mins': "{m} منٹ",
        'prenotify_off': "بند",
        'prenotify_min': "{} منٹ",
        'btn_prayer_times': "📅 نماز کے اوقات",
        'btn_hadith': "📚 آج کی حدیث",
        'btn_doa': "🤲 آج کی دعا",
        'btn_qiblat': "🕋 قبلہ",
        'btn_stats': "📊 اعداد و شمار",
        'btn_settings': "⚙️ ترتیبات",
        'btn_help': "❓ مدد",
        'btn_back': "↩️ مرکزی مینو",
        'btn_send_location': "📍 مقام بھیجیں",
        'btn_select_zone': "🇲🇾 ملائیشیا زون",
        'btn_change_language': "🌐 زبان تبدیل کریں",
        'btn_pre_notification': "🔔 پیشگی اطلاع",
        'btn_weekly': "📅 ہفتہ وار",
        'btn_monthly': "📅 ماہانہ",
        'btn_donate': "❤️ عطیہ",
        'donate_message': "SalatTime Bot کی مدد کریں! 🕌\n\nآپ کا عطیہ سرور کے اخراجات اور نئی خصوصیات کی ترقی میں مدد کرتا ہے۔\n\nعطیہ کی رقم منتخب کریں:",
        'donate_title': "SalatTime Bot کے لیے عطیہ",
        'donate_description': "اس بوٹ کی ترقی میں مدد کریں۔ جزاک اللہ خیراً!",
        'donate_thanks': "جزاک اللہ خیراً! ❤️ آپ کے {amount} ستاروں کے عطیہ کا شکریہ۔ اللہ آپ کی سخاوت کو قبول فرمائے۔",
        'donate_star': "{} ستارے",
        'prayer_header_zone': '🕌 *نماز کے اوقات — {name} ({code}):*',
        'prayer_header_location': '🕌 *نماز کے اوقات — {name}:*',
        'label_method': '📐 *طریقہ:* {method}',
        'label_school': '📖 *مذہب:* {school}',
        'label_date': '\n📅 *تاریخ:* {date}',
        'label_timezone': '\n🕰 *ٹائم زون:* {tz}',
        'weekly_title': '📅 *ہفتہ وار نماز کے اوقات — {title}*',
        'monthly_title': '📅 *ماہانہ نماز کے اوقات — {title}*',
        'monthly_part': '_(حصہ {part}/{total})_',
    },
    'id': {
        'welcome': "Selamat datang di SalatTime Bot! 🕌\nSilakan kirim lokasi Anda atau pilih zona untuk memulai.",
        'language_updated': "Bahasa telah diperbarui ke Bahasa Indonesia. ✅",
        'location_updated': "Lokasi Anda telah diperbarui ke zona {}. ✅",
        'location_updated_intl': "Lokasi Anda telah diperbarui ke {}. ✅",
        'zone_updated': "Zona waktu sholat Anda telah diatur ke {}. ✅",
        'prayer_notification': "Waktu sholat {} telah tiba. Waktu sholat: {}",
        'pre_notification': "{minutes} menit lagi waktu sholat {prayer}. Silakan bersiap!",
        'next_prayer': "Waktu sholat berikutnya adalah {} pada {}",
        'next_prayer_countdown': "Waktu sholat berikutnya *{}* pada *{}*\n⏳ *{}* lagi",
        'error_getting_prayer_times': "Maaf, tidak dapat mendapatkan waktu sholat untuk lokasi Anda.",
        'help_text': (
            "🕌 *SalatTime Bot — Bantuan*\n\n"
            "/start — Mulai bot\n"
            "/times — Waktu sholat hari ini\n"
            "/next — Waktu sholat berikutnya\n"
            "/weekly — Waktu sholat mingguan\n"
            "/monthly — Waktu sholat bulanan\n"
            "/zone — Pilih zona Malaysia\n"
            "/qiblat — Arah kiblat\n"
            "/doa — Doa harian\n"
            "/hadith — Hadits harian\n"
            "/stats — Statistik sholat\n"
            "/prenotify — Pengaturan pra-notifikasi\n"
            "/language — Ubah bahasa\n"
            "/help — Bantuan"
        ),
        'location_not_set': "Anda belum mengatur lokasi atau zona. Silakan kirim lokasi atau pilih zona.",
        'location_out_of_malaysia': "Maaf, lokasi di luar Malaysia. Silakan pilih zona secara manual.",
        'prayer_logged': "Sholat {} telah dicatat. Alhamdulillah! ✅",
        'prayer_already_logged': "Sholat {} sudah dicatat untuk hari ini.",
        'stats_header': "📊 *Statistik Sholat Anda*\n",
        'stats_streak': "🔥 *Streak saat ini:* {} hari berturut-turut (5/5 sholat)\n",
        'stats_total': "📈 *Total sholat tercatat:* {}\n",
        'stats_week': "📅 *Minggu ini:* {} sholat\n",
        'stats_month': "🗓 *Bulan ini:* {} sholat\n",
        'stats_today': "\n*Sholat hari ini:*\n",
        'stats_empty': "Belum ada catatan sholat. Tekan tombol ✅ setelah sholat untuk mencatat!",
        'pre_notification_set': "Pra-notifikasi diatur {} menit sebelum waktu sholat. ✅",
        'pre_notification_off': "Pra-notifikasi dimatikan. ✅",
        'select_pre_notification': "Pilih waktu pra-notifikasi sebelum sholat:",
        'weekly_not_available': "Maaf, tidak dapat mendapatkan waktu sholat mingguan.",
        'monthly_not_available': "Maaf, tidak dapat mendapatkan waktu sholat bulanan.",
        'qiblat_need_location': "Silakan kirim lokasi untuk mendapatkan arah kiblat.",
        'unknown_message': "Maaf, saya tidak mengerti pesan Anda. Gunakan tombol yang tersedia.",
        'select_option': "Silakan pilih:",
        'select_state': "Pilih negara bagian:",
        'select_zone': "Pilih zona untuk {}:",
        'select_setting': "Pilih opsi:",
        'invalid_zone': "Maaf, zona yang dipilih tidak valid.",
        'select_language': "Pilih bahasa Anda / Select your language:",
        'countdown_hours_mins': "{h} jam {m} menit",
        'countdown_mins': "{m} menit",
        'prenotify_off': "Matikan",
        'prenotify_min': "{} menit",
        'btn_prayer_times': "📅 Waktu Sholat",
        'btn_hadith': "📚 Hadits Harian",
        'btn_doa': "🤲 Doa Harian",
        'btn_qiblat': "🕋 Kiblat",
        'btn_stats': "📊 Statistik",
        'btn_settings': "⚙️ Pengaturan",
        'btn_help': "❓ Bantuan",
        'btn_back': "↩️ Menu Utama",
        'btn_send_location': "📍 Kirim Lokasi",
        'btn_select_zone': "🇲🇾 Pilih Zona Malaysia",
        'btn_change_language': "🌐 Ubah Bahasa",
        'btn_pre_notification': "🔔 Pra-notifikasi",
        'btn_weekly': "📅 Mingguan",
        'btn_monthly': "📅 Bulanan",
        'btn_donate': "❤️ Donasi",
        'donate_message': "Dukung SalatTime Bot! 🕌\n\nDonasi Anda membantu menutupi biaya server dan pengembangan fitur baru.\n\nPilih jumlah donasi:",
        'donate_title': "Donasi untuk SalatTime Bot",
        'donate_description': "Dukung pengembangan bot ini. Jazakallahu Khairan!",
        'donate_thanks': "Jazakallahu Khairan! ❤️ Terima kasih atas donasi {amount} bintang Anda. Semoga Allah membalas kebaikan Anda.",
        'donate_star': "{} Bintang",
        'prayer_header_zone': '🕌 *Waktu Sholat — {name} ({code}):*',
        'prayer_header_location': '🕌 *Waktu Sholat — {name}:*',
        'label_method': '📐 *Metode:* {method}',
        'label_school': '📖 *Mazhab:* {school}',
        'label_date': '\n📅 *Tanggal:* {date}',
        'label_timezone': '\n🕰 *Zona Waktu:* {tz}',
        'weekly_title': '📅 *Waktu Sholat Mingguan — {title}*',
        'monthly_title': '📅 *Waktu Sholat Bulanan — {title}*',
        'monthly_part': '_(Bagian {part}/{total})_',
    },
    'fr': {
        'welcome': "Bienvenue sur SalatTime Bot ! 🕌\nEnvoyez votre position ou choisissez une zone pour commencer.",
        'language_updated': "La langue a été mise à jour en français. ✅",
        'location_updated': "Votre position a été mise à jour vers la zone {}. ✅",
        'location_updated_intl': "Votre position a été mise à jour vers {}. ✅",
        'zone_updated': "Votre zone d'horaires de prière a été définie à {}. ✅",
        'prayer_notification': "C'est l'heure de la prière {}. Heure: {}",
        'pre_notification': "Encore {minutes} minutes avant la prière {prayer}. Préparez-vous !",
        'next_prayer': "La prochaine prière est {} à {}",
        'next_prayer_countdown': "La prochaine prière est *{}* à *{}*\n⏳ *{}* restantes",
        'error_getting_prayer_times': "Désolé, impossible d'obtenir les horaires de prière pour votre position.",
        'help_text': (
            "🕌 *SalatTime Bot — Aide*\n\n"
            "/start — Démarrer le bot\n"
            "/times — Horaires de prière du jour\n"
            "/next — Prochaine prière\n"
            "/weekly — Horaires hebdomadaires\n"
            "/monthly — Horaires mensuels\n"
            "/zone — Choisir une zone Malaisie\n"
            "/qiblat — Direction de la Qibla\n"
            "/doa — Doua du jour\n"
            "/hadith — Hadith du jour\n"
            "/stats — Statistiques de prière\n"
            "/prenotify — Paramètres de pré-notification\n"
            "/language — Changer la langue\n"
            "/help — Aide"
        ),
        'location_not_set': "Vous n'avez pas encore défini votre position ou zone. Envoyez votre position ou choisissez une zone.",
        'location_out_of_malaysia': "Désolé, la position est hors de Malaisie. Choisissez une zone manuellement.",
        'prayer_logged': "Prière {} enregistrée. Alhamdulillah ! ✅",
        'prayer_already_logged': "La prière {} est déjà enregistrée pour aujourd'hui.",
        'stats_header': "📊 *Vos Statistiques de Prière*\n",
        'stats_streak': "🔥 *Série en cours :* {} jours consécutifs (5/5 prières)\n",
        'stats_total': "📈 *Total des prières enregistrées :* {}\n",
        'stats_week': "📅 *Cette semaine :* {} prières\n",
        'stats_month': "🗓 *Ce mois :* {} prières\n",
        'stats_today': "\n*Prières d'aujourd'hui :*\n",
        'stats_empty': "Aucun enregistrement de prière. Appuyez sur ✅ après la prière pour enregistrer !",
        'pre_notification_set': "Pré-notification définie à {} minutes avant la prière. ✅",
        'pre_notification_off': "Pré-notification désactivée. ✅",
        'select_pre_notification': "Sélectionnez le temps de pré-notification avant la prière :",
        'weekly_not_available': "Désolé, impossible d'obtenir les horaires hebdomadaires.",
        'monthly_not_available': "Désolé, impossible d'obtenir les horaires mensuels.",
        'qiblat_need_location': "Envoyez votre position pour obtenir la direction de la Qibla.",
        'unknown_message': "Désolé, je ne comprends pas votre message. Utilisez les boutons disponibles.",
        'select_option': "Choisissez :",
        'select_state': "Sélectionnez un état :",
        'select_zone': "Sélectionnez une zone pour {} :",
        'select_setting': "Sélectionnez une option :",
        'invalid_zone': "Désolé, la zone sélectionnée est invalide.",
        'select_language': "Choisissez votre langue / Select your language :",
        'countdown_hours_mins': "{h}h {m}min",
        'countdown_mins': "{m} min",
        'prenotify_off': "Désactiver",
        'prenotify_min': "{} min",
        'btn_prayer_times': "📅 Horaires de Prière",
        'btn_hadith': "📚 Hadith du Jour",
        'btn_doa': "🤲 Doua du Jour",
        'btn_qiblat': "🕋 Qibla",
        'btn_stats': "📊 Statistiques",
        'btn_settings': "⚙️ Paramètres",
        'btn_help': "❓ Aide",
        'btn_back': "↩️ Menu Principal",
        'btn_send_location': "📍 Envoyer Position",
        'btn_select_zone': "🇲🇾 Zone Malaisie",
        'btn_change_language': "🌐 Changer Langue",
        'btn_pre_notification': "🔔 Pré-notification",
        'btn_weekly': "📅 Hebdomadaire",
        'btn_monthly': "📅 Mensuel",
        'btn_donate': "❤️ Don",
        'donate_message': "Soutenez SalatTime Bot ! 🕌\n\nVotre don aide à couvrir les coûts du serveur et le développement de nouvelles fonctionnalités.\n\nChoisissez un montant :",
        'donate_title': "Don pour SalatTime Bot",
        'donate_description': "Soutenez le développement de ce bot. Jazakallahu Khairan !",
        'donate_thanks': "Jazakallahu Khairan ! ❤️ Merci pour votre don de {amount} étoiles. Qu'Allah récompense votre générosité.",
        'donate_star': "{} Étoiles",
        'prayer_header_zone': '🕌 *Horaires de Prière — {name} ({code}) :*',
        'prayer_header_location': '🕌 *Horaires de Prière — {name} :*',
        'label_method': '📐 *Méthode :* {method}',
        'label_school': '📖 *École :* {school}',
        'label_date': '\n📅 *Date :* {date}',
        'label_timezone': '\n🕰 *Fuseau horaire :* {tz}',
        'weekly_title': '📅 *Horaires Hebdomadaires — {title}*',
        'monthly_title': '📅 *Horaires Mensuels — {title}*',
        'monthly_part': '_(Partie {part}/{total})_',
    },
}


def get_translation(lang, key):
    return translations.get(lang, translations['en']).get(key, translations['en'].get(key, f"[{key}]"))


def get_all_texts_for_key(key):
    texts = set()
    for lang_translations in translations.values():
        val = lang_translations.get(key)
        if val:
            texts.add(val)
    return texts


def detect_language(telegram_lang_code):
    if not telegram_lang_code:
        return 'en'
    code = telegram_lang_code.lower()
    if code in TELEGRAM_LANG_MAP:
        return TELEGRAM_LANG_MAP[code]
    short = code.split('-')[0]
    if short in TELEGRAM_LANG_MAP:
        return TELEGRAM_LANG_MAP[short]
    return 'en'
