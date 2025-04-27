import os

# Токен бота Telegram
TOKEN = 'YOUR_BOT_TOKEN'

# Путь к базе данных
DB_DIR = os.path.join(os.path.dirname(__file__), 'data')
DB_PATH = os.path.join(DB_DIR, 'users.db')

# Создаем папку data, если ее нет
os.makedirs(DB_DIR, exist_ok=True)

# Остальные настройки...
VOICE_COST = 5
personalities_list = [
    "Hacker", "Gopnik", "Professor", "Robot", "CoolGuy", "MafiaBoss", "RussianBear"
]
voices = [
    "alloy", "echo", "fable", "onyx", "nova", "shimmer",
    "coral", "verse", "ballad", "ash", "sage",
    "amuch", "aster", "brook", "clover", "dan", "elan",
    "marilyn", "meadow", "jazz", "rio", "jade-hardy", "megan-wetherall"
]