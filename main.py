import telebot
import logging
from config import BOT_TOKEN
from bot_handlers import register_handlers
from prayer_times import start_prayer_scheduler
from database import init_db
import threading

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def main():
    logger.info("Starting the bot...")
    init_db()

    bot = telebot.TeleBot(BOT_TOKEN)
    register_handlers(bot)

    bot_thread = threading.Thread(target=bot.polling, kwargs={'none_stop': True, 'interval': 0, 'timeout': 20})
    bot_thread.start()
    logger.info("Bot polling thread started")

    schedule_thread = threading.Thread(target=start_prayer_scheduler, args=(bot,), daemon=True)
    schedule_thread.start()
    logger.info("Prayer scheduler thread started")

    bot_thread.join()


if __name__ == "__main__":
    main()
