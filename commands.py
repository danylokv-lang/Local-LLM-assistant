import os
import subprocess
import webbrowser
from command_config import (
    APPS, WEBSITES, SEARCH_ENGINES, DEFAULT_SEARCH_ENGINE,
    STEAM_GAMES, NATURAL_LANGUAGE_COMMANDS,
    SEARCH_TRIGGERS, PLAY_GAME_TRIGGERS, OPEN_TRIGGERS,
    get_message
)

class CommandHandler:
    """
    Обробник команд з підтримкою природної мови.
    
    Використання:
        handler = CommandHandler()
        result = handler.process("відкрий стім")
        # result = {"executed": True, "response": "Відкриваю steam..."}
    """
    
    def __init__(self):
        # Кеш для швидшого пошуку
        self._build_lookup_tables()
    
    def _build_lookup_tables(self):
        """Побудувати таблиці для швидкого пошуку"""
        # Нормалізовані команди (lowercase)
        self.normalized_commands = {
            k.lower(): v for k, v in NATURAL_LANGUAGE_COMMANDS.items()
        }
        
        # Нормалізовані назви програм
        self.normalized_apps = {k.lower(): v for k, v in APPS.items()}
        
        # Нормалізовані назви сайтів
        self.normalized_websites = {k.lower(): v for k, v in WEBSITES.items()}
        
        # Нормалізовані назви ігор
        self.normalized_games = {k.lower(): v for k, v in STEAM_GAMES.items()}
    
    def process(self, user_input: str) -> dict:
        """
        Обробити введення користувача.
        
        Повертає:
            {
                "executed": bool,  # Чи була виконана команда
                "response": str,   # Відповідь/результат
                "type": str        # Тип команди або "chat" якщо не команда
            }
        """
        original_input = user_input.strip()
        normalized = original_input.lower()
        
        # 1. Перевірка прямих команд (/open, /steam, тощо)
        if original_input.startswith("/"):
            return self._handle_slash_command(original_input)
        
        # 2. Перевірка точного співпадіння з природною мовою
        if normalized in self.normalized_commands:
            cmd_type, param = self.normalized_commands[normalized]
            return self._execute_command(cmd_type, param)
        
        # 3. Перевірка часткового співпадіння (фраза містить команду)
        for phrase, (cmd_type, param) in self.normalized_commands.items():
            if phrase in normalized:
                return self._execute_command(cmd_type, param)
        
        # 4. Динамічні команди з параметрами
        result = self._try_dynamic_commands(normalized, original_input)
        if result:
            return result
        
        # 5. Не команда - передати AI
        return {
            "executed": False,
            "response": None,
            "type": "chat"
        }
    
    def _handle_slash_command(self, user_input: str) -> dict:
        """Обробка команд що починаються з /"""
        
        # /exit
        if user_input in ("/exit", "/quit"):
            return self._execute_command("exit", None)
        
        # /open <app>
        if user_input.startswith("/open "):
            target = user_input.replace("/open ", "", 1).strip()
            return self._open_app_or_path(target)
        
        # /steam <app_id або назва>
        if user_input.startswith("/steam "):
            target = user_input.replace("/steam ", "", 1).strip()
            return self._launch_steam_game(target)
        
        # /search <query>
        if user_input.startswith("/search "):
            query = user_input.replace("/search ", "", 1).strip()
            return self._search(query)
        
        # /site <website>
        if user_input.startswith("/site "):
            site = user_input.replace("/site ", "", 1).strip()
            return self._open_website(site)
        
        # /help
        if user_input == "/help":
            return {
                "executed": True,
                "response": self._get_help_text(),
                "type": "help"
            }
        
        return {
            "executed": False,
            "response": None,
            "type": "unknown_command"
        }
    
    def _try_dynamic_commands(self, normalized: str, original: str) -> dict:
        """Спробувати розпізнати динамічні команди з параметрами"""
        
        # Пошук
        for trigger in SEARCH_TRIGGERS:
            if trigger in normalized:
                # Витягти запит після тригера
                idx = normalized.find(trigger)
                query = original[idx + len(trigger):].strip()
                if query:
                    return self._search(query)
        
        # Запуск гри
        for trigger in PLAY_GAME_TRIGGERS:
            if trigger in normalized:
                idx = normalized.find(trigger)
                game_name = original[idx + len(trigger):].strip()
                if game_name:
                    return self._launch_steam_game(game_name)
        
        # Відкрити щось (програму або сайт)
        for trigger in OPEN_TRIGGERS:
            if normalized.startswith(trigger + " "):
                target = original[len(trigger):].strip()
                if target:
                    # Спробувати як програму
                    result = self._open_app_or_path(target)
                    if result["executed"]:
                        return result
                    # Спробувати як сайт
                    return self._open_website(target)
        
        return None
    
    def _execute_command(self, cmd_type: str, param: str) -> dict:
        """Виконати команду за типом"""
        
        if cmd_type == "exit":
            print(get_message("goodbye"))
            exit()
        
        if cmd_type == "open_app":
            return self._open_app(param)
        
        if cmd_type == "open_website":
            return self._open_website(param)
        
        if cmd_type == "search":
            return self._search(param)
        
        if cmd_type == "steam_game":
            return self._launch_steam_game(param)
        
        return {
            "executed": False,
            "response": get_message("command_not_recognized"),
            "type": "error"
        }
    
    def _open_app(self, app_name: str) -> dict:
        """Відкрити програму за назвою"""
        app_lower = app_name.lower()
        
        if app_lower in self.normalized_apps:
            path = self.normalized_apps[app_lower]
            try:
                subprocess.Popen(path, shell=True)
                return {
                    "executed": True,
                    "response": get_message("app_opened", app=app_name),
                    "type": "open_app"
                }
            except Exception as e:
                return {
                    "executed": False,
                    "response": f"Помилка: {e}",
                    "type": "error"
                }
        
        return {
            "executed": False,
            "response": get_message("app_not_found", app=app_name),
            "type": "error"
        }
    
    def _open_app_or_path(self, target: str) -> dict:
        """Відкрити програму за назвою або шляхом"""
        # Спочатку перевірити чи це відома програма
        result = self._open_app(target)
        if result["executed"]:
            return result
        
        # Спробувати як шлях до файлу
        try:
            subprocess.Popen(target, shell=True)
            return {
                "executed": True,
                "response": get_message("app_opened", app=target),
                "type": "open_app"
            }
        except Exception as e:
            return {
                "executed": False,
                "response": get_message("app_not_found", app=target),
                "type": "error"
            }
    
    def _open_website(self, site: str) -> dict:
        """Відкрити вебсайт"""
        site_lower = site.lower()
        
        # Перевірити чи це відомий сайт
        if site_lower in self.normalized_websites:
            url = self.normalized_websites[site_lower]
        elif site.startswith(("http://", "https://")):
            url = site
        else:
            # Спробувати як домен
            url = f"https://{site}"
        
        try:
            webbrowser.open(url)
            return {
                "executed": True,
                "response": get_message("website_opened", site=site),
                "type": "open_website"
            }
        except Exception as e:
            return {
                "executed": False,
                "response": f"Помилка: {e}",
                "type": "error"
            }
    
    def _search(self, query: str, engine: str = None) -> dict:
        """Пошук в інтернеті"""
        if not engine:
            engine = DEFAULT_SEARCH_ENGINE
        
        search_url = SEARCH_ENGINES.get(engine, SEARCH_ENGINES["google"])
        url = search_url + query.replace(" ", "+")
        
        try:
            webbrowser.open(url)
            return {
                "executed": True,
                "response": get_message("searching", query=query),
                "type": "search"
            }
        except Exception as e:
            return {
                "executed": False,
                "response": f"Помилка: {e}",
                "type": "error"
            }
    
    def _launch_steam_game(self, game: str) -> dict:
        """Запустити гру в Steam"""
        game_lower = game.lower()
        
        # Перевірити чи це відома гра
        if game_lower in self.normalized_games:
            app_id = self.normalized_games[game_lower]
        elif game.isdigit():
            # Це вже app_id
            app_id = game
        else:
            return {
                "executed": False,
                "response": get_message("game_not_found", game=game),
                "type": "error"
            }
        
        try:
            url = f"steam://rungameid/{app_id}"
            webbrowser.open(url)
            return {
                "executed": True,
                "response": get_message("game_launched", game=game),
                "type": "steam_game"
            }
        except Exception as e:
            return {
                "executed": False,
                "response": f"Помилка: {e}",
                "type": "error"
            }
    
    def _get_help_text(self) -> str:
        """Повернути текст допомоги"""
        return """
📋 ДОСТУПНІ КОМАНДИ:

Прямі команди (починаються з /):
  /open <програма>  - відкрити програму
  /steam <гра>      - запустити Steam гру
  /search <запит>   - пошук в Google
  /site <сайт>      - відкрити сайт
  /exit             - вийти
  /help             - ця допомога

Природна мова (приклади):
  "відкрий стім"       - відкриє Steam
  "запусти дискорд"    - відкриє Discord
  "знайди котиків"     - пошук в Google
  "пограй в dota"      - запустить Dota 2
  "відкрий ютуб"       - відкриє YouTube

💡 Налаштування в файлі: command_config.py
"""


# Глобальний екземпляр для зворотної сумісності
_handler = None

def get_handler() -> CommandHandler:
    """Отримати глобальний екземпляр обробника"""
    global _handler
    if _handler is None:
        _handler = CommandHandler()
    return _handler

def handle_command(user_input: str):
    """
    Функція для зворотної сумісності.
    Повертає рядок з результатом або None якщо не команда.
    """
    handler = get_handler()
    result = handler.process(user_input)
    
    if result["executed"]:
        return result["response"]
    return None



