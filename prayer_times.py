import requests
from datetime import datetime, timedelta, timezone
import schedule
import time
from database import get_db_connection
from translations import get_translation
from datetime import datetime
from pytz import timezone
from datetime import datetime  # Pastikan ini sudah diimport

# Zon-zon Malaysia
MALAYSIA_ZONES = {
    'Johor': {
        'JHR01': 'Pulau Aur dan Pulau Pemanggil',
        'JHR02': 'Johor Bharu, Kota Tinggi, Mersing',
        'JHR03': 'Kluang, Pontian',
        'JHR04': 'Batu Pahat, Muar, Segamat, Gemas Johor'
    },
    'Kedah': {
        'KDH01': 'Kota Setar, Kubang Pasu, Pokok Sena (Daerah Kecil)',
        'KDH02': 'Kuala Muda, Yan, Pendang',
        'KDH03': 'Padang Terap, Sik',
        'KDH04': 'Baling',
        'KDH05': 'Bandar Baharu, Kulim',
        'KDH06': 'Langkawi',
        'KDH07': 'Gunung Jerai'
    },
    'Kelantan': {
        'KTN01': 'Bachok, Kota Bharu, Machang, Pasir Mas, Pasir Puteh, Tanah Merah, Tumpat, Kuala Krai, Mukim Chiku',
        'KTN03': 'Gua Musang (Daerah Galas Dan Bertam), Jeli'
    },
    'Melaka': {
        'MLK01': 'SELURUH NEGERI MELAKA'
    },
    'Negeri Sembilan': {
        'NGS01': 'Tampin, Jempol',
        'NGS02': 'Jelebu, Kuala Pilah, Port Dickson, Rembau, Seremban'
    },
    'Pahang': {
        'PHG01': 'Pulau Tioman',
        'PHG02': 'Kuantan, Pekan, Rompin, Muadzam Shah',
        'PHG03': 'Jerantut, Temerloh, Maran, Bera, Chenor, Jengka',
        'PHG04': 'Bentong, Lipis, Raub',
        'PHG05': 'Genting Sempah, Janda Baik, Bukit Tinggi',
        'PHG06': 'Cameron Highlands, Genting Higlands, Bukit Fraser'
    },
    'Perlis': {
        'PLS01': 'Kangar, Padang Besar, Arau'
    },
    'Pulau Pinang': {
        'PNG01': 'Seluruh Negeri Pulau Pinang'
    },
    'Perak': {
        'PRK01': 'Tapah, Slim River, Tanjung Malim',
        'PRK02': 'Kuala Kangsar, Sg. Siput (Daerah Kecil), Ipoh, Batu Gajah, Kampar',
        'PRK03': 'Lenggong, Pengkalan Hulu, Grik',
        'PRK04': 'Temengor, Belum',
        'PRK05': 'Kg Gajah, Teluk Intan, Bagan Datuk, Seri Iskandar, Beruas, Parit, Lumut, Sitiawan, Pulau Pangkor',
        'PRK06': 'Selama, Taiping, Bagan Serai, Parit Buntar',
        'PRK07': 'Bukit Larut'
    },
    'Sabah': {
        'SBH01': 'Bahagian Sandakan (Timur), Bukit Garam, Semawang, Temanggong, Tambisan, Bandar Sandakan',
        'SBH02': 'Beluran, Telupid, Pinangah, Terusan, Kuamut, Bahagian Sandakan (Barat)',
        'SBH03': 'Lahad Datu, Silabukan, Kunak, Sahabat, Semporna, Tungku, Bahagian Tawau (Timur)',
        'SBH04': 'Bandar Tawau, Balong, Merotai, Kalabakan, Bahagian Tawau (Barat)',
        'SBH05': 'Kudat, Kota Marudu, Pitas, Pulau Banggi, Bahagian Kudat',
        'SBH06': 'Gunung Kinabalu',
        'SBH07': 'Kota Kinabalu, Ranau, Kota Belud, Tuaran, Penampang, Papar, Putatan, Bahagian Pantai Barat',
        'SBH08': 'Pensiangan, Keningau, Tambunan, Nabawan, Bahagian Pendalaman (Atas)',
        'SBH09': 'Beaufort, Kuala Penyu, Sipitang, Tenom, Long Pa Sia, Membakut, Weston, Bahagian Pendalaman (Bawah)'
    },
    'Selangor': {
        'SGR01': 'Gombak, Petaling, Sepang, Hulu Langat, Hulu Selangor, Rawang, S.Alam',
        'SGR02': 'Kuala Selangor, Sabak Bernam',
        'SGR03': 'Klang, Kuala Langat'
    },
    'Sarawak': {
        'SWK01': 'Limbang, Lawas, Sundar, Trusan',
        'SWK02': 'Miri, Niah, Bekenu, Sibuti, Marudi',
        'SWK03': 'Pandan, Belaga, Suai, Tatau, Sebauh, Bintulu',
        'SWK04': 'Sibu, Mukah, Dalat, Song, Igan, Oya, Balingian, Kanowit, Kapit',
        'SWK05': 'Sarikei, Matu, Julau, Rajang, Daro, Bintangor, Belawai',
        'SWK06': 'Lubok Antu, Sri Aman, Roban, Debak, Kabong, Lingga, Engkelili, Betong, Spaoh, Pusa, Saratok',
        'SWK07': 'Serian, Simunjan, Samarahan, Sebuyau, Meludam',
        'SWK08': 'Kuching, Bau, Lundu, Sematan',
        'SWK09': 'Zon Khas (Kampung Patarikan)'
    },
    'Terengganu': {
        'TRG01': 'Kuala Terengganu, Marang, Kuala Nerus',
        'TRG02': 'Besut, Setiu',
        'TRG03': 'Hulu Terengganu',
        'TRG04': 'Dungun, Kemaman'
    },
    'Wilayah Persekutuan': {
        'WLY01': 'Kuala Lumpur, Putrajaya',
        'WLY02': 'Labuan'
    }
}

CALCULATION_METHODS = {
    0: "Shia Ithna Ashari",
    1: "University of Islamic Sciences, Karachi",
    2: "Islamic Society of North America (ISNA)",
    3: "Muslim World League (MWL)",
    4: "Umm al-Qura, Makkah",
    5: "Egyptian General Authority of Survey",
    7: "Institute of Geophysics, University of Tehran",
    8: "Gulf Region",
    9: "Kuwait",
    10: "Qatar",
    11: "Majlis Ugama Islam Singapura, Singapore",
    12: "Union Organization Islamic de France",
    13: "Diyanet İşleri Başkanlığı, Turkey",
    14: "Spiritual Administration of Muslims of Russia",
    15: "Moonsighting Committee Worldwide",
    16: "Dubai (unofficial)",
    20: "Department of Islamic Advancement, Malaysia (JAKIM)",
    99: "Custom"
}

def parse_time(time_str):
    try:
        return datetime.strptime(time_str, "%H:%M:%S").strftime("%H:%M")
    except ValueError:
        return datetime.strptime(time_str, "%H:%M").strftime("%H:%M")

def convert_to_24hour(time_str):
    try:
        time_obj = datetime.strptime(time_str, "%I:%M %p")
        return time_obj.strftime("%H:%M")
    except ValueError:
        print(f"Error converting time: {time_str}")
        return time_str

def get_prayer_times(zone, lat=None, lon=None, method=20):
    print(f"get_prayer_times called with zone: {zone}, lat: {lat}, lon: {lon}, method: {method}")
    
    if zone:
        for state, zones in MALAYSIA_ZONES.items():
            if zone in zones:
                print(f"Zone {zone} found in {state}")
                times, source = get_jakim_prayer_times(zone), 'Malaysia'
                print(f"Prayer times from JAKIM: {times}")
                return times, source
        print(f"Zone {zone} not found in MALAYSIA_ZONES")
    elif lat and lon:
        print(f"Using international prayer times for coordinates: {lat}, {lon}")
        times, source = get_international_prayer_times(lat, lon, method), 'International'
        print(f"International prayer times: {times}")
        return times, source
    else:
        print("No valid zone or coordinates provided")
        return None, None

def get_jakim_prayer_times(zone):
    base_url = "https://www.e-solat.gov.my/index.php"
    params = {
        "r": "esolatApi/takwimsolat",
        "period": "today",
        "zone": zone
    }
    try:
        print(f"Requesting prayer times for zone: {zone}")
        print(f"Full URL: {base_url}?{'&'.join([f'{k}={v}' for k, v in params.items()])}")
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        print(f"JAKIM API response: {data}")

        if 'prayerTime' in data and data['prayerTime'] and isinstance(data['prayerTime'], list) and data['prayerTime'][0]:
            prayer_times = data['prayerTime'][0]
            result = {
                'Subuh': prayer_times.get('fajr', 'N/A'),
                'Syuruk': prayer_times.get('syuruk', 'N/A'),
                'Zohor': prayer_times.get('dhuhr', 'N/A'),
                'Asar': prayer_times.get('asr', 'N/A'),
                'Maghrib': prayer_times.get('maghrib', 'N/A'),
                'Isyak': prayer_times.get('isha', 'N/A')
            }
            print(f"Processed prayer times: {result}")
            return result
        else:
            print(f"Error: Unexpected data structure from JAKIM API: {data}")
            return None
    except requests.RequestException as e:
        print(f"Error fetching prayer times from JAKIM: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error in get_jakim_prayer_times: {e}")
        return None

def get_international_prayer_times(lat, lon, method=2):
    base_url = "http://api.aladhan.com/v1/timings"
    date = datetime.now().strftime("%d-%m-%Y")
    params = {
        "latitude": lat,
        "longitude": lon,
        "method": method,
        "date": date
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        if "data" in data and "timings" in data["data"]:
            return {
                'Subuh': data['data']['timings']['Fajr'],
                'Syuruk': data['data']['timings']['Sunrise'],
                'Zohor': data['data']['timings']['Dhuhr'],
                'Asar': data['data']['timings']['Asr'],
                'Maghrib': data['data']['timings']['Maghrib'],
                'Isyak': data['data']['timings']['Isha']
            }
    except requests.RequestException as e:
        print(f"Error fetching international prayer times: {e}")
    return None


def get_next_prayer(zone, lat=None, lon=None, method=20):
    times, location_type = get_prayer_times(zone, lat, lon, method)
    if not times:
        return None, None, None

    malaysia_tz = timezone('Asia/Kuala_Lumpur')
    now = datetime.now(malaysia_tz).time()
    next_prayer = None
    next_time = None

    for prayer, time_str in times.items():
        prayer_time = datetime.strptime(time_str, "%H:%M:%S").time()
        if prayer_time > now:
            if next_time is None or prayer_time < next_time:
                next_prayer = prayer
                next_time = prayer_time

    if next_prayer is None:
        next_prayer = "Subuh"
        next_time = datetime.strptime(times["Subuh"], "%H:%M:%S").time()
        next_time = datetime.combine(datetime.now(malaysia_tz).date() + timedelta(days=1), next_time).time()

    return next_prayer, next_time.strftime("%I:%M %p"), location_type

def format_prayer_times(zone, lat=None, lon=None, method=20):
    print(f"Formatting prayer times for zone: {zone}, lat: {lat}, lon: {lon}, method: {method}")
    times, location_type = get_prayer_times(zone, lat, lon, method)
    print(f"Received times: {times}, location_type: {location_type}")
    
    if not times:
        print("No prayer times received")
        return "Maaf, tidak dapat mendapatkan waktu solat untuk lokasi ini."
    
    if location_type == 'Malaysia':
        formatted = f"🕌 *Waktu Solat untuk {get_zone_name(zone)}:*\n\n"
    else:
        method_name = CALCULATION_METHODS.get(method, f"Kaedah Tidak Dikenali ({method})")
        formatted = f"🕌 *Waktu Solat untuk lokasi anda (Kaedah: {method_name}):*\n\n"
    
    emojis = {
        'Subuh': '🌄',
        'Syuruk': '🌅',
        'Zohor': '☀️',
        'Asar': '🌇',
        'Maghrib': '🌆',
        'Isyak': '🌙'
    }
    
    for prayer, time in times.items():
        emoji = emojis.get(prayer, '')
        formatted_time = datetime.strptime(time, '%H:%M:%S').strftime('%I:%M %p')
        formatted += f"{emoji} *{prayer}:* {formatted_time}\n"
    
    formatted += f"\n📅 *Tarikh:* {datetime.now(timezone('Asia/Kuala_Lumpur')).strftime('%d/%m/%Y')}"
    formatted += "\n🕰 *Zon Waktu:* Asia/Kuala_Lumpur"
    
    formatted += "\n\n📲 Dapatkan waktu solat di Telegram: [Muslim Prayer Times Bot](https://t.me/muslimprayertimes_bot)"
    
    print(f"Formatted prayer times: {formatted}")
    return formatted

def get_zone_name(zone):
    for state, zones in MALAYSIA_ZONES.items():
        if zone in zones:
            return zones[zone]
    return zone  # Return the zone code

def get_calculation_methods():
    return CALCULATION_METHODS

def send_prayer_notification(bot):
    malaysia_tz = timezone('Asia/Kuala_Lumpur')
    now = datetime.now(malaysia_tz)
    current_time = now.strftime("%H:%M")
    print(f"Checking notifications at {current_time}")  # Log masa semasa

    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT user_id, zone, latitude, longitude, language, calculation_method FROM users")
    users = c.fetchall()
    conn.close()

    for user in users:
        user_id, zone, lat, lon, lang, method = user
        print(f"Checking for user {user_id}, zone: {zone}, lat: {lat}, lon: {lon}")  # Log maklumat pengguna

        if zone:
            prayer_times, _ = get_prayer_times(zone)
        elif lat and lon:
            prayer_times, _ = get_prayer_times(None, lat, lon, method)
        else:
            continue  # Skip users without location info

        if prayer_times:
            print(f"Prayer times for user {user_id}: {prayer_times}")  # Log waktu solat
            for prayer, time in prayer_times.items():
                prayer_time = parse_time(time)
                if prayer_time == current_time:
                    print(f"Sending notification for {prayer} to user {user_id}")  # Log notifikasi yang dihantar
                    message = get_translation(lang, 'prayer_notification').format(prayer, datetime.strptime(time, "%H:%M:%S").strftime("%I:%M %p"))
                    bot.send_message(user_id, message)

def start_prayer_scheduler(bot):
    schedule.every(1).minutes.do(send_prayer_notification, bot)
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    # Test code
    print(format_prayer_times('SGR01'))
    print(format_prayer_times(None, 3.1390, 101.6869, 2))  # Kuala Lumpur coordinates
    next_prayer, next_time, location_type = get_next_prayer('SGR01')
    print(f"Next prayer: {next_prayer} at {next_time}")