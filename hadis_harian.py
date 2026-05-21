import requests
from deep_translator import GoogleTranslator


def get_daily_hadith():
    try:
        response = requests.get("https://hadis-api-id.vercel.app/hadith/random", timeout=10)
        if response.status_code != 200:
            return "Maaf, tidak dapat mendapatkan hadith pada masa ini. Sila cuba lagi kemudian."

        data = response.json()
        translator = GoogleTranslator(source='id', target='ms')

        narrator = data['data']['narrator']
        narrator_ms = translator.translate(narrator)

        translation = data['data']['translation']
        translation_ms = translator.translate(translation)

        text = data['data']['text']
        reference = f"{data['data']['book']} No. {data['data']['number']}"

        hadith = f"*Hadith Harian*\n\n"
        hadith += f"*Perawi:* {narrator_ms}\n\n"
        hadith += f"*Teks Arab:*\n{text}\n\n"
        hadith += f"*Terjemahan:*\n{translation_ms}\n\n"
        hadith += f"*Rujukan:* {reference}"

        return hadith
    except Exception as e:
        print(f"Error getting hadith: {e}")
        return "Maaf, tidak dapat mendapatkan hadith pada masa ini. Sila cuba lagi kemudian."


def send_daily_hadith(bot, message):
    hadith = get_daily_hadith()
    bot.reply_to(message, hadith, parse_mode='Markdown')
