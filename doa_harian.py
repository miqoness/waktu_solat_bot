from datetime import datetime
from pytz import timezone

DOAS = [
    {
        'title': 'Doa Sebelum Tidur',
        'arab': 'بِاسْمِكَ اللَّهُمَّ أَمُوتُ وَأَحْيَا',
        'rumi': "Bismikallahumma amutu wa ahya",
        'maksud': 'Dengan nama-Mu ya Allah, aku mati dan aku hidup.',
    },
    {
        'title': 'Doa Bangun Tidur',
        'arab': 'اَلْحَمْدُ لِلَّهِ الَّذِيْ أَحْيَانَا بَعْدَ مَا أَمَاتَنَا وَإِلَيْهِ النُّشُوْرُ',
        'rumi': "Alhamdu lillahil-ladhi ahyana ba'da ma amatana wa ilayhin-nushur",
        'maksud': 'Segala puji bagi Allah yang menghidupkan kami setelah mematikan kami, dan kepada-Nya kami dikembalikan.',
    },
    {
        'title': 'Doa Masuk Tandas',
        'arab': 'اللَّهُمَّ إِنِّي أَعُوذُ بِكَ مِنَ الْخُبُثِ وَالْخَبَائِثِ',
        'rumi': "Allahumma inni a'udzu bika minal khubutsi wal khaba'its",
        'maksud': 'Ya Allah, aku berlindung kepada-Mu daripada syaitan jantan dan syaitan betina.',
    },
    {
        'title': 'Doa Keluar Tandas',
        'arab': 'غُفْرَانَكَ',
        'rumi': "Ghufranaka",
        'maksud': 'Aku memohon keampunan-Mu.',
    },
    {
        'title': 'Doa Sebelum Makan',
        'arab': 'بِسْمِ اللَّهِ وَعَلَى بَرَكَةِ اللَّهِ',
        'rumi': "Bismillahi wa 'ala barakatillah",
        'maksud': 'Dengan nama Allah dan dengan berkat Allah.',
    },
    {
        'title': 'Doa Selepas Makan',
        'arab': 'اَلْحَمْدُ لِلَّهِ الَّذِيْ أَطْعَمَنَا وَسَقَانَا وَجَعَلَنَا مِنَ الْمُسْلِمِيْنَ',
        'rumi': "Alhamdu lillahil-ladhi at'amana wa saqana wa ja'alana minal muslimin",
        'maksud': 'Segala puji bagi Allah yang memberi kami makan dan minum serta menjadikan kami orang Islam.',
    },
    {
        'title': 'Doa Keluar Rumah',
        'arab': 'بِسْمِ اللَّهِ تَوَكَّلْتُ عَلَى اللَّهِ لَا حَوْلَ وَلَا قُوَّةَ إِلَّا بِاللَّهِ',
        'rumi': "Bismillahi tawakkaltu 'alallah, la hawla wa la quwwata illa billah",
        'maksud': 'Dengan nama Allah, aku bertawakkal kepada Allah. Tiada daya dan upaya melainkan dengan pertolongan Allah.',
    },
    {
        'title': 'Doa Masuk Rumah',
        'arab': 'بِسْمِ اللَّهِ وَلَجْنَا وَبِسْمِ اللَّهِ خَرَجْنَا وَعَلَى رَبِّنَا تَوَكَّلْنَا',
        'rumi': "Bismillahi walajna, wa bismillahi kharajna, wa 'ala Rabbina tawakkalna",
        'maksud': 'Dengan nama Allah kami masuk, dengan nama Allah kami keluar, dan kepada Tuhan kami, kami bertawakkal.',
    },
    {
        'title': 'Doa Masuk Masjid',
        'arab': 'اللَّهُمَّ افْتَحْ لِي أَبْوَابَ رَحْمَتِكَ',
        'rumi': "Allahummaf-tah li abwaba rahmatik",
        'maksud': 'Ya Allah, bukakanlah untukku pintu-pintu rahmat-Mu.',
    },
    {
        'title': 'Doa Keluar Masjid',
        'arab': 'اللَّهُمَّ إِنِّي أَسْأَلُكَ مِنْ فَضْلِكَ',
        'rumi': "Allahumma inni as'aluka min fadlik",
        'maksud': 'Ya Allah, sesungguhnya aku memohon kepada-Mu daripada kelebihan-Mu.',
    },
    {
        'title': 'Doa Ketika Hujan',
        'arab': 'اللَّهُمَّ صَيِّبًا نَافِعًا',
        'rumi': "Allahumma sayyiban nafi'an",
        'maksud': 'Ya Allah, turunkan hujan yang bermanfaat.',
    },
    {
        'title': 'Doa Selepas Azan',
        'arab': 'اللَّهُمَّ رَبَّ هَذِهِ الدَّعْوَةِ التَّامَّةِ وَالصَّلَاةِ الْقَائِمَةِ آتِ مُحَمَّدًا الْوَسِيلَةَ وَالْفَضِيلَةَ وَابْعَثْهُ مَقَامًا مَحْمُودًا الَّذِي وَعَدْتَهُ',
        'rumi': "Allahumma Rabba hadhihid-da'watit-tammah, was-salatil-qa'imah, ati Muhammadanil-wasilata wal-fadilah, wab'athhu maqamam mahmudanil-ladhi wa'adtah",
        'maksud': 'Ya Allah, Tuhan yang memiliki seruan yang sempurna ini dan solat yang ditegakkan, berikanlah kepada Muhammad wasilah dan kelebihan, dan bangkitkanlah dia ke tempat yang terpuji seperti yang Engkau janjikan.',
    },
    {
        'title': 'Doa Mohon Kebaikan Dunia Akhirat',
        'arab': 'رَبَّنَا آتِنَا فِي الدُّنْيَا حَسَنَةً وَفِي الْآخِرَةِ حَسَنَةً وَقِنَا عَذَابَ النَّارِ',
        'rumi': "Rabbana atina fid-dunya hasanatan wa fil-akhirati hasanatan waqina 'adhabannar",
        'maksud': 'Ya Tuhan kami, berilah kami kebaikan di dunia dan kebaikan di akhirat, dan peliharalah kami daripada azab neraka.',
    },
    {
        'title': 'Doa Minta Petunjuk',
        'arab': 'اللَّهُمَّ اهْدِنِي وَسَدِّدْنِي',
        'rumi': "Allahummah-dini wa saddidni",
        'maksud': 'Ya Allah, tunjukkanlah aku dan luruskanlah aku.',
    },
    {
        'title': 'Doa Memohon Ampun',
        'arab': 'رَبِّ اغْفِرْ لِي وَتُبْ عَلَيَّ إِنَّكَ أَنْتَ التَّوَّابُ الرَّحِيمُ',
        'rumi': "Rabbighfir li wa tub 'alayya innaka antat-Tawwabur-Rahim",
        'maksud': 'Ya Tuhanku, ampunilah aku dan terimalah taubatku. Sesungguhnya Engkau Maha Penerima Taubat lagi Maha Penyayang.',
    },
    {
        'title': 'Doa Menaiki Kenderaan',
        'arab': 'سُبْحَانَ الَّذِي سَخَّرَ لَنَا هَذَا وَمَا كُنَّا لَهُ مُقْرِنِينَ وَإِنَّا إِلَى رَبِّنَا لَمُنْقَلِبُونَ',
        'rumi': "Subhanalladhi sakh-khara lana hadha wa ma kunna lahu muqrinin wa inna ila Rabbina lamunqalibun",
        'maksud': 'Maha Suci Tuhan yang memudahkan semua ini untuk kami sedangkan kami tidak mampu menguasainya, dan sesungguhnya kami akan kembali kepada Tuhan kami.',
    },
    {
        'title': 'Doa Ketika Bermusafir',
        'arab': 'اللَّهُمَّ إِنَّا نَسْأَلُكَ فِي سَفَرِنَا هَذَا الْبِرَّ وَالتَّقْوَى',
        'rumi': "Allahumma inna nas'aluka fi safarina hadhal-birra wat-taqwa",
        'maksud': 'Ya Allah, sesungguhnya kami memohon kepada-Mu dalam perjalanan ini kebajikan dan ketaqwaan.',
    },
    {
        'title': 'Doa Untuk Ibu Bapa',
        'arab': 'رَبِّ ارْحَمْهُمَا كَمَا رَبَّيَانِي صَغِيرًا',
        'rumi': "Rabbir-hamhuma kama rabbayani saghira",
        'maksud': 'Ya Tuhanku, rahmatilah mereka berdua sebagaimana mereka memeliharaku sewaktu kecil.',
    },
    {
        'title': 'Doa Pagi Hari',
        'arab': 'اللَّهُمَّ بِكَ أَصْبَحْنَا وَبِكَ أَمْسَيْنَا وَبِكَ نَحْيَا وَبِكَ نَمُوتُ وَإِلَيْكَ النُّشُورُ',
        'rumi': "Allahumma bika asbahna, wa bika amsayna, wa bika nahya, wa bika namutu, wa ilaykan-nushur",
        'maksud': 'Ya Allah, dengan-Mu kami memasuki waktu pagi, dengan-Mu kami memasuki waktu petang, dengan-Mu kami hidup, dengan-Mu kami mati, dan kepada-Mu tempat kembali.',
    },
    {
        'title': 'Doa Petang Hari',
        'arab': 'اللَّهُمَّ بِكَ أَمْسَيْنَا وَبِكَ أَصْبَحْنَا وَبِكَ نَحْيَا وَبِكَ نَمُوتُ وَإِلَيْكَ الْمَصِيرُ',
        'rumi': "Allahumma bika amsayna, wa bika asbahna, wa bika nahya, wa bika namutu, wa ilaykal-masir",
        'maksud': 'Ya Allah, dengan-Mu kami memasuki waktu petang, dengan-Mu kami memasuki waktu pagi, dengan-Mu kami hidup, dengan-Mu kami mati, dan kepada-Mu tempat kembali.',
    },
    {
        'title': 'Doa Minta Ilmu',
        'arab': 'رَبِّ زِدْنِي عِلْمًا',
        'rumi': "Rabbi zidni 'ilma",
        'maksud': 'Ya Tuhanku, tambahkanlah ilmu kepadaku.',
    },
    {
        'title': 'Doa Ketika Susah',
        'arab': 'لَا إِلَهَ إِلَّا أَنْتَ سُبْحَانَكَ إِنِّي كُنْتُ مِنَ الظَّالِمِينَ',
        'rumi': "La ilaha illa Anta, Subhanaka inni kuntu minaz-zalimin",
        'maksud': 'Tiada Tuhan melainkan Engkau, Maha Suci Engkau, sesungguhnya aku adalah antara orang-orang yang zalim.',
    },
    {
        'title': 'Doa Minta Perlindungan',
        'arab': 'اللَّهُمَّ إِنِّي أَعُوذُ بِكَ مِنَ الْهَمِّ وَالْحُزْنِ',
        'rumi': "Allahumma inni a'udhu bika minal-hammi wal-hazan",
        'maksud': 'Ya Allah, aku berlindung kepada-Mu daripada kegelisahan dan kesedihan.',
    },
    {
        'title': 'Doa Sebelum Belajar',
        'arab': 'اللَّهُمَّ انْفَعْنِي بِمَا عَلَّمْتَنِي وَعَلِّمْنِي مَا يَنْفَعُنِي وَزِدْنِي عِلْمًا',
        'rumi': "Allahumman-fa'ni bima 'allamtani, wa 'allimni ma yanfa'uni, wa zidni 'ilma",
        'maksud': 'Ya Allah, manfaatkanlah apa yang Engkau ajarkan kepadaku, ajarkanlah aku apa yang bermanfaat, dan tambahkanlah ilmu kepadaku.',
    },
    {
        'title': 'Doa Minta Kesihatan',
        'arab': 'اللَّهُمَّ عَافِنِي فِي بَدَنِي اللَّهُمَّ عَافِنِي فِي سَمْعِي اللَّهُمَّ عَافِنِي فِي بَصَرِي',
        'rumi': "Allahumma 'afini fi badani, Allahumma 'afini fi sam'i, Allahumma 'afini fi basari",
        'maksud': 'Ya Allah, sihatkan badanku. Ya Allah, sihatkan pendengaranku. Ya Allah, sihatkan penglihatanku.',
    },
    {
        'title': 'Doa Ketika Bercermin',
        'arab': 'اللَّهُمَّ كَمَا حَسَّنْتَ خَلْقِي فَحَسِّنْ خُلُقِي',
        'rumi': "Allahumma kama hassanta khalqi fa hassin khuluqi",
        'maksud': 'Ya Allah, sebagaimana Engkau cantikkan rupaku, maka cantikkanlah akhlakku.',
    },
    {
        'title': 'Doa Minta Rezeki',
        'arab': 'اللَّهُمَّ إِنِّي أَسْأَلُكَ عِلْمًا نَافِعًا وَرِزْقًا طَيِّبًا وَعَمَلًا مُتَقَبَّلًا',
        'rumi': "Allahumma inni as'aluka 'ilman nafi'an, wa rizqan tayyiban, wa 'amalan mutaqabbalan",
        'maksud': 'Ya Allah, aku memohon kepada-Mu ilmu yang bermanfaat, rezeki yang baik, dan amalan yang diterima.',
    },
    {
        'title': 'Doa Sebelum Solat',
        'arab': 'اللَّهُمَّ بَاعِدْ بَيْنِي وَبَيْنَ خَطَايَايَ كَمَا بَاعَدْتَ بَيْنَ الْمَشْرِقِ وَالْمَغْرِبِ',
        'rumi': "Allahumma ba'id bayni wa bayna khatayaya kama ba'adta baynal-mashriqi wal-maghrib",
        'maksud': 'Ya Allah, jauhkanlah antaraku dengan kesalahan-kesalahanku sebagaimana Engkau jauhkan antara timur dan barat.',
    },
    {
        'title': 'Doa Selepas Solat',
        'arab': 'اللَّهُمَّ أَعِنِّي عَلَى ذِكْرِكَ وَشُكْرِكَ وَحُسْنِ عِبَادَتِكَ',
        'rumi': "Allahumma a'inni 'ala dhikrika wa shukrika wa husni 'ibadatik",
        'maksud': 'Ya Allah, bantulah aku untuk mengingati-Mu, bersyukur kepada-Mu, dan memperbaiki ibadah kepada-Mu.',
    },
]


def get_daily_doa():
    malaysia_tz = timezone('Asia/Kuala_Lumpur')
    today = datetime.now(malaysia_tz)
    index = today.timetuple().tm_yday % len(DOAS)
    doa = DOAS[index]

    result = f"🤲 *Doa Harian*\n\n"
    result += f"📖 *{doa['title']}*\n\n"
    result += f"*Arab:*\n{doa['arab']}\n\n"
    result += f"*Rumi:*\n_{doa['rumi']}_\n\n"
    result += f"*Maksud:*\n{doa['maksud']}"

    return result


def send_daily_doa(bot, message):
    doa = get_daily_doa()
    bot.reply_to(message, doa, parse_mode='Markdown')
