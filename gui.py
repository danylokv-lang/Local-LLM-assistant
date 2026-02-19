"""
AI Assistant GUI - Steam Big Picture Style
Modern dark theme with glow effects and smooth animations
"""

import sys
import os
import math

# Windows DPI Awareness - BEFORE tkinter import
if sys.platform == 'win32':
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except:
            pass

import tkinter as tk
from tkinter import font as tkfont
import threading
import time
import json
from datetime import datetime
from typing import Callable, Dict, Optional

# ============ COLORS ============
COLORS = {
    "bg_dark": "#080808",
    "bg_medium": "#101010",
    "bg_light": "#181818",
    "bg_card": "#1a1a1a",
    "bg_input": "#141414",
    "bg_sidebar": "#0c0c0c",
    "white": "#ffffff",
    "gray_light": "#c0c0c0",
    "gray": "#808080",
    "gray_dark": "#404040",
    "accent": "#00a8ff",  # Blue accent
    "accent_glow": "#0066cc",
    "user_msg": "#1e1e1e",
    "ai_msg": "#282828",
    "hover": "#252525",
    "selected": "#303030",
    "success": "#22c55e",
    "warning": "#f59e0b",
}

CHATS_FILE = os.path.join(os.path.dirname(__file__), "chat_history.json")


# ============ CHAT STORAGE ============
class ChatStorage:
    def __init__(self):
        self.chats = {}
        self.load()
    
    def load(self):
        try:
            if os.path.exists(CHATS_FILE):
                with open(CHATS_FILE, 'r', encoding='utf-8') as f:
                    self.chats = json.load(f)
        except:
            self.chats = {}
    
    def save(self):
        try:
            with open(CHATS_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.chats, f, ensure_ascii=False, indent=2)
        except:
            pass
    
    def create_chat(self) -> str:
        chat_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.chats[chat_id] = {
            "id": chat_id, "title": "Новий чат",
            "created": datetime.now().isoformat(), "messages": []
        }
        self.save()
        return chat_id
    
    def add_message(self, chat_id: str, message: str, is_user: bool):
        if chat_id in self.chats:
            self.chats[chat_id]["messages"].append({
                "text": message, "is_user": is_user,
                "timestamp": datetime.now().isoformat()
            })
            if is_user and len([m for m in self.chats[chat_id]["messages"] if m["is_user"]]) == 1:
                self.chats[chat_id]["title"] = message[:25] + "..." if len(message) > 25 else message
            self.save()
    
    def get_chat(self, chat_id: str):
        return self.chats.get(chat_id)
    
    def get_all_chats(self):
        return sorted(self.chats.values(), key=lambda x: x["created"], reverse=True)
    
    def delete_chat(self, chat_id: str):
        if chat_id in self.chats:
            del self.chats[chat_id]
            self.save()


# ============ SPLASH SCREEN - Steam Big Picture Style ============
class SplashScreen(tk.Toplevel):
    def __init__(self, parent, on_complete):
        super().__init__(parent)
        self.on_complete = on_complete
        self.alpha = 0.0
        self.glow_phase = 0.0
        self.progress = 0.0
        self.particles = []
        self.is_loading = True  # Block closing while loading
        self.loaded_brain = None
        
        # Window setup
        self.title("")
        self.configure(bg=COLORS["bg_dark"])
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        
        # Block window closing
        self.protocol("WM_DELETE_WINDOW", self._on_close_attempt)
        
        # Size and center
        self.w, self.h = 600, 400
        x = (self.winfo_screenwidth() - self.w) // 2
        y = (self.winfo_screenheight() - self.h) // 2
        self.geometry(f"{self.w}x{self.h}+{x}+{y}")
        
        # Canvas for animations
        self.canvas = tk.Canvas(
            self, width=self.w, height=self.h,
            bg=COLORS["bg_dark"], highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)
        
        # Initialize particles
        for _ in range(30):
            self.particles.append({
                "x": self.w * 0.1 + (self.w * 0.8) * ((_ % 10) / 10),
                "y": self.h + 20 + (_ * 15),
                "speed": 0.5 + (_ % 5) * 0.3,
                "size": 2 + (_ % 3),
                "alpha": 0.3 + (_ % 5) * 0.1
            })
        
        # Start animations
        self.animate()
        self.load_sequence()
    
    def animate(self):
        """Main animation loop"""
        if not self.winfo_exists():
            return
        
        self.canvas.delete("all")
        
        # Background gradient effect
        for i in range(20):
            y = i * (self.h / 20)
            shade = int(8 + i * 0.5)
            color = f"#{shade:02x}{shade:02x}{shade:02x}"
            self.canvas.create_rectangle(0, y, self.w, y + self.h/20 + 1, fill=color, outline="")
        
        # Animated particles (rising dots)
        for p in self.particles:
            p["y"] -= p["speed"]
            if p["y"] < -20:
                p["y"] = self.h + 20
            
            # Fade based on position
            fade = 1.0 - abs(p["y"] - self.h/2) / (self.h/2)
            if fade > 0:
                alpha = int(min(255, fade * p["alpha"] * 255))
                color = f"#{alpha:02x}{alpha:02x}{alpha:02x}"
                self.canvas.create_oval(
                    p["x"] - p["size"], p["y"] - p["size"],
                    p["x"] + p["size"], p["y"] + p["size"],
                    fill=color, outline=""
                )
        
        # Center content
        cx, cy = self.w / 2, self.h / 2 - 30
        
        # GLOW EFFECT - Multiple layers
        self.glow_phase += 0.08
        glow_intensity = 0.6 + 0.4 * math.sin(self.glow_phase)
        
        # Outer glow rings
        for i in range(5, 0, -1):
            radius = 60 + i * 15
            alpha = int(30 * glow_intensity * (1 - i/5))
            if alpha > 0:
                color = f"#{alpha:02x}{alpha:02x}{alpha:02x}"
                self.canvas.create_oval(
                    cx - radius, cy - radius,
                    cx + radius, cy + radius,
                    outline=color, width=2
                )
        
        # Central glow
        glow_size = int(80 + 10 * math.sin(self.glow_phase * 2))
        for i in range(glow_size, 0, -5):
            alpha = int((glow_size - i) * 2 * glow_intensity)
            if alpha > 255: alpha = 255
            color = f"#{alpha:02x}{alpha:02x}{alpha:02x}"
            self.canvas.create_oval(
                cx - i, cy - i, cx + i, cy + i,
                fill=color, outline=""
            )
        
        # Logo hexagon
        size = 45
        points = []
        for i in range(6):
            angle = math.pi / 6 + i * math.pi / 3
            points.extend([
                cx + size * math.cos(angle),
                cy + size * math.sin(angle)
            ])
        self.canvas.create_polygon(points, fill=COLORS["bg_dark"], outline="#ffffff", width=3)
        
        # "AI" text in center
        self.canvas.create_text(cx, cy, text="AI", fill="#ffffff",
                               font=("Segoe UI", 24, "bold"))
        
        # Title with glow
        title_y = cy + 90
        # Glow behind text
        glow_alpha = int(100 * glow_intensity)
        for offset in range(3, 0, -1):
            self.canvas.create_text(
                cx, title_y,
                text="LOCAL AI ASSISTANT",
                fill=f"#{glow_alpha:02x}{glow_alpha:02x}{glow_alpha:02x}",
                font=("Segoe UI", 20 + offset, "bold")
            )
        self.canvas.create_text(cx, title_y, text="LOCAL AI ASSISTANT",
                               fill="#ffffff", font=("Segoe UI", 20, "bold"))
        
        # Version
        self.canvas.create_text(cx, title_y + 30, text="v2.0",
                               fill=COLORS["gray"], font=("Segoe UI", 11))
        
        # Progress bar
        bar_y = self.h - 60
        bar_w = 300
        bar_h = 4
        
        # Bar background
        self.canvas.create_rectangle(
            cx - bar_w/2, bar_y, cx + bar_w/2, bar_y + bar_h,
            fill=COLORS["gray_dark"], outline=""
        )
        
        # Progress fill with glow
        if self.progress > 0:
            fill_w = bar_w * self.progress
            # Glow
            self.canvas.create_rectangle(
                cx - bar_w/2 - 2, bar_y - 2,
                cx - bar_w/2 + fill_w + 2, bar_y + bar_h + 2,
                fill=f"#{int(50*glow_intensity):02x}{int(50*glow_intensity):02x}{int(50*glow_intensity):02x}",
                outline=""
            )
            # Main bar
            self.canvas.create_rectangle(
                cx - bar_w/2, bar_y,
                cx - bar_w/2 + fill_w, bar_y + bar_h,
                fill="#ffffff", outline=""
            )
        
        # Status text
        self.canvas.create_text(cx, bar_y + 25, text=getattr(self, 'status_text', 'Ініціалізація...'),
                               fill=COLORS["gray_light"], font=("Segoe UI", 10))
        
        self.after(16, self.animate)  # ~60 FPS
    
    def _on_close_attempt(self):
        """Block closing while loading"""
        if not self.is_loading:
            self.finish()
    
    def load_sequence(self):
        """Loading sequence - fast with Ollama"""
        def run():
            self.status_text = "Завантаження..."
            self.progress = 0.3
            time.sleep(0.2)
            
            self.status_text = "Підключення до AI..."
            self.progress = 0.5
            
            try:
                from brain import Brain
                self.loaded_brain = Brain()
                self.status_text = "Готово!"
                self.progress = 1.0
            except Exception as e:
                self.loaded_brain = None
                self.status_text = "Помилка AI"
            
            self.is_loading = False
            time.sleep(0.3)
            self.after(0, self.finish)
        
        threading.Thread(target=run, daemon=True).start()
    
    def finish(self):
        """Fade out and complete"""
        self.is_loading = False
        brain = getattr(self, 'loaded_brain', None)
        self.destroy()
        self.on_complete(brain)


# ============ MAIN WINDOW ============
class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("AI Assistant")
        self.configure(bg=COLORS["bg_dark"])
        self.geometry("1100x800")
        self.minsize(900, 600)
        
        # Force proper rendering
        self.tk.call('tk', 'scaling', 1.0)
        
        self.brain = None
        self.is_processing = False
        self.chat_storage = ChatStorage()
        self.current_chat_id = None
        self.sidebar_visible = True
        self.resize_after_id = None
        
        self._setup_fonts()
        self._setup_ui()
        self._center()
        self._load_initial_chat()
        
        # Bind resize with debounce
        self.bind("<Configure>", self._on_resize)
    
    def _setup_fonts(self):
        self.font_title = tkfont.Font(family="Segoe UI", size=26, weight="bold")
        self.font_normal = tkfont.Font(family="Segoe UI", size=20)
        self.font_small = tkfont.Font(family="Segoe UI", size=15)
        self.font_msg = tkfont.Font(family="Segoe UI", size=22)
    
    def _center(self):
        self.update_idletasks()
        w, h = 1100, 800
        x = (self.winfo_screenwidth() - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")
    
    def _setup_ui(self):
        # Main container
        self.main_frame = tk.Frame(self, bg=COLORS["bg_dark"])
        self.main_frame.pack(fill="both", expand=True)
        
        # Sidebar
        self._create_sidebar()
        
        # Chat area
        self._create_chat_area()
    
    def _create_sidebar(self):
        self.sidebar = tk.Frame(self.main_frame, bg=COLORS["bg_sidebar"], width=280)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        # Header
        header = tk.Frame(self.sidebar, bg=COLORS["bg_sidebar"])
        header.pack(fill="x", padx=15, pady=15)
        
        tk.Label(header, text="Чати", font=self.font_title,
                bg=COLORS["bg_sidebar"], fg=COLORS["white"]).pack(side="left")
        
        # New chat button
        new_btn = tk.Button(
            header, text="+", font=("Segoe UI", 20),
            bg=COLORS["gray_dark"], fg=COLORS["white"],
            activebackground=COLORS["gray"], activeforeground=COLORS["white"],
            bd=0, padx=12, pady=2, cursor="hand2",
            command=self._new_chat
        )
        new_btn.pack(side="right")
        
        # Separator
        tk.Frame(self.sidebar, bg=COLORS["gray_dark"], height=1).pack(fill="x", padx=15)
        
        # Chat list
        self.chat_list_frame = tk.Frame(self.sidebar, bg=COLORS["bg_sidebar"])
        self.chat_list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Canvas + Scrollbar for chat list
        self.chat_canvas = tk.Canvas(self.chat_list_frame, bg=COLORS["bg_sidebar"],
                                     highlightthickness=0)
        self.chat_scrollbar = tk.Scrollbar(self.chat_list_frame, orient="vertical",
                                           command=self.chat_canvas.yview)
        self.chat_inner = tk.Frame(self.chat_canvas, bg=COLORS["bg_sidebar"])
        
        self.chat_canvas.configure(yscrollcommand=self.chat_scrollbar.set)
        # Scrollbar hidden - use mouse wheel
        self.chat_canvas.pack(side="left", fill="both", expand=True)
        self.chat_canvas.create_window((0, 0), window=self.chat_inner, anchor="nw")
        
        self.chat_inner.bind("<Configure>", 
                            lambda e: self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all")))
    
    def _create_chat_area(self):
        self.chat_area = tk.Frame(self.main_frame, bg=COLORS["bg_dark"])
        self.chat_area.pack(side="left", fill="both", expand=True)
        
        # Header
        header = tk.Frame(self.chat_area, bg=COLORS["bg_dark"], height=60)
        header.pack(fill="x", padx=20, pady=(15, 10))
        header.pack_propagate(False)
        
        # Toggle button
        self.toggle_btn = tk.Button(
            header, text="☰", font=("Segoe UI", 20),
            bg=COLORS["gray_dark"], fg=COLORS["white"],
            activebackground=COLORS["gray"], activeforeground=COLORS["white"],
            bd=0, padx=10, pady=5, cursor="hand2",
            command=self._toggle_sidebar
        )
        self.toggle_btn.pack(side="left", padx=(0, 15))
        
        # Title
        title_frame = tk.Frame(header, bg=COLORS["bg_dark"])
        title_frame.pack(side="left", fill="y")
        
        tk.Label(title_frame, text="⬡", font=("Segoe UI", 28),
                bg=COLORS["bg_dark"], fg=COLORS["white"]).pack(side="left", padx=(0, 8))
        tk.Label(title_frame, text="AI ASSISTANT", font=self.font_title,
                bg=COLORS["bg_dark"], fg=COLORS["white"]).pack(side="left")
        
        # Status
        self.status_label = tk.Label(
            header, text="● Online", font=self.font_small,
            bg=COLORS["bg_dark"], fg=COLORS["success"]
        )
        self.status_label.pack(side="right", padx=10)
        
        # Chat container
        chat_container = tk.Frame(self.chat_area, bg=COLORS["bg_medium"])
        chat_container.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        
        # Messages area with canvas
        self.msg_canvas = tk.Canvas(chat_container, bg=COLORS["bg_medium"],
                                    highlightthickness=0)
        self.msg_scrollbar = tk.Scrollbar(chat_container, orient="vertical",
                                          command=self.msg_canvas.yview)
        self.msg_frame = tk.Frame(self.msg_canvas, bg=COLORS["bg_medium"])
        
        self.msg_canvas.configure(yscrollcommand=self.msg_scrollbar.set)
        # Scrollbar hidden - use mouse wheel
        self.msg_canvas.pack(side="left", fill="both", expand=True)
        self.msg_window = self.msg_canvas.create_window((0, 0), window=self.msg_frame, anchor="nw")
        
        # Update scroll region
        self.msg_frame.bind("<Configure>", self._on_msg_frame_configure)
        self.msg_canvas.bind("<Configure>", self._on_canvas_configure)
        
        # Mouse wheel scrolling
        self.msg_canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # Input area - auto-resize
        self.input_container = tk.Frame(self.chat_area, bg=COLORS["bg_dark"])
        self.input_container.pack(fill="x", padx=20, pady=(0, 15))
        
        input_frame = tk.Frame(self.input_container, bg=COLORS["bg_input"])
        input_frame.pack(fill="both", expand=True, pady=5)
        
        self.input_text = tk.Text(
            input_frame, font=self.font_normal,
            bg=COLORS["bg_input"], fg=COLORS["white"],
            insertbackground=COLORS["white"],
            height=1, wrap="word", bd=0, padx=15, pady=10
        )
        self.input_text.pack(side="left", fill="both", expand=True)
        self.input_text.bind("<Return>", self._on_send)
        self.input_text.bind("<Shift-Return>", lambda e: None)
        self.input_text.bind("<KeyRelease>", self._auto_resize_input)
        
        # Placeholder
        self.input_text.insert("1.0", "Напиши повідомлення...")
        self.input_text.config(fg=COLORS["gray"])
        self.input_text.bind("<FocusIn>", self._on_input_focus_in)
        self.input_text.bind("<FocusOut>", self._on_input_focus_out)
        self.has_placeholder = True
        
        # Send button
        self.send_btn = tk.Button(
            input_frame, text="→", font=("Segoe UI", 22),
            bg=COLORS["white"], fg=COLORS["bg_dark"],
            activebackground=COLORS["gray_light"], activeforeground=COLORS["bg_dark"],
            bd=0, padx=15, pady=8, cursor="hand2",
            command=self._on_send
        )
        self.send_btn.pack(side="right", padx=10, pady=5)
        
        # Hints
        tk.Label(
            self.chat_area, text="Enter → надіслати  •  Shift+Enter → новий рядок  •  /help → команди",
            font=self.font_small, bg=COLORS["bg_dark"], fg=COLORS["gray"]
        ).pack(pady=(0, 5))
    
    def _on_msg_frame_configure(self, event):
        self.msg_canvas.configure(scrollregion=self.msg_canvas.bbox("all"))
    
    def _on_canvas_configure(self, event):
        self.msg_canvas.itemconfig(self.msg_window, width=event.width)
    
    def _on_mousewheel(self, event):
        self.msg_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    def _on_resize(self, event):
        # Debounce resize events
        if self.resize_after_id:
            self.after_cancel(self.resize_after_id)
        self.resize_after_id = self.after(100, self._do_resize)
    
    def _do_resize(self):
        self.resize_after_id = None
    
    def _on_input_focus_in(self, event):
        if self.has_placeholder:
            self.input_text.delete("1.0", "end")
            self.input_text.config(fg=COLORS["white"])
            self.has_placeholder = False
    
    def _on_input_focus_out(self, event):
        if not self.input_text.get("1.0", "end-1c").strip():
            self.input_text.insert("1.0", "Напиши повідомлення...")
            self.input_text.config(fg=COLORS["gray"])
            self.has_placeholder = True
    
    def _auto_resize_input(self, event=None):
        """Автоматично змінювати висоту поля вводу"""
        # Підрахувати кількість рядків
        content = self.input_text.get("1.0", "end-1c")
        lines = content.count('\n') + 1
        
        # Обмежити від 1 до 8 рядків
        new_height = max(1, min(8, lines))
        
        current_height = int(self.input_text.cget("height"))
        if new_height != current_height:
            self.input_text.config(height=new_height)
    
    def _toggle_sidebar(self):
        if self.sidebar_visible:
            self.sidebar.pack_forget()
            self.sidebar_visible = False
        else:
            self.sidebar.pack(side="left", fill="y", before=self.chat_area)
            self.sidebar_visible = True
    
    def _load_initial_chat(self):
        chats = self.chat_storage.get_all_chats()
        if chats:
            self.current_chat_id = chats[0]["id"]
            self._load_chat(self.current_chat_id)
        else:
            self._new_chat()
        self._refresh_chat_list()
    
    def _refresh_chat_list(self):
        for widget in self.chat_inner.winfo_children():
            widget.destroy()
        
        for chat in self.chat_storage.get_all_chats():
            self._create_chat_item(chat)
    
    def _create_chat_item(self, chat):
        is_selected = chat["id"] == self.current_chat_id
        bg = COLORS["selected"] if is_selected else COLORS["bg_sidebar"]
        
        frame = tk.Frame(self.chat_inner, bg=bg, cursor="hand2")
        frame.pack(fill="x", pady=2)
        
        # Content
        content = tk.Frame(frame, bg=bg)
        content.pack(fill="x", padx=10, pady=8)
        
        tk.Label(content, text="💬", font=self.font_normal, bg=bg, fg=COLORS["white"]).pack(side="left")
        
        text_frame = tk.Frame(content, bg=bg)
        text_frame.pack(side="left", fill="x", expand=True, padx=8)
        
        tk.Label(text_frame, text=chat.get("title", "Новий чат")[:20],
                font=self.font_normal, bg=bg, fg=COLORS["white"], anchor="w").pack(anchor="w")
        
        try:
            date = datetime.fromisoformat(chat["created"]).strftime("%d.%m.%Y")
        except:
            date = ""
        tk.Label(text_frame, text=date, font=self.font_small, bg=bg, fg=COLORS["gray"]).pack(anchor="w")
        
        # Delete button
        del_btn = tk.Button(content, text="✕", font=self.font_small,
                           bg=bg, fg=COLORS["gray"],
                           activebackground=bg, activeforeground=COLORS["white"],
                           bd=0, cursor="hand2",
                           command=lambda: self._delete_chat(chat["id"]))
        del_btn.pack(side="right")
        
        # Click binding
        for widget in [frame, content, text_frame]:
            widget.bind("<Button-1>", lambda e, cid=chat["id"]: self._select_chat(cid))
        
        # Hover effect
        def on_enter(e):
            if chat["id"] != self.current_chat_id:
                frame.config(bg=COLORS["hover"])
                for w in frame.winfo_children():
                    self._set_bg_recursive(w, COLORS["hover"])
        
        def on_leave(e):
            if chat["id"] != self.current_chat_id:
                frame.config(bg=COLORS["bg_sidebar"])
                for w in frame.winfo_children():
                    self._set_bg_recursive(w, COLORS["bg_sidebar"])
        
        frame.bind("<Enter>", on_enter)
        frame.bind("<Leave>", on_leave)
    
    def _set_bg_recursive(self, widget, color):
        try:
            widget.config(bg=color)
            for child in widget.winfo_children():
                self._set_bg_recursive(child, color)
        except:
            pass
    
    def _select_chat(self, chat_id):
        if chat_id != self.current_chat_id:
            self.current_chat_id = chat_id
            self._load_chat(chat_id)
            self._refresh_chat_list()
    
    def _new_chat(self):
        chat_id = self.chat_storage.create_chat()
        self.current_chat_id = chat_id
        self._clear_messages()
        self._add_welcome()
        self._refresh_chat_list()
    
    def _delete_chat(self, chat_id):
        self.chat_storage.delete_chat(chat_id)
        if chat_id == self.current_chat_id:
            chats = self.chat_storage.get_all_chats()
            if chats:
                self.current_chat_id = chats[0]["id"]
                self._load_chat(self.current_chat_id)
            else:
                self._new_chat()
        self._refresh_chat_list()
    
    def _load_chat(self, chat_id):
        self._clear_messages()
        chat = self.chat_storage.get_chat(chat_id)
        if chat:
            if not chat["messages"]:
                self._add_welcome()
            else:
                for msg in chat["messages"]:
                    self._add_message_widget(msg["text"], msg["is_user"])
    
    def _clear_messages(self):
        for widget in self.msg_frame.winfo_children():
            widget.destroy()
    
    def _add_welcome(self):
        text = """Привіт! Я твій AI асистент.


Напиши /help для списку команд."""
        self._add_message_widget(text, is_user=False)
    
    def _add_message_widget(self, text, is_user):
        bg = COLORS["user_msg"] if is_user else COLORS["ai_msg"]
        fg = COLORS["white"] if is_user else COLORS["gray_light"]
        prefix = "ТИ" if is_user else "AI"
        
        frame = tk.Frame(self.msg_frame, bg=bg)
        frame.pack(fill="x", padx=15, pady=8)
        
        # Header
        header = tk.Frame(frame, bg=bg)
        header.pack(fill="x", padx=15, pady=(12, 8))
        
        tk.Label(header, text=prefix, font=("Segoe UI", 16, "bold"),
                bg=bg, fg=COLORS["gray_light"] if is_user else COLORS["white"]).pack(side="left")
        tk.Label(header, text=datetime.now().strftime("%H:%M"),
                font=self.font_small, bg=bg, fg=COLORS["gray"]).pack(side="right")
        
        # Message text
        msg_label = tk.Label(frame, text=text, font=self.font_msg,
                            bg=bg, fg=fg, wraplength=700, justify="left", anchor="w")
        msg_label.pack(fill="x", padx=15, pady=(0, 15))
        
        # Scroll to bottom
        self.msg_canvas.update_idletasks()
        self.msg_canvas.yview_moveto(1.0)
    
    def _on_send(self, event=None):
        if self.is_processing or self.has_placeholder:
            return "break"
        
        text = self.input_text.get("1.0", "end-1c").strip()
        if not text:
            return "break"
        
        self.input_text.delete("1.0", "end")
        self.input_text.config(height=1)  # Reset height after sending
        self._add_message_widget(text, is_user=True)
        
        if self.current_chat_id:
            self.chat_storage.add_message(self.current_chat_id, text, True)
            self._refresh_chat_list()
        
        self.is_processing = True
        self.send_btn.config(state="disabled")
        self.status_label.config(text="● Думаю...", fg=COLORS["warning"])
        
        threading.Thread(target=self._process_message, args=(text,), daemon=True).start()
        return "break"
    
    def _process_message(self, text):
        try:
            if self.brain:
                response = self.brain.process(text)
            else:
                response = "AI не ініціалізований. Перезапустіть програму."
        except Exception as e:
            response = f"Помилка: {e}"
        
        self.after(0, lambda: self._show_response(response))
    
    def _show_response(self, response):
        self._add_message_widget(response, is_user=False)
        
        if self.current_chat_id:
            self.chat_storage.add_message(self.current_chat_id, response, False)
        
        self.is_processing = False
        self.send_btn.config(state="normal")
        self.status_label.config(text="● Online", fg=COLORS["success"])
    
    def set_brain(self, brain):
        self.brain = brain


# ============ APP ============
class App:
    def __init__(self):
        # Create main window
        self.main_window = MainWindow()
        self.main_window.withdraw()
        
        # Load brain directly (fast with Ollama)
        try:
            from brain import Brain
            self.brain = Brain()
        except Exception as e:
            self.brain = None
        
        self.main_window.set_brain(self.brain)
        self.main_window.deiconify()
        self.main_window.lift()
        self.main_window.focus_force()
    
    def run(self):
        self.main_window.mainloop()


def main():
    app = App()
    app.run()


if __name__ == "__main__":
    main()
