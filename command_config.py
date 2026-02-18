# ============================================
# КОНФІГУРАЦІЯ КОМАНД - РЕДАГУЙ ТУТ!
# ============================================
# Тут ти можеш налаштувати:
# - Які слова/фрази активують команди
# - Шляхи до програм
# - Налаштування пошуку
# ============================================

# --- НАЛАШТУВАННЯ ШЛЯХІВ ДО ПРОГРАМ --- 
# Important: Write your own path to files
APPS = {
    "steam": r"C:\Program Files (x86)\Steam\Steam.exe",
    "discord": r"C:\Users\danyl\AppData\Local\Discord\Update.exe --processStart Discord.exe",
    "telegram": r"C:\Users\danyl\AppData\Roaming\Telegram Desktop\Telegram.exe",
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "firefox": r"C:\Program Files\Mozilla Firefox\firefox.exe",
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "explorer": "explorer.exe",
    "spotify": r"C:\Users\danyl\AppData\Roaming\Spotify\Spotify.exe",
    "vscode": r"C:\Users\danyl\AppData\Local\Programs\Microsoft VS Code\Code.exe",
}

# --- НАЛАШТУВАННЯ ВЕБСАЙТІВ ---
WEBSITES = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "github": "https://github.com",
    "digitec": "https://www.digitec.ch",
    "gmail": "https://mail.google.com",
    "twitch": "https://www.twitch.tv",
}

# --- URL ДЛЯ ПОШУКУ ---
SEARCH_ENGINES = {
    "google": "https://www.google.com/search?q=",
    "youtube": "https://www.youtube.com/results?search_query=",
    "digitec": "https://www.digitec.ch/search?q=",
}
DEFAULT_SEARCH_ENGINE = "google"

# --- STEAM ІГРИ (назва -> app_id) ---
# Знайти app_id: https://steamdb.info/
STEAM_GAMES = {
    "cs2": "730",
    "dota 2": "570",
    "gta 5": "271590",
    "pubg": "578080",
    "rust": "252490",
    "terraria": "105600",
    "arc raiders": "1808500",
    "detroid become human": "1222140",
    "war thunder": "236390",
    "Asseto Corza Competizione": "805550",
    "The Finals": "2073850",
    "F1 25": "3059520",


}

# ============================================
# РОЗПІЗНАВАННЯ ПРИРОДНОЇ МОВИ
# ============================================
# Формат: "ключове слово/фраза" -> ("тип_команди", "параметр")
# Типи команд: "open_app", "open_website", "search", "steam_game", "exit"
# 
# ПОРАДИ:
# - Додавай варіанти написання (укр/англ, з помилками)
# - Чим більше варіантів - тим краще розпізнавання
# ============================================

NATURAL_LANGUAGE_COMMANDS = {
    # --- ВИХІД ---
    "вийти": ("exit", None),
    "вийди": ("exit", None),
    "закрийся": ("exit", None),
    "пока": ("exit", None),
    "бувай": ("exit", None),
    "exit": ("exit", None),
    "quit": ("exit", None),
    "bye": ("exit", None),
    
    # --- STEAM ---
    "відкрий стім": ("open_app", "steam"),
    "відкрий steam": ("open_app", "steam"),
    "запусти стім": ("open_app", "steam"),
    "запусти steam": ("open_app", "steam"),
    "open steam": ("open_app", "steam"),
    
    # --- DISCORD ---
    "відкрий дискорд": ("open_app", "discord"),
    "відкрий discord": ("open_app", "discord"),
    "запусти дискорд": ("open_app", "discord"),
    "open discord": ("open_app", "discord"),
    
    # --- TELEGRAM ---
    "відкрий телеграм": ("open_app", "telegram"),
    "відкрий telegram": ("open_app", "telegram"),
    "запусти телеграм": ("open_app", "telegram"),
    
    # --- CHROME ---
    "відкрий браузер": ("open_app", "chrome"),
    "відкрий хром": ("open_app", "chrome"),
    "відкрий chrome": ("open_app", "chrome"),
    "open browser": ("open_app", "chrome"),
    "open chrome": ("open_app", "chrome"),
    
    # --- YOUTUBE ---
    "відкрий ютуб": ("open_website", "youtube"),
    "відкрий youtube": ("open_website", "youtube"),
    "open youtube": ("open_website", "youtube"),
    
    # --- ІНШІ САЙТИ ---
    "відкрий гугл": ("open_website", "google"),
    "відкрий google": ("open_website", "google"),
    "відкрий github": ("open_website", "github"),
    "відкрий гітхаб": ("open_website", "github"),
    "відкрий твіттер": ("open_website", "twitter"),
    "відкрий twitter": ("open_website", "twitter"),
    "відкрий редіт": ("open_website", "reddit"),
    "відкрий reddit": ("open_website", "reddit"),
    "відкрий twitch": ("open_website", "twitch"),
    "відкрий твіч": ("open_website", "twitch"),
    "відкрити digitec": ("open_website", "digitec"),
    "відкрити "
    
    # --- КАЛЬКУЛЯТОР ---
    "відкрий калькулятор": ("open_app", "calculator"),
    "калькулятор": ("open_app", "calculator"),
    "open calculator": ("open_app", "calculator"),
    
    # --- NOTEPAD ---
    "відкрий блокнот": ("open_app", "notepad"),
    "блокнот": ("open_app", "notepad"),
    "open notepad": ("open_app", "notepad"),
    
    # --- ПРОВІДНИК ---
    "відкрий провідник": ("open_app", "explorer"),
    "відкрий файли": ("open_app", "explorer"),
    "open explorer": ("open_app", "explorer"),
    "open files": ("open_app", "explorer"),
    
    # --- SPOTIFY ---
    "відкрий спотіфай": ("open_app", "spotify"),
    "відкрий spotify": ("open_app", "spotify"),
    "музика": ("open_app", "spotify"),
    
    # --- VS CODE ---
    "відкрий vscode": ("open_app", "vscode"),
    "відкрий код": ("open_app", "vscode"),
    "open vscode": ("open_app", "vscode"),
}

# --- ПАТЕРНИ ДЛЯ ДИНАМІЧНИХ КОМАНД ---
# Ці патерни допомагають розпізнавати команди з параметрами
# Наприклад: "знайди котиків" -> search("котиків")
SEARCH_TRIGGERS = [
    "знайди", "знайти", "пошукай", "пошук", "шукай",
    "загугли", "погугли", "google", "search", "find",
    "шукати", "найди", "найти",
]

PLAY_GAME_TRIGGERS = [
    "запусти гру", "запусти", "пограй в", "пограти в",
    "грати в", "play", "launch game", "start game",
    "включи гру", "включи",
]

OPEN_TRIGGERS = [
    "відкрий", "открой", "open", "запусти", "launch", "start",
]

# --- НАЛАШТУВАННЯ МОВИ ---
LANGUAGE = "uk"  # "uk" для української, "en" для англійської

# --- ПОВІДОМЛЕННЯ ---
MESSAGES = {
    "uk": {
        "app_opened": "Відкриваю {app}...",
        "app_not_found": "Не знайшов програму: {app}",
        "website_opened": "Відкриваю {site}...",
        "searching": "Шукаю: {query}...",
        "game_launched": "Запускаю гру: {game}...",
        "game_not_found": "Не знайшов гру: {game}. Спробуй додати її в STEAM_GAMES в command_config.py",
        "command_not_recognized": "Не зрозумів команду. Спробуй ще раз.",
        "goodbye": "Бувай! До зустрічі!",
    },
    "en": {
        "app_opened": "Opening {app}...",
        "app_not_found": "App not found: {app}",
        "website_opened": "Opening {site}...",
        "searching": "Searching for: {query}...",
        "game_launched": "Launching game: {game}...",
        "game_not_found": "Game not found: {game}. Try adding it to STEAM_GAMES in command_config.py",
        "command_not_recognized": "Command not recognized. Try again.",
        "goodbye": "Goodbye! See you later!",
    }
}

def get_message(key, **kwargs):
    """Отримати повідомлення поточною мовою"""
    msg = MESSAGES.get(LANGUAGE, MESSAGES["uk"]).get(key, key)
    return msg.format(**kwargs) if kwargs else msg
