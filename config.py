import os

# Guna path absolut untuk database
DATABASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'users.db')

BOT_TOKEN = '7547222355:AAF73e4_24YqE-0IBmhnhKu0fyagCNxo9Ts'
PRAYER_API_URL = 'https://api.aladhan.com/v1/timings/'
JAKIM_API_URL = 'https://www.e-solat.gov.my/index.php?r=esolatApi/takwimsolat'
CHECK_INTERVAL = 60