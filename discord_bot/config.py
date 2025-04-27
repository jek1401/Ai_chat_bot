import os

# Параметры для бота
TOKEN = 'YOUR_BOT_TOKEN'

# Параметры базы данных
DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'users.db')
# В случае, если база данных уже находится в папке `bots`
DB_PATH = "bots/users.db"

# Стоимость голосовой команды
VOICE_COST = 5

# Активные сессии
active_sessions = {}

# Список персональностей
personalities_list = [
    "Hacker", "Gopnik", "Professor", "Robot", "CoolGuy", "MafiaBoss", "RussianBear"
]

# Список голосов
voices = [
    "alloy", "echo", "fable", "onyx", "nova", "shimmer",
    "coral", "verse", "ballad", "ash", "sage",
    "amuch", "aster", "brook", "clover", "dan", "elan",
    "marilyn", "meadow", "jazz", "rio", "jade-hardy", "megan-wetherall"
]
