"""
AI Model - підтримка Ollama та llama-cpp-python

Використовує Ollama за замовчуванням (простіше налаштувати).
Для локальної моделі через llama-cpp - розкоментуй відповідний код.
"""

import os

# Спробувати імпортувати ollama, якщо не вдалося - llama-cpp
try:
    import ollama
    USE_OLLAMA = True
except ImportError:
    USE_OLLAMA = False
    try:
        from llama_cpp import Llama
    except ImportError:
        raise ImportError("Встанови ollama (pip install ollama) або llama-cpp-python")


class AIModel:
    """
    Інтерфейс для AI моделі.
    
    Підтримує:
    - Ollama (рекомендовано) - потребує запущений ollama serve
    - llama-cpp-python - потребує .gguf файл моделі
    """
    
    # --- НАЛАШТУВАННЯ ---
    OLLAMA_MODEL = "llama3-local"  # твоя модель Meta-Llama-3-8B-Instruct
    
    SYSTEM_PROMPT = """You are a helpful, friendly AI assistant. 
You can help with various tasks and answer questions.
When the user asks to open apps, search, or control their computer, 
acknowledge their request naturally.
Be conversational and friendly. You can respond in Ukrainian or English 
based on the user's language."""

    def __init__(self):
        if USE_OLLAMA:
            self._init_ollama()
        else:
            self._init_llama_cpp()
    
    def _init_ollama(self):
        """Ініціалізація Ollama"""
        print(f"Підключаюсь до Ollama ({self.OLLAMA_MODEL})...")
        self.backend = "ollama"
        
        # Перевірити чи модель доступна
        try:
            # Тестовий запит
            ollama.chat(model=self.OLLAMA_MODEL, messages=[
                {"role": "user", "content": "test"}
            ])
            print("Ollama готовий!")
        except Exception as e:
            print(f"⚠️ Помилка Ollama: {e}")
            print("Переконайся що:")
            print("1. Ollama запущений (ollama serve)")
            print(f"2. Модель завантажена (ollama pull {self.OLLAMA_MODEL})")
            raise
    
    def _init_llama_cpp(self):
        """Ініціалізація llama-cpp-python"""
        print("Завантажую локальну модель...")
        self.backend = "llama_cpp"
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(base_dir, "models", "mistral-7b-openorca.Q4_K_M.gguf")
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Модель не знайдена: {model_path}")
        
        self.model = Llama(
            model_path=model_path,
            n_ctx=2048,
            n_gpu_layers=0,
            verbose=False
        )
        print("Модель завантажена!")
    
    def generate(self, user_input: str, history: list = None) -> str:
        """
        Згенерувати відповідь на запит користувача.
        
        Args:
            user_input: Текст від користувача
            history: Історія розмови (опціонально)
        
        Returns:
            Відповідь AI
        """
        if self.backend == "ollama":
            return self._generate_ollama(user_input, history)
        else:
            return self._generate_llama_cpp(user_input, history)
    
    def _generate_ollama(self, user_input: str, history: list = None) -> str:
        """Генерація через Ollama"""
        messages = [{"role": "system", "content": self.SYSTEM_PROMPT}]
        
        # Додати історію якщо є
        if history:
            for msg in history[-10:]:  # Останні 10 повідомлень
                messages.append(msg)
        
        messages.append({"role": "user", "content": user_input})
        
        try:
            response = ollama.chat(
                model=self.OLLAMA_MODEL,
                messages=messages
            )
            return response["message"]["content"].strip()
        except Exception as e:
            return f"Помилка генерації: {e}"
    
    def _generate_llama_cpp(self, user_input: str, history: list = None) -> str:
        """Генерація через llama-cpp-python"""
        full_prompt = (
            f"<|im_start|>system\n{self.SYSTEM_PROMPT}<|im_end|>\n"
            f"<|im_start|>user\n{user_input}<|im_end|>\n"
            f"<|im_start|>assistant\n"
        )
        
        output = self.model(
            full_prompt,
            max_tokens=200,
            stop=["<|im_end|>"],
        )
        return output["choices"][0]["text"].strip()


