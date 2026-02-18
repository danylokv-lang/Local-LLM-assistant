#  Local Llama 3 Chatbot

> **A lightweight, local-first AI assistant** powered by `llama.cpp` and **Meta Llama 3**, wrapped in a simple Python architecture with clear separation of concerns.

This project is ideal as a foundation for building your own **CLI assistant**, **personal agent**, or for experimenting with **local LLMs**.

---

##  Features

- **Local inference** with `llama.cpp` (no external API required)
- **Clean modular design:**
  - `AIModel` – low-level model wrapper
  - `Brain` – conversation logic and history handling
  - `Memory` – configurable conversation context window
  - `commands` – extensible slash-commands (`/open`, `/exit`, etc.)
  - `config` – centralized model and behavior settings
- **Simple CLI interface** (`main.py`) with a chat-like experience
- **Conversation history** to keep context across turns
- **Easy to adapt** for other GGUF models or front-ends (GUI, web, Discord, etc.)

---

##  Project Structure

```
.
├── main.py          # Entry point, CLI chat loop
├── brain.py         # High-level conversation brain, uses AIModel + history
├── model.py         # Llama.cpp model wrapper (Meta Llama 3 GGUF)
├── memory.py        # Conversation memory management
├── commands.py      # Slash command handling (/open, /exit, ...)
├── config.py        # Global configuration (model name, system prompt, history)
└── models/
    └── meta-llama-3-8b-instruct-q4_0.gguf  # Local model file (not included)
```

---

##  Requirements

- **Python 3.10+** (recommended)
- **GPU or CPU** capable of running the chosen GGUF model
- **Python dependencies:**
  - `llama-cpp-python`
  - *(Optionally)* any extra deps for commands or integrations

### Installation

```model
Meta-Llama-3-8B-Instruct-Q4_0-GGUF
https://huggingface.co/aptha/Meta-Llama-3-8B-Instruct-Q4_0-GGUF/tree/main

```


```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install llama-cpp-python
```

> **Note:** Make sure the GGUF model file is placed under `models/` and the path in `model.py` matches:

```python
self.model = Llama(
    model_path="models/meta-llama-3-8b-instruct-q4_0.gguf",
    n_ctx=2048,
    n_gpu_layers=40,
    verbose=False,
)
```

---

##  Usage

Run the chatbot from the project root:

```bash
python main.py
```

You will see:

```
Loading model on GPU with llama.cpp...
Model loaded!
AI Assistant started. Type /exit to quit.
You:
```

### Examples

**Regular message** – sent to the AI:
```
You: Hi, how are you?
AI: ...
```

**Exit the assistant:**
```
You: /exit
```

**Open a local program:**
```
You: /open notepad.exe
```

> Commands are handled in `commands.py`, and you can extend this with your own tooling.

---

##  Core Components

### **AIModel** (`model.py`)

Encapsulates `llama.cpp` and defines how prompts are sent to the model:

- Initializes the Llama model with a given GGUF file, context size, and GPU layers
- Builds a prompt (optionally including history) and calls the model
- Extracts and returns the generated text

**You can:**
- Switch to another GGUF model
- Tune generation parameters (`max_tokens`, `temperature`, `stop` tokens)
- Adjust the chat template for different model families

---

### **Brain** (`brain.py`)

High-level logic for a single conversation:

- Holds a history of turns
- Calls `AIModel.generate(...)` with the current user message and history
- Stores each `{user, assistant}` pair for future context

**You can:**
- Implement system messages, roles, tools, or routing between multiple models
- Add filters, safety, or additional reasoning logic

---

### **Memory** (`memory.py`)

Simple sliding-window memory:

- Stores recent messages as `{"role": ..., "content": ...}`
- Keeps only the last `MAX_HISTORY` items (configured in `config.py`)
- Provides a `get_context()` method to build a context string

**You can replace or upgrade this with:**
- Persistent storage (database, files)
- Retrieval-augmented generation (RAG) pipelines
- Per-user or per-session memory

---

### **Commands** (`commands.py`)

Basic slash command support:

| Command | Description |
|---------|-------------|
| `/open <program>` | Launches a local program via subprocess |
| `/exit` | Terminates the assistant |

**Extend with:**
- Custom tools (open URLs, manage files, control media)
- Integration with external APIs or local services

---

### **Config** (`config.py`)

Central configuration:

| Setting | Description |
|---------|-------------|
| `MODEL_NAME` | Reference model name |
| `MAX_HISTORY` | How many messages to retain in memory |
| `SYSTEM_PROMPT` | Default system instruction for the assistant |

**Use this to manage:**
- Different profiles or modes ("code assistant", "teacher", "storyteller")
- Environment-specific settings

---

##  Customization Ideas

| Idea | Description |
|------|-------------|
| **Swap the model** | Use a different Llama 3 variant or another GGUF instruct model |
| **Change the chat style** | Adjust the prompt and stop tokens to match your preferred template |
| **Add front-ends** | Wrap Brain in a web server (FastAPI/Flask), Discord bot, or desktop UI |
| **Extend commands** | Add `/search`, `/note`, `/todo`, or integrate with your own tools |

---

##  Disclaimer

> **This project runs a local LLM** – quality and performance depend on your hardware and the chosen model.
>
> **Be careful** with `/open` and any other system commands – they execute programs on your machine.


