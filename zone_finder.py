import requests

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

# --- Reverse geocoding district → zone mapping ---

_STATE_ALIASES = {
    'malacca': 'Melaka',
    'melaka': 'Melaka',
    'penang': 'Pulau Pinang',
    'pulau pinang': 'Pulau Pinang',
    'perlis': 'Perlis',
    'johor': 'Johor',
    'kedah': 'Kedah',
    'kelantan': 'Kelantan',
    'negeri sembilan': 'Negeri Sembilan',
    'pahang': 'Pahang',
    'perak': 'Perak',
    'selangor': 'Selangor',
    'terengganu': 'Terengganu',
    'sabah': 'Sabah',
    'sarawak': 'Sarawak',
}

_SINGLE_ZONE_STATES = {
    'Melaka': 'MLK01',
    'Perlis': 'PLS01',
    'Pulau Pinang': 'PNG01',
}

_WP_ZONES = {
    'kuala lumpur': 'WLY01',
    'putrajaya': 'WLY01',
    'labuan': 'WLY02',
}

_CITY_TO_ZONE = {
    'Johor': {
        'johor bahru': 'JHR02', 'johor bharu': 'JHR02', 'kota tinggi': 'JHR02',
        'mersing': 'JHR02', 'kulai': 'JHR02',
        'kluang': 'JHR03', 'pontian': 'JHR03',
        'batu pahat': 'JHR04', 'muar': 'JHR04', 'segamat': 'JHR04',
        'gemas': 'JHR04', 'tangkak': 'JHR04', 'ledang': 'JHR04',
    },
    'Kedah': {
        'kota setar': 'KDH01', 'kubang pasu': 'KDH01', 'pokok sena': 'KDH01',
        'alor setar': 'KDH01', 'alor star': 'KDH01',
        'kuala muda': 'KDH02', 'yan': 'KDH02', 'pendang': 'KDH02',
        'sungai petani': 'KDH02',
        'padang terap': 'KDH03', 'sik': 'KDH03',
        'baling': 'KDH04',
        'bandar baharu': 'KDH05', 'kulim': 'KDH05', 'bandar bahru': 'KDH05',
        'langkawi': 'KDH06',
    },
    'Kelantan': {
        'kota bharu': 'KTN01', 'bachok': 'KTN01', 'machang': 'KTN01',
        'pasir mas': 'KTN01', 'pasir puteh': 'KTN01', 'tanah merah': 'KTN01',
        'tumpat': 'KTN01', 'kuala krai': 'KTN01',
        'gua musang': 'KTN03', 'jeli': 'KTN03',
    },
    'Negeri Sembilan': {
        'tampin': 'NGS01', 'jempol': 'NGS01',
        'jelebu': 'NGS02', 'kuala pilah': 'NGS02', 'port dickson': 'NGS02',
        'rembau': 'NGS02', 'seremban': 'NGS02',
    },
    'Pahang': {
        'kuantan': 'PHG02', 'pekan': 'PHG02', 'rompin': 'PHG02',
        'muadzam shah': 'PHG02',
        'jerantut': 'PHG03', 'temerloh': 'PHG03', 'maran': 'PHG03',
        'bera': 'PHG03', 'jengka': 'PHG03',
        'bentong': 'PHG04', 'lipis': 'PHG04', 'raub': 'PHG04',
        'kuala lipis': 'PHG04',
        'genting sempah': 'PHG05', 'janda baik': 'PHG05', 'bukit tinggi': 'PHG05',
        'cameron highlands': 'PHG06', 'genting highlands': 'PHG06',
        'bukit fraser': 'PHG06', "fraser's hill": 'PHG06',
    },
    'Perak': {
        'tapah': 'PRK01', 'slim river': 'PRK01', 'tanjung malim': 'PRK01',
        'tanjong malim': 'PRK01', 'batang padang': 'PRK01', 'muallim': 'PRK01',
        'kuala kangsar': 'PRK02', 'sungai siput': 'PRK02', 'ipoh': 'PRK02',
        'batu gajah': 'PRK02', 'kampar': 'PRK02', 'kinta': 'PRK02',
        'lenggong': 'PRK03', 'pengkalan hulu': 'PRK03', 'grik': 'PRK03',
        'gerik': 'PRK03', 'hulu perak': 'PRK03',
        'temengor': 'PRK04', 'belum': 'PRK04',
        'teluk intan': 'PRK05', 'bagan datuk': 'PRK05', 'seri iskandar': 'PRK05',
        'lumut': 'PRK05', 'sitiawan': 'PRK05', 'kampung gajah': 'PRK05',
        'hilir perak': 'PRK05', 'manjung': 'PRK05', 'perak tengah': 'PRK05',
        'selama': 'PRK06', 'taiping': 'PRK06', 'bagan serai': 'PRK06',
        'parit buntar': 'PRK06', 'kerian': 'PRK06', 'larut': 'PRK06',
        'larut, matang dan selama': 'PRK06',
        'bukit larut': 'PRK07',
    },
    'Selangor': {
        'gombak': 'SGR01', 'petaling': 'SGR01', 'petaling jaya': 'SGR01',
        'sepang': 'SGR01', 'hulu langat': 'SGR01', 'hulu selangor': 'SGR01',
        'shah alam': 'SGR01', 'rawang': 'SGR01', 'subang jaya': 'SGR01',
        'ampang': 'SGR01', 'kajang': 'SGR01', 'bangi': 'SGR01',
        'cyberjaya': 'SGR01', 'puchong': 'SGR01', 'serdang': 'SGR01',
        'kuala selangor': 'SGR02', 'sabak bernam': 'SGR02',
        'tanjong karang': 'SGR02',
        'klang': 'SGR03', 'kuala langat': 'SGR03', 'port klang': 'SGR03',
        'banting': 'SGR03',
    },
    'Terengganu': {
        'kuala terengganu': 'TRG01', 'marang': 'TRG01', 'kuala nerus': 'TRG01',
        'besut': 'TRG02', 'setiu': 'TRG02',
        'hulu terengganu': 'TRG03',
        'dungun': 'TRG04', 'kemaman': 'TRG04',
    },
    'Sabah': {
        'sandakan': 'SBH01',
        'beluran': 'SBH02', 'telupid': 'SBH02', 'kuamut': 'SBH02',
        'pinangah': 'SBH02',
        'lahad datu': 'SBH03', 'kunak': 'SBH03', 'semporna': 'SBH03',
        'silabukan': 'SBH03',
        'tawau': 'SBH04', 'kalabakan': 'SBH04',
        'kudat': 'SBH05', 'kota marudu': 'SBH05', 'pitas': 'SBH05',
        'kota kinabalu': 'SBH07', 'kota belud': 'SBH07', 'tuaran': 'SBH07',
        'penampang': 'SBH07', 'papar': 'SBH07', 'putatan': 'SBH07',
        'ranau': 'SBH07',
        'keningau': 'SBH08', 'tambunan': 'SBH08', 'nabawan': 'SBH08',
        'pensiangan': 'SBH08',
        'beaufort': 'SBH09', 'sipitang': 'SBH09', 'tenom': 'SBH09',
        'kuala penyu': 'SBH09', 'membakut': 'SBH09', 'weston': 'SBH09',
        'west coast division': 'SBH07', 'sandakan division': 'SBH01',
        'tawau division': 'SBH04', 'kudat division': 'SBH05',
        'interior division': 'SBH08',
    },
    'Sarawak': {
        'kuching': 'SWK08', 'bau': 'SWK08', 'lundu': 'SWK08', 'sematan': 'SWK08',
        'serian': 'SWK07', 'simunjan': 'SWK07', 'samarahan': 'SWK07',
        'sri aman': 'SWK06', 'betong': 'SWK06', 'saratok': 'SWK06',
        'lubok antu': 'SWK06', 'engkelili': 'SWK06',
        'sarikei': 'SWK05', 'bintangor': 'SWK05', 'daro': 'SWK05',
        'julau': 'SWK05',
        'sibu': 'SWK04', 'mukah': 'SWK04', 'kapit': 'SWK04',
        'kanowit': 'SWK04', 'dalat': 'SWK04',
        'bintulu': 'SWK03', 'belaga': 'SWK03', 'tatau': 'SWK03',
        'sebauh': 'SWK03',
        'miri': 'SWK02', 'marudi': 'SWK02', 'niah': 'SWK02',
        'limbang': 'SWK01', 'lawas': 'SWK01',
        'kuching division': 'SWK08', 'samarahan division': 'SWK07',
        'sri aman division': 'SWK06', 'betong division': 'SWK06',
        'sarikei division': 'SWK05', 'sibu division': 'SWK04',
        'mukah division': 'SWK04', 'kapit division': 'SWK04',
        'bintulu division': 'SWK03', 'miri division': 'SWK02',
        'limbang division': 'SWK01',
    },
}

_geocode_cache = {}
_country_cache = {}
_NOMINATIM_URL = 'https://nominatim.openstreetmap.org/reverse'
_HEADERS = {'User-Agent': 'WaktuSolatBot/1.0'}


def get_malaysia_zone(lat, lon):
    zone = _zone_from_geocoding(lat, lon)
    if zone:
        return zone
    return _zone_from_bounds(lat, lon)


def get_country_code(lat, lon):
    cache_key = (round(lat, 2), round(lon, 2))
    if cache_key in _country_cache:
        return _country_cache[cache_key]
    _do_geocode(lat, lon)
    return _country_cache.get(cache_key)


def get_location_name(lat, lon):
    _do_geocode(lat, lon)
    cache_key = (round(lat, 2), round(lon, 2))
    return _country_cache.get(f"{cache_key}_name", f"{lat:.2f}, {lon:.2f}")


def _do_geocode(lat, lon):
    cache_key = (round(lat, 2), round(lon, 2))
    if cache_key in _country_cache:
        return

    try:
        resp = requests.get(_NOMINATIM_URL, params={
            'lat': lat, 'lon': lon, 'format': 'json',
            'addressdetails': 1, 'accept-language': 'en',
        }, headers=_HEADERS, timeout=4)
        resp.raise_for_status()
        data = resp.json()
    except Exception:
        return

    addr = data.get('address', {})
    country_code = addr.get('country_code', '')
    _country_cache[cache_key] = country_code

    city = addr.get('city', addr.get('town', addr.get('village', ''))).strip()
    country_name = addr.get('country', '').strip()
    state = addr.get('state', '').strip()
    parts = [p for p in [city, state, country_name] if p]
    _country_cache[f"{cache_key}_name"] = ', '.join(parts) if parts else f"{lat:.2f}, {lon:.2f}"

    if country_code == 'my':
        state_raw = state
        county = addr.get('county', addr.get('state_district', '')).strip()
        zone = _match_zone(state_raw, city, county)
        _geocode_cache[cache_key] = zone
    else:
        _geocode_cache[cache_key] = None


def _zone_from_geocoding(lat, lon):
    cache_key = (round(lat, 2), round(lon, 2))
    if cache_key in _geocode_cache:
        return _geocode_cache[cache_key]
    _do_geocode(lat, lon)
    return _geocode_cache.get(cache_key)


def _match_zone(state_raw, city, county):
    state_lower = state_raw.lower()
    city_lower = city.lower()
    county_lower = county.lower().replace(' district', '')

    if state_lower in _WP_ZONES:
        return _WP_ZONES[state_lower]
    if city_lower in _WP_ZONES:
        return _WP_ZONES[city_lower]

    state = _STATE_ALIASES.get(state_lower)
    if not state:
        return None

    if state in _SINGLE_ZONE_STATES:
        return _SINGLE_ZONE_STATES[state]

    zone_map = _CITY_TO_ZONE.get(state, {})

    for name in [city_lower, county_lower]:
        if not name:
            continue
        if name in zone_map:
            return zone_map[name]
        for key, zone in zone_map.items():
            if key in name or name in key:
                return zone

    return None


# --- Bounding box fallback ---

def _zone_from_bounds(lat, lon):
    if 5.2 <= lat <= 5.4 and 115.1 <= lon <= 115.35:
        return 'WLY02'
    if 1.2 <= lat <= 6.75 and 99.5 <= lon <= 104.5:
        return _get_peninsular_zone(lat, lon)
    if 4.0 <= lat <= 7.5 and 115.0 <= lon <= 119.5:
        return _get_sabah_zone(lat, lon)
    if 0.8 <= lat <= 5.0 and 109.0 <= lon <= 115.6:
        return _get_sarawak_zone(lat, lon)
    return None


def _get_peninsular_zone(lat, lon):
    if 6.18 <= lat <= 6.75 and 100.1 <= lon <= 100.5:
        return 'PLS01'
    if 6.15 <= lat <= 6.5 and 99.6 <= lon <= 100.0:
        return 'KDH06'
    if 5.1 <= lat <= 5.55 and 100.15 <= lon <= 100.55:
        return 'PNG01'
    if 5.4 <= lat <= 6.65 and 100.15 <= lon <= 101.15:
        if lat >= 6.0 and lon <= 100.6:
            return 'KDH01'
        elif lon <= 100.75:
            return 'KDH02'
        elif lon >= 100.8 and lat >= 5.6:
            return 'KDH04'
        elif lon >= 100.75 and lat < 5.6:
            return 'KDH05'
        else:
            return 'KDH03'
    if 3.6 <= lat <= 5.85 and 100.4 <= lon <= 101.7:
        if lat >= 5.5:
            return 'PRK04'
        if lat >= 5.0 and lon <= 101.0:
            return 'PRK03'
        if lat >= 4.75 and lon <= 100.85:
            return 'PRK06'
        if lat >= 4.3:
            return 'PRK02'
        if lon <= 101.0:
            return 'PRK05'
        return 'PRK01'
    if 4.6 <= lat <= 6.25 and 101.5 <= lon <= 102.7:
        if lat <= 5.0:
            return 'KTN03'
        return 'KTN01'
    if 4.0 <= lat <= 5.8 and 102.5 <= lon <= 103.6:
        if lat >= 5.2:
            return 'TRG02'
        if lat >= 4.8:
            return 'TRG01'
        if lat >= 4.3:
            return 'TRG03'
        return 'TRG04'
    if 2.95 <= lat <= 3.25 and 101.6 <= lon <= 101.8:
        return 'WLY01'
    if 2.4 <= lat <= 3.15 and 101.7 <= lon <= 102.6:
        if lat <= 2.7:
            return 'NGS01'
        return 'NGS02'
    if 2.0 <= lat <= 2.5 and 102.0 <= lon <= 102.6:
        return 'MLK01'
    if 2.6 <= lat <= 3.9 and 100.85 <= lon <= 102.0:
        if lat >= 3.5 and lon <= 101.5:
            return 'SGR02'
        if lon <= 101.5:
            return 'SGR03'
        return 'SGR01'
    if 2.7 <= lat <= 4.7 and 101.8 <= lon <= 104.0:
        if lat >= 4.3 and lon >= 103.5:
            return 'PHG01'
        if lon >= 103.0:
            return 'PHG02'
        if lat >= 3.8:
            return 'PHG03'
        if lat >= 3.5 and lon <= 102.0:
            return 'PHG06'
        if lat >= 3.3 and lon <= 102.1:
            return 'PHG05'
        return 'PHG04'
    if 1.37 <= lat <= 2.8 and 102.4 <= lon <= 104.5:
        if lon >= 104.0 and lat <= 2.0:
            return 'JHR01'
        if lat >= 2.3:
            return 'JHR04'
        if lon <= 103.2:
            return 'JHR03'
        return 'JHR02'
    return None


def _get_sabah_zone(lat, lon):
    if 5.9 <= lat <= 6.1 and 116.4 <= lon <= 116.7:
        return 'SBH06'
    if lat >= 6.3 and 116.5 <= lon <= 117.5:
        return 'SBH05'
    if lat >= 5.5 and lon <= 116.5:
        return 'SBH07'
    if lat >= 5.5 and lon >= 117.5:
        return 'SBH01'
    if lat >= 5.5 and 116.5 <= lon < 117.5:
        return 'SBH02'
    if lat < 5.5 and lon >= 117.5:
        return 'SBH03'
    if lat < 5.5 and 117.0 <= lon < 117.5:
        return 'SBH04'
    if lat < 5.5 and 116.0 <= lon < 117.0:
        return 'SBH08'
    if lat < 5.5 and lon < 116.0:
        return 'SBH09'
    return 'SBH07'


def _get_sarawak_zone(lat, lon):
    if lat >= 4.0 and lon >= 114.5:
        return 'SWK01'
    if lon >= 113.8:
        return 'SWK02'
    if lon >= 112.8:
        return 'SWK03'
    if lon >= 111.8:
        return 'SWK04'
    if lon >= 111.3:
        return 'SWK05'
    if lon >= 110.8:
        return 'SWK06'
    if lon >= 110.45:
        return 'SWK07'
    return 'SWK08'


# --- Public helpers ---

def get_zone_info(zone_code):
    for state, zones in MALAYSIA_ZONES.items():
        if zone_code in zones:
            return state, zones[zone_code]
    return None, None


def get_malaysia_zone_info(lat, lon):
    zone_code = get_malaysia_zone(lat, lon)
    if zone_code is None:
        return None, None, None
    state, zone_name = get_zone_info(zone_code)
    return zone_code, state, zone_name
