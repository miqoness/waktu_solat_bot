def get_malaysia_zone(lat, lon):
    # Semenanjung Malaysia
    if 1 <= lat <= 6.75:
        # Perlis
        if 100.13 <= lon <= 100.9 and 6.18 <= lat <= 6.7:
            return 'PLS01'
        
        # Kedah
        elif 100.15 <= lon <= 101.15 and 5.4 <= lat <= 6.65:
            if lon <= 100.55:
                return 'KDH01'  # Kota Setar, Kubang Pasu, Pokok Sena
            elif lon <= 100.75:
                return 'KDH02'  # Pendang, Kuala Muda, Yan
            else:
                return 'KDH03'  # Baling, Sik, Padang Terap
        
        # Pulau Pinang
        elif 100.15 <= lon <= 100.55 and 5.1 <= lat <= 5.6:
            return 'PNG01'
        
        # Perak
        elif 100.55 <= lon <= 101.7 and 3.6 <= lat <= 5.85:
            if lat >= 5.25:
                return 'PRK01'  # Hulu Perak
            elif lat >= 4.75:
                return 'PRK02'  # Kerian, Larut & Matang, Selama, Kuala Kangsar, Perak Tengah
            elif lat >= 4.3:
                return 'PRK03'  # Kinta, Kampar
            else:
                return 'PRK04'  # Hilir Perak, Batang Padang, Muallim
        
        # Selangor
        elif 100.85 <= lon <= 102 and 2.6 <= lat <= 3.9:
            if lat >= 3.4:
                return 'SGR01'  # Selangor 1
            else:
                return 'SGR02'  # Selangor 2
        
        # Kuala Lumpur & Putrajaya
        elif 101.6 <= lon <= 101.8 and 2.9 <= lat <= 3.2:
            return 'WLY01'
        
        # Negeri Sembilan
        elif 101.6 <= lon <= 102.7 and 2.4 <= lat <= 3.2:
            if lon <= 102.3:
                return 'NGS01'  # Jempol, Tampin
            else:
                return 'NGS02'  # Port Dickson, Seremban, Kuala Pilah, Jelebu, Rembau
        
        # Melaka
        elif 102 <= lon <= 102.6 and 2.1 <= lat <= 2.5:
            return 'MLK01'
        
        # Johor
        elif 102.5 <= lon <= 104.5 and 1.2 <= lat <= 2.8:
            if lon <= 103.5:
                return 'JHR01'  # Pulau Aur dan Pemanggil
            elif lat >= 2.4:
                return 'JHR02'  # Kota Tinggi, Mersing, Johor Bahru
            elif lon <= 103.2:
                return 'JHR03'  # Kluang, Pontian
            else:
                return 'JHR04'  # Batu Pahat, Muar, Segamat, Tangkak
        
        # Pahang
        elif 101.3 <= lon <= 104 and 2.7 <= lat <= 4.7:
            if lon <= 102.5:
                return 'PHG01'  # Pulau Tioman
            elif lon <= 103:
                return 'PHG02'  # Kuantan, Pekan, Rompin, Muadzam Shah
            elif lat >= 3.8:
                return 'PHG03'  # Maran, Jerantut, Temerloh, Bera
            else:
                return 'PHG04'  # Cameron Highlands, Genting Sempah, Bukit Fraser
        
        # Terengganu
        elif 102.5 <= lon <= 104 and 4 <= lat <= 5.8:
            if lat >= 5:
                return 'TRG01'  # Kuala Terengganu, Marang
            else:
                return 'TRG02'  # Dungun, Kemaman
        
        # Kelantan
        elif 101.5 <= lon <= 102.7 and 4.6 <= lat <= 6.25:
            if lat >= 5.8:
                return 'KTN01'  # Jeli, Gua Musang (Mukim Galas)
            else:
                return 'KTN02'  # Kota Bharu, Bachok, Pasir Puteh, Tumpat, Pasir Mas, Tanah Merah, Machang, Kuala Krai, Gua Musang (Mukim Chiku)
    
    # Sabah
    elif 4 <= lat <= 7.5 and 115 <= lon <= 120:
        if 116 <= lon <= 117 and 5 <= lat <= 7:
            return 'SBH01'  # Zon 1 - Timur
        else:
            return 'SBH02'  # Zon 2 - Barat
    
    # Sarawak
    elif 0.8 <= lat <= 5 and 109 <= lon <= 115.6:
        if lon <= 112:
            return 'SRW01'  # Zon 1 - Kuching, Samarahan, Serian, Sri Aman, Betong, Sarikei
        elif lon <= 113.2:
            return 'SRW02'  # Zon 2 - Sibu, Kapit, Mukah
        else:
            return 'SRW03'  # Zon 3 - Miri, Bintulu, Limbang
    
    # Wilayah Persekutuan Labuan
    elif 5.2 <= lat <= 5.4 and 115.1 <= lon <= 115.3:
        return 'WLY02'
    
    # Default jika tidak dapat menentukan zon
    return 'WLY01'  # Default ke Wilayah Persekutuan sebagai langkah keselamatan