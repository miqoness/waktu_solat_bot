import telebot
import logging
from config import BOT_TOKEN
from bot_handlers import register_handlers
from prayer_times import start_prayer_scheduler
from database import init_db
import threading

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting the bot...")
    # Inisialisasi pangkalan data
    init_db()

    bot = telebot.TeleBot(BOT_TOKEN)
    register_handlers(bot)
    
    # Jalankan bot dalam thread utama
    bot_thread = threading.Thread(target=bot.polling, kwargs={'none_stop': True, 'interval': 0, 'timeout': 20})
    bot_thread.start()
    logger.info("Bot polling thread started")
    
    # Jalankan penjadual dalam thread berasingan
    schedule_thread = threading.Thread(target=start_prayer_scheduler, args=(bot,))
    schedule_thread.start()
    logger.info("Prayer scheduler thread started")
    
    # Tunggu kedua-dua thread selesai (ini tidak akan berlaku kecuali bot dihentikan)
    bot_thread.join()
    schedule_thread.join()

if __name__ == "__main__":
    main()