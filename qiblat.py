import math
from config import KAABA_LAT, KAABA_LON


def calculate_qiblat(lat, lon):
    lat1 = math.radians(lat)
    lat2 = math.radians(KAABA_LAT)
    delta_lon = math.radians(KAABA_LON - lon)

    x = math.sin(delta_lon) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(delta_lon)

    bearing = math.degrees(math.atan2(x, y))
    bearing = (bearing + 360) % 360

    R = 6371
    dlat = math.radians(KAABA_LAT - lat)
    dlon = math.radians(KAABA_LON - lon)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat)) * math.cos(math.radians(KAABA_LAT)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c

    return bearing, distance


def get_compass_direction(bearing):
    directions = ['Utara', 'Timur Laut', 'Timur', 'Tenggara', 'Selatan', 'Barat Daya', 'Barat', 'Barat Laut']
    index = round(bearing / 45) % 8
    return directions[index]


def format_qiblat_info(lat, lon):
    bearing, distance = calculate_qiblat(lat, lon)
    direction = get_compass_direction(bearing)

    result = f"🕋 *Arah Kiblat*\n\n"
    result += f"📍 *Lokasi anda:* {lat:.4f}°, {lon:.4f}°\n"
    result += f"🧭 *Bearing:* {bearing:.1f}°\n"
    result += f"🔄 *Arah:* {direction}\n"
    result += f"📏 *Jarak ke Kaabah:* {distance:.0f} km\n"
    result += f"\n💡 Menghadap ke arah {direction} ({bearing:.1f}°) dari lokasi anda."

    return result
