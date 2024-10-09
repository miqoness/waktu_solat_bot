# hadis_harian.py

import requests
from googletrans import Translator

def get_daily_hadith():
    # Dapatkan hadith secara rawak
    response = requests.get("https://hadis-api-id.vercel.app/hadith/random")
    if response.status_code == 200:
        data = response.json()
        
        # Terjemah ke Bahasa Melayu
        translator = Translator()
        
        narrator = data['data']['narrator']
        narrator_ms = translator.translate(narrator, src='id', dest='ms').text
        
        text = data['data']['text']
        text_ms = translator.translate(text, src='id', dest='ms').text
        
        translation = data['data']['translation']
        translation_ms = translator.translate(translation, src='id', dest='ms').text
        
        reference = f"{data['data']['book']} No. {data['data']['number']}"
        
        hadith = f"*Hadith Harian*\n\n"
        hadith += f"*Perawi:* {narrator_ms}\n\n"
        hadith += f"*Teks Arab:*\n{text}\n\n"
        hadith += f"*Terjemahan:*\n{translation_ms}\n\n"
        hadith += f"*Rujukan:* {reference}"
        
        return hadith
    else:
        return "Maaf, tidak dapat mendapatkan hadith pada masa ini. Sila cuba lagi kemudian."

def send_daily_hadith(bot, message):
    hadith = get_daily_hadith()
    bot.reply_to(message, hadith, parse_mode='Markdown')