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


def get_malaysia_zone(lat, lon):
    # Wilayah Persekutuan Labuan (check first — small island)
    if 5.2 <= lat <= 5.4 and 115.1 <= lon <= 115.35:
        return 'WLY02'

    # Semenanjung Malaysia
    if 1.2 <= lat <= 6.75 and 99.5 <= lon <= 104.5:
        return _get_peninsular_zone(lat, lon)

    # Sabah
    if 4.0 <= lat <= 7.5 and 115.0 <= lon <= 119.5:
        return _get_sabah_zone(lat, lon)

    # Sarawak
    if 0.8 <= lat <= 5.0 and 109.0 <= lon <= 115.6:
        return _get_sarawak_zone(lat, lon)

    return None


def _get_peninsular_zone(lat, lon):
    # Perlis
    if 6.18 <= lat <= 6.75 and 100.1 <= lon <= 100.5:
        return 'PLS01'

    # Langkawi
    if 6.15 <= lat <= 6.5 and 99.6 <= lon <= 100.0:
        return 'KDH06'

    # Pulau Pinang (check before Kedah — overlapping lat/lon)
    if 5.1 <= lat <= 5.55 and 100.15 <= lon <= 100.55:
        return 'PNG01'

    # Kedah
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

    # Perak
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

    # Kelantan
    if 4.6 <= lat <= 6.25 and 101.5 <= lon <= 102.7:
        if lat <= 5.0:
            return 'KTN03'
        return 'KTN01'

    # Terengganu
    if 4.0 <= lat <= 5.8 and 102.5 <= lon <= 103.6:
        if lat >= 5.2:
            return 'TRG02'
        if lat >= 4.8:
            return 'TRG01'
        if lat >= 4.3:
            return 'TRG03'
        return 'TRG04'

    # Kuala Lumpur & Putrajaya (check before Pahang/Selangor — small area inside their bounds)
    if 2.95 <= lat <= 3.25 and 101.6 <= lon <= 101.8:
        return 'WLY01'

    # Negeri Sembilan (check before Pahang — overlapping lon range)
    if 2.4 <= lat <= 3.15 and 101.7 <= lon <= 102.6:
        if lat <= 2.7:
            return 'NGS01'
        return 'NGS02'

    # Melaka
    if 2.0 <= lat <= 2.5 and 102.0 <= lon <= 102.6:
        return 'MLK01'

    # Selangor
    if 2.6 <= lat <= 3.9 and 100.85 <= lon <= 102.0:
        if lat >= 3.5 and lon <= 101.5:
            return 'SGR02'
        if lon <= 101.5:
            return 'SGR03'
        return 'SGR01'

    # Pahang
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

    # Johor (1.37 excludes Singapore)
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
    # Gunung Kinabalu (specific)
    if 5.9 <= lat <= 6.1 and 116.4 <= lon <= 116.7:
        return 'SBH06'

    # Kudat
    if lat >= 6.3 and 116.5 <= lon <= 117.5:
        return 'SBH05'

    # Kota Kinabalu / west coast
    if lat >= 5.5 and lon <= 116.5:
        return 'SBH07'

    # Sandakan east
    if lat >= 5.5 and lon >= 117.5:
        return 'SBH01'

    # Sandakan west
    if lat >= 5.5 and 116.5 <= lon < 117.5:
        return 'SBH02'

    # Tawau east
    if lat < 5.5 and lon >= 117.5:
        return 'SBH03'

    # Tawau west
    if lat < 5.5 and 117.0 <= lon < 117.5:
        return 'SBH04'

    # Interior upper (Keningau)
    if lat < 5.5 and 116.0 <= lon < 117.0:
        return 'SBH08'

    # Interior lower (Beaufort)
    if lat < 5.5 and lon < 116.0:
        return 'SBH09'

    return 'SBH07'


def _get_sarawak_zone(lat, lon):
    # Limbang, Lawas
    if lat >= 4.0 and lon >= 114.5:
        return 'SWK01'

    # Miri
    if lon >= 113.8:
        return 'SWK02'

    # Bintulu
    if lon >= 112.8:
        return 'SWK03'

    # Sibu, Kapit
    if lon >= 111.8:
        return 'SWK04'

    # Sarikei
    if lon >= 111.3:
        return 'SWK05'

    # Sri Aman, Betong
    if lon >= 110.8:
        return 'SWK06'

    # Serian, Samarahan
    if lon >= 110.45:
        return 'SWK07'

    # Kuching
    return 'SWK08'


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
