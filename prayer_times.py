import requests
from datetime import datetime, timedelta
from pytz import timezone
import schedule
import time
from database import get_db_connection
from translations import get_translation
from zone_finder import get_malaysia_zone, get_zone_info

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

def parse_time(time_str):
    try:
        return datetime.strptime(time_str, "%H:%M:%S").strftime("%H:%M")
    except ValueError:
        return datetime.strptime(time_str, "%H:%M").strftime("%H:%M")

def get_prayer_times(zone=None, lat=None, lon=None):
    print(f"get_prayer_times called with zone: {zone}, lat: {lat}, lon: {lon}")
    
    if zone is None and lat is not None and lon is not None:
        zone = get_malaysia_zone(lat, lon)
    
    if zone:
        for state, zones in MALAYSIA_ZONES.items():
            if zone in zones:
                print(f"Zone {zone} found in {state}")
                times = get_jakim_prayer_times(zone)
                print(f"Prayer times from JAKIM: {times}")
                return times, 'Malaysia'
        print(f"Zone {zone} not found in MALAYSIA_ZONES")
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

def format_prayer_times(zone, lat=None, lon=None):
    print(f"Formatting prayer times for zone: {zone}, lat: {lat}, lon: {lon}")
    
    if zone is None and lat is not None and lon is not None:
        zone = get_malaysia_zone(lat, lon)
    
    times, location_type = get_prayer_times(zone, lat, lon)
    print(f"Received times: {times}, location_type: {location_type}")
    
    if not times:
        print("No prayer times received")
        return "Maaf, tidak dapat mendapatkan waktu solat untuk lokasi ini."
    
    zone_name = get_zone_name(zone)
    formatted = f"🕌 *Waktu Solat untuk {zone_name} ({zone}):*\n\n"
    
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
    return zone  # Return the zone code if not found

def send_prayer_notification(bot):
    malaysia_tz = timezone('Asia/Kuala_Lumpur')
    now = datetime.now(malaysia_tz)
    current_time = now.strftime("%H:%M")
    print(f"Checking notifications at {current_time}")

    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT user_id, zone, latitude, longitude, language FROM users")
    users = c.fetchall()
    conn.close()

    for user in users:
        user_id, zone, lat, lon, lang = user
        print(f"Checking for user {user_id}, zone: {zone}, lat: {lat}, lon: {lon}")

        if zone is None and lat is not None and lon is not None:
            zone = get_malaysia_zone(lat, lon)

        if zone:
            prayer_times, _ = get_prayer_times(zone)
            if prayer_times:
                print(f"Prayer times for user {user_id}: {prayer_times}")
                for prayer, time in prayer_times.items():
                    prayer_time = parse_time(time)
                    if prayer_time == current_time:
                        print(f"Sending notification for {prayer} to user {user_id}")
                        message = get_translation(lang, 'prayer_notification').format(prayer, datetime.strptime(time, "%H:%M:%S").strftime("%I:%M %p"))
                        bot.send_message(user_id, message)
        else:
            print(f"No valid zone for user {user_id}")

def start_prayer_scheduler(bot):
    schedule.every(1).minutes.do(send_prayer_notification, bot)
    
    while True:
        schedule.run_pending()
        time.sleep(60)

def get_next_prayer(zone, lat=None, lon=None):
    times, location_type = get_prayer_times(zone, lat, lon)
    if not times:
        return None, None, None
    
    malaysia_tz = timezone('Asia/Kuala_Lumpur')
    now = datetime.now(malaysia_tz).time()
    
    for prayer, time_str in times.items():
        prayer_time = datetime.strptime(time_str, '%H:%M:%S').time()
        if prayer_time > now:
            return prayer, prayer_time.strftime('%I:%M %p'), location_type
    
    # If no upcoming prayer is found for today, return the first prayer of the next day
    first_prayer, first_time_str = list(times.items())[0]
    first_time = datetime.strptime(first_time_str, '%H:%M:%S').time()
    return first_prayer, first_time.strftime('%I:%M %p'), location_type

if __name__ == "__main__":
    # Test code
    print(format_prayer_times('SGR01'))
    print(format_prayer_times(None, 3.1390, 101.6869))  # Kuala Lumpur coordinates
    next_prayer, next_time, location_type = get_next_prayer('SGR01')
    print(f"Next prayer: {next_prayer} at {next_time}")