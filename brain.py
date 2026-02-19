from model import AIModel
from commands import CommandHandler

class Brain:
    """
    Мозок асистента - обробляє введення користувача.
    
    Логіка:
    1. Спочатку перевіряє чи це команда (відкрити програму, пошук, тощо)
    2. Якщо не команда - передає AI для генерації відповіді
    """
    
    def __init__(self):
        # Use ASCII-safe messages for Windows console compatibility
        self.command_handler = CommandHandler()
        self.model = AIModel()
        self.history = []

    def process(self, user_input: str) -> str:
        """
        Обробити введення користувача.
        
        Args:
            user_input: Текст від користувача
            
        Returns:
            Відповідь (від команди або AI)
        """
        # Спочатку перевірити чи це команда
        result = self.command_handler.process(user_input)
        
        if result["executed"]:
            # Команда виконана - повернути результат
            # Можна також попросити AI прокоментувати
            if result["type"] not in ["exit", "help"]:
                # Додати в історію
                self.history.append({
                    "role": "user", 
                    "content": user_input
                })
                self.history.append({
                    "role": "assistant", 
                    "content": result["response"]
                })
            return result["response"]
        
        # Не команда - передати AI
        response = self.model.generate(user_input, history=self.history)
        
        # Зберегти в історію
        self.history.append({"role": "user", "content": user_input})
        self.history.append({"role": "assistant", "content": response})
        
        # Обмежити розмір історії
        if len(self.history) > 20:
            self.history = self.history[-20:]
        
        return response
    
    def clear_history(self):
        """Очистити історію розмови"""
        self.history = []
        return "Історію очищено!"
