"""
AI Model - підтримка Ollama та llama-cpp-python

Вибери бекенд нижче: USE_OLLAMA = True/False
"""

import os

# ========== ВИБІР БЕКЕНДУ ==========
# True = Ollama (потребує ollama serve)
# False = llama-cpp-python (працює напряму з .gguf файлом)
USE_OLLAMA = True  # Ollama - швидко!

# Шлях до твоєї моделі
MODEL_FILE = "Meta-Llama-3-8B-Instruct.Q4_K_M.gguf"


if USE_OLLAMA:
    try:
        import ollama
    except ImportError:
        raise ImportError("Встанови ollama: pip install ollama")
else:
    try:
        from llama_cpp import Llama
    except ImportError:
        raise ImportError("Встанови llama-cpp-python: pip install llama-cpp-python")


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
        """Initialize Ollama"""
        self.backend = "ollama"
        
        # Check if model is available
        try:
            ollama.chat(model=self.OLLAMA_MODEL, messages=[
                {"role": "user", "content": "test"}
            ])
        except Exception as e:
            raise RuntimeError(f"Ollama error: {e}. Make sure ollama serve is running.")
    
    def _init_llama_cpp(self):
        """Initialize llama-cpp-python with Meta-Llama-3"""
        self.backend = "llama_cpp"
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(base_dir, "models", MODEL_FILE)
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found: {model_path}")
        
        self.model = Llama(
            model_path=model_path,
            n_ctx=4096,  # Llama 3 supports 8K context
            n_gpu_layers=0,  # 0 = CPU only
            verbose=False
        )
    
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
        """Генерація через llama-cpp-python (Llama 3 формат)"""
        # Llama 3 Instruct формат
        full_prompt = (
            f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n"
            f"{self.SYSTEM_PROMPT}<|eot_id|>"
            f"<|start_header_id|>user<|end_header_id|>\n\n"
            f"{user_input}<|eot_id|>"
            f"<|start_header_id|>assistant<|end_header_id|>\n\n"
        )
        
        output = self.model(
            full_prompt,
            max_tokens=512,
            stop=["<|eot_id|>", "<|end_of_text|>"],
            temperature=0.7,
        )
        return output["choices"][0]["text"].strip()


