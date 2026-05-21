import requests
from datetime import datetime, timedelta
from pytz import timezone
import schedule
import time
from database import get_db_connection, get_user_pre_notification
from translations import get_translation
from zone_finder import get_malaysia_zone, get_zone_info, MALAYSIA_ZONES

FARD_PRAYERS = ['Subuh', 'Zohor', 'Asar', 'Maghrib', 'Isyak']

_prayer_cache = {}


def _cache_key(zone, date_str):
    return f"{zone}_{date_str}"


def _get_today_str():
    return datetime.now(timezone('Asia/Kuala_Lumpur')).strftime('%Y-%m-%d')


def parse_time(time_str):
    if not time_str or time_str == 'N/A':
        return None
    try:
        return datetime.strptime(time_str, "%H:%M:%S").strftime("%H:%M")
    except ValueError:
        try:
            return datetime.strptime(time_str, "%H:%M").strftime("%H:%M")
        except ValueError:
            return None


def get_prayer_times(zone=None, lat=None, lon=None):
    if zone is None and lat is not None and lon is not None:
        zone = get_malaysia_zone(lat, lon)

    if zone:
        for state, zones in MALAYSIA_ZONES.items():
            if zone in zones:
                times = get_cached_prayer_times(zone)
                return times, 'Malaysia'

    return None, None


def get_cached_prayer_times(zone):
    today = _get_today_str()
    key = _cache_key(zone, today)
    if key in _prayer_cache:
        return _prayer_cache[key]
    times = get_jakim_prayer_times(zone)
    if times:
        _prayer_cache[key] = times
    return times


def get_jakim_prayer_times(zone):
    base_url = "https://www.e-solat.gov.my/index.php"
    params = {
        "r": "esolatApi/takwimsolat",
        "period": "today",
        "zone": zone
    }
    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if 'prayerTime' in data and data['prayerTime'] and isinstance(data['prayerTime'], list) and data['prayerTime'][0]:
            prayer_times = data['prayerTime'][0]
            return {
                'Subuh': prayer_times.get('fajr', 'N/A'),
                'Syuruk': prayer_times.get('syuruk', 'N/A'),
                'Zohor': prayer_times.get('dhuhr', 'N/A'),
                'Asar': prayer_times.get('asr', 'N/A'),
                'Maghrib': prayer_times.get('maghrib', 'N/A'),
                'Isyak': prayer_times.get('isha', 'N/A')
            }
        return None
    except (requests.RequestException, Exception) as e:
        print(f"Error fetching prayer times from JAKIM: {e}")
        return None


def get_jakim_prayer_times_period(zone, period='week'):
    base_url = "https://www.e-solat.gov.my/index.php"
    params = {
        "r": "esolatApi/takwimsolat",
        "period": period,
        "zone": zone
    }
    try:
        response = requests.get(base_url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()

        if 'prayerTime' in data and data['prayerTime'] and isinstance(data['prayerTime'], list):
            results = []
            for day in data['prayerTime']:
                results.append({
                    'date': day.get('date', ''),
                    'hijri': day.get('hijri', ''),
                    'day': day.get('day', ''),
                    'Subuh': day.get('fajr', 'N/A'),
                    'Syuruk': day.get('syuruk', 'N/A'),
                    'Zohor': day.get('dhuhr', 'N/A'),
                    'Asar': day.get('asr', 'N/A'),
                    'Maghrib': day.get('maghrib', 'N/A'),
                    'Isyak': day.get('isha', 'N/A')
                })
            return results
        return None
    except (requests.RequestException, Exception) as e:
        print(f"Error fetching {period} prayer times: {e}")
        return None


def format_prayer_times(zone, lat=None, lon=None):
    if zone is None and lat is not None and lon is not None:
        zone = get_malaysia_zone(lat, lon)

    times, location_type = get_prayer_times(zone, lat, lon)

    if not times:
        return "Maaf, tidak dapat mendapatkan waktu solat untuk lokasi ini."

    zone_name = get_zone_name(zone)
    formatted = f"🕌 *Waktu Solat untuk {zone_name} ({zone}):*\n\n"

    emojis = {
        'Subuh': '🌄', 'Syuruk': '🌅', 'Zohor': '☀️',
        'Asar': '🌇', 'Maghrib': '🌆', 'Isyak': '🌙'
    }

    for prayer, time_val in times.items():
        emoji = emojis.get(prayer, '')
        parsed = parse_time(time_val)
        if parsed:
            try:
                formatted_time = datetime.strptime(time_val, '%H:%M:%S').strftime('%I:%M %p')
            except ValueError:
                formatted_time = parsed
        else:
            formatted_time = 'N/A'
        formatted += f"{emoji} *{prayer}:* {formatted_time}\n"

    malaysia_tz = timezone('Asia/Kuala_Lumpur')
    formatted += f"\n📅 *Tarikh:* {datetime.now(malaysia_tz).strftime('%d/%m/%Y')}"
    formatted += "\n🕰 *Zon Waktu:* Asia/Kuala_Lumpur"

    return formatted


def format_weekly_prayer_times(zone):
    days = get_jakim_prayer_times_period(zone, 'week')
    if not days:
        return None

    zone_name = get_zone_name(zone)
    formatted = f"📅 *Waktu Solat Mingguan — {zone_name} ({zone})*\n"

    for day in days:
        date_str = day.get('date', '')
        day_name = day.get('day', '')

        formatted += f"\n*{day_name}, {date_str}*\n"
        for prayer in ['Subuh', 'Zohor', 'Asar', 'Maghrib', 'Isyak']:
            parsed = parse_time(day.get(prayer, 'N/A'))
            formatted += f"  {prayer}: {parsed or 'N/A'}"
            if prayer != 'Isyak':
                formatted += " | "
        formatted += "\n"

    return formatted


def format_monthly_prayer_times(zone):
    days = get_jakim_prayer_times_period(zone, 'month')
    if not days:
        return None

    zone_name = get_zone_name(zone)
    messages = []
    chunk_size = 10

    for i in range(0, len(days), chunk_size):
        chunk = days[i:i + chunk_size]
        part = i // chunk_size + 1
        total_parts = (len(days) + chunk_size - 1) // chunk_size
        formatted = f"📅 *Waktu Solat Bulanan — {zone_name} ({zone})*\n"
        formatted += f"_(Bahagian {part}/{total_parts})_\n"

        for day in chunk:
            date_str = day.get('date', '')

            formatted += f"\n*{date_str}*\n"
            for prayer in ['Subuh', 'Zohor', 'Asar', 'Maghrib', 'Isyak']:
                parsed = parse_time(day.get(prayer, 'N/A'))
                formatted += f"  {prayer}: {parsed or 'N/A'}"
                if prayer != 'Isyak':
                    formatted += " | "
            formatted += "\n"

        messages.append(formatted)

    return messages


def get_zone_name(zone):
    for state, zones in MALAYSIA_ZONES.items():
        if zone in zones:
            return zones[zone]
    return zone


def send_prayer_notification(bot):
    malaysia_tz = timezone('Asia/Kuala_Lumpur')
    now = datetime.now(malaysia_tz)
    current_time = now.strftime("%H:%M")

    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT user_id, zone, latitude, longitude, language, pre_notification FROM users")
    users = c.fetchall()
    conn.close()

    zone_cache = {}

    for user in users:
        user_id, zone, lat, lon, lang, pre_notif = user

        if zone is None and lat is not None and lon is not None:
            zone = get_malaysia_zone(lat, lon)

        if not zone:
            continue

        if zone not in zone_cache:
            prayer_times, _ = get_prayer_times(zone)
            zone_cache[zone] = prayer_times

        prayer_times = zone_cache[zone]
        if not prayer_times:
            continue

        for prayer, time_val in prayer_times.items():
            if prayer not in FARD_PRAYERS:
                continue

            prayer_time = parse_time(time_val)
            if not prayer_time:
                continue

            if prayer_time == current_time:
                try:
                    formatted_time = datetime.strptime(time_val, "%H:%M:%S").strftime("%I:%M %p")
                except ValueError:
                    formatted_time = prayer_time
                message = get_translation(lang, 'prayer_notification').format(prayer, formatted_time)
                try:
                    bot.send_message(user_id, message)
                except Exception as e:
                    print(f"Failed to send notification to {user_id}: {e}")

            if pre_notif and pre_notif > 0:
                try:
                    prayer_dt = datetime.strptime(f"{now.strftime('%Y-%m-%d')} {time_val}", "%Y-%m-%d %H:%M:%S")
                    pre_dt = prayer_dt - timedelta(minutes=pre_notif)
                    pre_time_str = pre_dt.strftime("%H:%M")
                    if pre_time_str == current_time:
                        message = get_translation(lang, 'pre_notification').format(minutes=pre_notif, prayer=prayer)
                        try:
                            bot.send_message(user_id, message)
                        except Exception as e:
                            print(f"Failed to send pre-notification to {user_id}: {e}")
                except ValueError:
                    pass


def start_prayer_scheduler(bot):
    schedule.every(1).minutes.do(send_prayer_notification, bot)

    while True:
        schedule.run_pending()
        time.sleep(30)


def get_next_prayer(zone, lat=None, lon=None):
    times, location_type = get_prayer_times(zone, lat, lon)
    if not times:
        return None, None, None, None

    malaysia_tz = timezone('Asia/Kuala_Lumpur')
    now = datetime.now(malaysia_tz)

    for prayer, time_str in times.items():
        if prayer not in FARD_PRAYERS:
            continue
        parsed = parse_time(time_str)
        if not parsed:
            continue
        try:
            prayer_time = datetime.strptime(time_str, '%H:%M:%S').time()
        except ValueError:
            continue
        if prayer_time > now.time():
            prayer_dt = now.replace(hour=prayer_time.hour, minute=prayer_time.minute, second=0, microsecond=0)
            remaining = prayer_dt - now
            mins = int(remaining.total_seconds() // 60)
            if mins >= 60:
                countdown = f"{mins // 60} jam {mins % 60} minit"
            else:
                countdown = f"{mins} minit"
            return prayer, prayer_time.strftime('%I:%M %p'), location_type, countdown

    first_fard = [(p, t) for p, t in times.items() if p in FARD_PRAYERS]
    if first_fard:
        prayer, time_str = first_fard[0]
        parsed = parse_time(time_str)
        if parsed:
            try:
                prayer_time = datetime.strptime(time_str, '%H:%M:%S').time()
                tomorrow = now + timedelta(days=1)
                prayer_dt = tomorrow.replace(hour=prayer_time.hour, minute=prayer_time.minute, second=0, microsecond=0)
                remaining = prayer_dt - now
                mins = int(remaining.total_seconds() // 60)
                hours = mins // 60
                countdown = f"{hours} jam {mins % 60} minit"
                return prayer, prayer_time.strftime('%I:%M %p'), location_type, countdown
            except ValueError:
                pass

    return None, None, None, None
