# Local LLM Assistant v3.0

A local AI assistant with modern GUI, Ollama/llama-cpp support, and smart NLP commands.

---

## What's New in v3.0

### Added

- Modern GUI with dark theme and large fonts
- Chat history sidebar with ability to switch between conversations
- Auto-save chats to `chat_history.json`
- Auto-expanding input field (grows with each line)
- DPI awareness for crisp text on any monitor
- Dual backend support: Ollama (fast) or llama-cpp-python (standalone)
- Natural language commands: "open steam", "search cats", "play game"

### Removed

- Splash screen (slowed startup, not needed with Ollama)
- CustomTkinter (replaced with pure tkinter for speed)
- Unicode print statements (fixed Windows encoding issues)

### Changed

- CLI interface -> GUI with sidebar
- Commands trigger only at start of message (prevents false matches)
- Increased font sizes to 20-26pt
- Instant startup with Ollama instead of 2-4 min model loading

---

## Quick Start

### 1. Install dependencies

```bash
python -m venv venv
venv\Scripts\activate  # Windows
pip install ollama
```

### 2. Install Ollama + model

```bash
# Download Ollama from https://ollama.ai
ollama pull llama3
# or create your own model
ollama create llama3-local -f Modelfile
```

### 3. Run

```bash
python gui.py
```

---

## Project Structure

```
gui.py              - Main GUI (tkinter)
brain.py            - Message processing logic
model.py            - AI model (Ollama/llama-cpp)
commands.py         - Command handler
command_config.py   - Command settings
config.py           - General settings
memory.py           - Memory management
chat_history.json   - Saved chats
Modelfile           - Ollama config
models/             - Folder for .gguf models
```

---

## Backend Configuration

Edit `model.py`:

```python
# Ollama (recommended) - fast, model stays in memory
USE_OLLAMA = True
OLLAMA_MODEL = "llama3-local"

# or llama-cpp-python - standalone, but slower startup
USE_OLLAMA = False
MODEL_FILE = "Meta-Llama-3-8B-Instruct.Q4_K_M.gguf"
```

---

## NLP Commands

| Command | Example |
|---------|---------|
| Search | "search recipe" |
| Open app | "open steam" |
| Launch game | "play cs" |
| Open website | "open youtube" |
| Exit | "bye", "quit" |

Commands are configured in `command_config.py`.

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| Enter | Send message |
| Shift+Enter | New line |
| /help | Show commands |

---

## Backend Comparison

| Parameter | Ollama | llama-cpp-python |
|-----------|--------|------------------|
| Startup speed | ~2 sec | ~2-4 min |
| RAM | Model in memory | Loads each time |
| Setup | Easier | More control |
| Dependencies | ollama serve | Python only |

Recommendation: Use Ollama for daily use.

---

## Troubleshooting

### "AI not initialized"
```bash
# Check if Ollama is running
ollama list
# If not, start it
ollama serve
```

### Slow startup
- Switch to Ollama (`USE_OLLAMA = True`)

### Small text
- Font sizes are configured in `gui.py` -> `_setup_fonts()`

---

## Version History

| Version | Changes |
|---------|---------|
| v3.0 | GUI, chat history, NLP commands, Ollama |
| v2.0 | Brain architecture, commands |
| v1.0 | CLI chatbot with llama-cpp |

---

## License

MIT License


