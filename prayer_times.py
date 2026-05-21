import requests
from datetime import datetime, timedelta
from pytz import timezone
import schedule
import time
from database import get_db_connection, get_user_pre_notification
from translations import get_translation
from zone_finder import (
    get_malaysia_zone, get_zone_info, get_country_code, get_location_name,
    MALAYSIA_ZONES,
)

FARD_PRAYERS = ['Subuh', 'Zohor', 'Asar', 'Maghrib', 'Isyak']

_prayer_cache = {}

ALADHAN_METHODS = {
    'pk': 1, 'in': 1, 'bd': 1, 'af': 1, 'np': 1, 'lk': 1,
    'us': 2, 'ca': 2, 'mx': 2,
    'sa': 4, 'ye': 4,
    'eg': 5, 'sd': 5, 'ly': 5, 'sy': 5, 'iq': 5, 'lb': 5, 'jo': 5, 'ps': 5,
    'ir': 7,
    'ae': 8, 'om': 8, 'bh': 8,
    'kw': 9,
    'qa': 10,
    'sg': 11,
    'fr': 12,
    'tr': 13, 'az': 13, 'uz': 13, 'kz': 13, 'kg': 13, 'tj': 13, 'tm': 13,
    'ru': 14, 'ua': 14, 'by': 14, 'ge': 14,
}

HANAFI_COUNTRIES = {
    'pk', 'in', 'bd', 'af', 'np', 'lk',
    'tr', 'az', 'uz', 'kz', 'kg', 'tj', 'tm',
    'iq', 'sy',
}

METHOD_NAMES = {
    1: 'University of Islamic Sciences, Karachi',
    2: 'Islamic Society of North America (ISNA)',
    3: 'Muslim World League (MWL)',
    4: 'Umm Al-Qura University, Makkah',
    5: 'Egyptian General Authority of Survey',
    7: 'Institute of Geophysics, University of Tehran',
    8: 'Gulf Region',
    9: 'Kuwait',
    10: 'Qatar',
    11: 'Majlis Ugama Islam Singapura (MUIS)',
    12: "Union Organization Islamic de France (UOIF)",
    13: 'Diyanet İşleri Başkanlığı, Turkey',
    14: 'Spiritual Administration of Muslims of Russia',
}


def _get_method_for_country(country_code):
    return ALADHAN_METHODS.get(country_code, 3)


def _get_school_for_country(country_code):
    return 1 if country_code in HANAFI_COUNTRIES else 0


def _cache_key(identifier, date_str):
    return f"{identifier}_{date_str}"


def _get_today_str():
    return datetime.now(timezone('Asia/Kuala_Lumpur')).strftime('%Y-%m-%d')


def _get_utc_today_str():
    return datetime.utcnow().strftime('%d-%m-%Y')


def parse_time(time_str):
    if not time_str or time_str == 'N/A':
        return None
    time_str = time_str.strip()
    if ' ' in time_str:
        time_str = time_str.split(' ')[0]
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

    if lat is not None and lon is not None:
        country = get_country_code(lat, lon)
        method = _get_method_for_country(country or '')
        school = _get_school_for_country(country or '')
        times = get_aladhan_prayer_times(lat, lon, method, school)
        if times:
            return times, 'International'

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


def get_aladhan_prayer_times(lat, lon, method=3, school=0):
    today = _get_today_str()
    key = _cache_key(f"aladhan_{lat:.2f}_{lon:.2f}_{method}_{school}", today)
    if key in _prayer_cache:
        return _prayer_cache[key]

    date_str = _get_utc_today_str()
    try:
        response = requests.get(
            f"https://api.aladhan.com/v1/timings/{date_str}",
            params={
                'latitude': lat, 'longitude': lon,
                'method': method, 'school': school,
            },
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        if data.get('code') == 200 and 'data' in data:
            timings = data['data']['timings']
            result = {
                'Subuh': timings.get('Fajr', 'N/A'),
                'Syuruk': timings.get('Sunrise', 'N/A'),
                'Zohor': timings.get('Dhuhr', 'N/A'),
                'Asar': timings.get('Asr', 'N/A'),
                'Maghrib': timings.get('Maghrib', 'N/A'),
                'Isyak': timings.get('Isha', 'N/A'),
            }
            _prayer_cache[key] = result
            return result
        return None
    except (requests.RequestException, Exception) as e:
        print(f"Error fetching prayer times from Aladhan: {e}")
        return None


def get_aladhan_prayer_times_period(lat, lon, method, school, year, month):
    try:
        response = requests.get(
            f"https://api.aladhan.com/v1/calendar/{year}/{month}",
            params={
                'latitude': lat, 'longitude': lon,
                'method': method, 'school': school,
            },
            timeout=15,
        )
        response.raise_for_status()
        data = response.json()

        if data.get('code') == 200 and 'data' in data:
            results = []
            for day_data in data['data']:
                timings = day_data['timings']
                date_info = day_data['date']
                results.append({
                    'date': date_info['readable'],
                    'hijri': date_info.get('hijri', {}).get('date', ''),
                    'day': date_info.get('gregorian', {}).get('weekday', {}).get('en', ''),
                    'Subuh': timings.get('Fajr', 'N/A'),
                    'Syuruk': timings.get('Sunrise', 'N/A'),
                    'Zohor': timings.get('Dhuhr', 'N/A'),
                    'Asar': timings.get('Asr', 'N/A'),
                    'Maghrib': timings.get('Maghrib', 'N/A'),
                    'Isyak': timings.get('Isha', 'N/A'),
                })
            return results
        return None
    except (requests.RequestException, Exception) as e:
        print(f"Error fetching Aladhan calendar: {e}")
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


def format_prayer_times(zone, lat=None, lon=None, lang='ms'):
    if zone is None and lat is not None and lon is not None:
        zone = get_malaysia_zone(lat, lon)

    times, location_type = get_prayer_times(zone, lat, lon)

    if not times:
        return get_translation(lang, 'error_getting_prayer_times')

    emojis = {
        'Subuh': '🌄', 'Syuruk': '🌅', 'Zohor': '☀️',
        'Asar': '🌇', 'Maghrib': '🌆', 'Isyak': '🌙'
    }

    if location_type == 'Malaysia' and zone:
        zone_name = get_zone_name(zone)
        formatted = f"🕌 *Waktu Solat untuk {zone_name} ({zone}):*\n\n"
    else:
        loc_name = get_location_name(lat, lon) if lat and lon else "?"
        country = get_country_code(lat, lon) if lat and lon else None
        method = _get_method_for_country(country or '')
        method_name = METHOD_NAMES.get(method, 'Muslim World League')
        school = 'Hanafi' if _get_school_for_country(country or '') == 1 else "Shafi'i"
        formatted = f"🕌 *Waktu Solat untuk {loc_name}:*\n\n"
        formatted += f"📐 *Kaedah:* {method_name}\n"
        formatted += f"📖 *Mazhab:* {school}\n\n"

    for prayer, time_val in times.items():
        emoji = emojis.get(prayer, '')
        parsed = parse_time(time_val)
        if parsed:
            try:
                formatted_time = datetime.strptime(parsed, '%H:%M').strftime('%I:%M %p')
            except ValueError:
                formatted_time = parsed
        else:
            formatted_time = 'N/A'
        formatted += f"{emoji} *{prayer}:* {formatted_time}\n"

    formatted += f"\n📅 *Tarikh:* {datetime.utcnow().strftime('%d/%m/%Y')}"
    if location_type == 'Malaysia':
        formatted += "\n🕰 *Zon Waktu:* Asia/Kuala\\_Lumpur"

    return formatted


def format_weekly_prayer_times(zone=None, lat=None, lon=None):
    if zone:
        days = get_jakim_prayer_times_period(zone, 'week')
        title = f"{get_zone_name(zone)} ({zone})"
    elif lat is not None and lon is not None:
        country = get_country_code(lat, lon)
        method = _get_method_for_country(country or '')
        school = _get_school_for_country(country or '')
        now = datetime.utcnow()
        days = get_aladhan_prayer_times_period(lat, lon, method, school, now.year, now.month)
        if days:
            today_idx = now.day - 1
            days = days[today_idx:today_idx + 7]
        title = get_location_name(lat, lon)
    else:
        return None

    if not days:
        return None

    formatted = f"📅 *Waktu Solat Mingguan — {title}*\n"
    for day in days:
        date_str = day.get('date', '')
        day_name = day.get('day', '')
        label = f"{day_name}, {date_str}" if day_name else date_str

        formatted += f"\n*{label}*\n"
        for prayer in ['Subuh', 'Zohor', 'Asar', 'Maghrib', 'Isyak']:
            parsed = parse_time(day.get(prayer, 'N/A'))
            formatted += f"  {prayer}: {parsed or 'N/A'}"
            if prayer != 'Isyak':
                formatted += " | "
        formatted += "\n"

    return formatted


def format_monthly_prayer_times(zone=None, lat=None, lon=None):
    if zone:
        days = get_jakim_prayer_times_period(zone, 'month')
        title = f"{get_zone_name(zone)} ({zone})"
    elif lat is not None and lon is not None:
        country = get_country_code(lat, lon)
        method = _get_method_for_country(country or '')
        school = _get_school_for_country(country or '')
        now = datetime.utcnow()
        days = get_aladhan_prayer_times_period(lat, lon, method, school, now.year, now.month)
        title = get_location_name(lat, lon)
    else:
        return None

    if not days:
        return None

    messages = []
    chunk_size = 10

    for i in range(0, len(days), chunk_size):
        chunk = days[i:i + chunk_size]
        part = i // chunk_size + 1
        total_parts = (len(days) + chunk_size - 1) // chunk_size
        formatted = f"📅 *Waktu Solat Bulanan — {title}*\n"
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
    from pytz import utc as utc_tz

    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT user_id, zone, latitude, longitude, language, pre_notification FROM users")
    users = c.fetchall()
    conn.close()

    now_utc = datetime.now(timezone('UTC'))
    notification_cache = {}

    for user in users:
        user_id, zone, lat, lon, lang, pre_notif = user

        if zone is None and lat is not None and lon is not None:
            zone = get_malaysia_zone(lat, lon)

        if zone:
            cache_id = zone
        elif lat is not None and lon is not None:
            cache_id = f"{lat:.2f}_{lon:.2f}"
        else:
            continue

        if cache_id not in notification_cache:
            prayer_times_data, loc_type = get_prayer_times(zone, lat, lon)
            notification_cache[cache_id] = prayer_times_data
        prayer_times_data = notification_cache[cache_id]

        if not prayer_times_data:
            continue

        if zone:
            current_time = datetime.now(timezone('Asia/Kuala_Lumpur')).strftime("%H:%M")
        else:
            current_time = now_utc.strftime("%H:%M")

        for prayer, time_val in prayer_times_data.items():
            if prayer not in FARD_PRAYERS:
                continue

            prayer_time = parse_time(time_val)
            if not prayer_time:
                continue

            if prayer_time == current_time:
                try:
                    formatted_time = datetime.strptime(prayer_time, "%H:%M").strftime("%I:%M %p")
                except ValueError:
                    formatted_time = prayer_time
                message = get_translation(lang, 'prayer_notification').format(prayer, formatted_time)
                try:
                    bot.send_message(user_id, message)
                except Exception as e:
                    print(f"Failed to send notification to {user_id}: {e}")

            if pre_notif and pre_notif > 0:
                try:
                    today_str = now_utc.strftime('%Y-%m-%d')
                    prayer_dt = datetime.strptime(f"{today_str} {prayer_time}", "%Y-%m-%d %H:%M")
                    pre_dt = prayer_dt - timedelta(minutes=pre_notif)
                    if pre_dt.strftime("%H:%M") == current_time:
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

    if location_type == 'Malaysia':
        now = datetime.now(timezone('Asia/Kuala_Lumpur'))
    else:
        now = datetime.utcnow()

    for prayer, time_str in times.items():
        if prayer not in FARD_PRAYERS:
            continue
        parsed = parse_time(time_str)
        if not parsed:
            continue
        try:
            prayer_time = datetime.strptime(parsed, '%H:%M').time()
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
                prayer_time = datetime.strptime(parsed, '%H:%M').time()
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
