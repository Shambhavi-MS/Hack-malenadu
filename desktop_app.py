# ═══════════════════════════════════════════════════════════════
# desktop_app.py — ThreatForge Main Desktop Window
# This is the GUI window with buttons, metrics, and the live log
# ═══════════════════════════════════════════════════════════════

import customtkinter as ctk
from agent import ThreatAgent

# ── Set dark theme ──
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class ThreatForgeApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        # ── Window settings ──
        self.title("⚡ ThreatForge — Desktop Agent")
        self.geometry("900x620")
        self.resizable(True, True)

        # ── Create the agent ──
        self.agent = ThreatAgent(interval=3, on_event=self.handle_event)

        # ── Build the interface ──
        self.build_header()
        self.build_stats_row()
        self.build_log_area()
        self.build_controls()

    # ═══ HEADER ═══
    def build_header(self):
        header = ctk.CTkFrame(self, fg_color="#161b22", corner_radius=0)
        header.pack(fill="x")

        ctk.CTkLabel(header, text="⚡  THREAT FORGE  AGENT",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#ff6b35").pack(side="left", padx=20, pady=14)

        self.status_label = ctk.CTkLabel(header, text="● IDLE",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#8b949e")
        self.status_label.pack(side="right", padx=20)

    # ═══ STATS ROW (4 metric boxes) ═══
    def build_stats_row(self):
        row = ctk.CTkFrame(self, fg_color="transparent")
        row.pack(fill="x", padx=16, pady=12)

        stats = [
            ("🔴 Attacks",  "0", "#ff6b35", "attacks"),
            ("✅ Safe",     "0", "#3fb950", "safe"),
            ("🔍 Total",   "0", "#58a6ff", "total"),
            ("🎯 Rate",    "0%", "#bc8cff", "rate"),
        ]
        self.stat_labels = {}

        for label, val, color, key in stats:
            card = ctk.CTkFrame(row, fg_color="#161b22", corner_radius=10)
            card.pack(side="left", expand=True, fill="x", padx=6)

            val_lbl = ctk.CTkLabel(card, text=val,
                font=ctk.CTkFont(size=28, weight="bold"), text_color=color)
            val_lbl.pack(pady=(12,2))

            ctk.CTkLabel(card, text=label,
                font=ctk.CTkFont(size=11),
                text_color="#8b949e").pack(pady=(0,12))

            self.stat_labels[key] = val_lbl

    # ═══ SCROLLING LOG ═══
    def build_log_area(self):
        frame = ctk.CTkFrame(self, fg_color="#161b22", corner_radius=10)
        frame.pack(fill="both", expand=True, padx=16, pady=4)

        ctk.CTkLabel(frame, text="📋  Live Event Log",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#8b949e").pack(anchor="w", padx=14, pady=(12,4))

        self.log_box = ctk.CTkTextbox(frame,
            font=ctk.CTkFont(family="Consolas", size=12),
            fg_color="#0d1117", text_color="#e6edf3", wrap="word")
        self.log_box.pack(fill="both", expand=True, padx=10, pady=(0,10))

        self.log("[ ThreatForge Agent ready — press START to begin ]")

    # ═══ CONTROL BUTTONS ═══
    def build_controls(self):
        bar = ctk.CTkFrame(self, fg_color="#161b22", corner_radius=0)
        bar.pack(fill="x", side="bottom")

        self.start_btn = ctk.CTkButton(bar, text="▶  START",
            fg_color="#238636", hover_color="#2ea043",
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self.start_agent)
        self.start_btn.pack(side="left", padx=12, pady=10)

        self.stop_btn = ctk.CTkButton(bar, text="■  STOP",
            fg_color="#6e1a1a", hover_color="#9a2828",
            font=ctk.CTkFont(size=13, weight="bold"),
            state="disabled", command=self.stop_agent)
        self.stop_btn.pack(side="left", padx=4)

        ctk.CTkButton(bar, text="🗑  Clear Log",
            fg_color="#21262d", font=ctk.CTkFont(size=13),
            command=self.clear_log).pack(side="left", padx=4)

    # ═══ BUTTON ACTIONS ═══
    def start_agent(self):
        self.agent.start()
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.status_label.configure(text="● MONITORING", text_color="#3fb950")
        self.log("Agent started — monitoring every 3 seconds...")
        self.schedule_stats_update()

    def stop_agent(self):
        self.agent.stop()
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.status_label.configure(text="● STOPPED", text_color="#e85d4a")
        self.log("Agent stopped.")

    def clear_log(self):
        self.log_box.delete("1.0", "end")

    # ═══ EVENT HANDLERS ═══
    def handle_event(self, result):
        # Called from background thread — use .after() to update GUI safely
        self.after(0, self._update_ui, result)

    def _update_ui(self, result):
        msg = f"[ {result['timestamp']} ]  {result['label']}  |  {result['confidence']}"
        self.log(msg)

    def log(self, msg):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", msg + "\n")
        self.log_box.configure(state="disabled")
        self.log_box.see("end")

    def schedule_stats_update(self):
        # Updates the 4 metric boxes every 2 seconds
        if self.agent.running:
            stats = self.agent.get_stats()
            self.stat_labels['attacks'].configure(text=str(stats['attacks']))
            self.stat_labels['safe'].configure(text=str(stats['safe']))
            self.stat_labels['total'].configure(text=str(stats['total']))
            self.stat_labels['rate'].configure(text=stats['rate'])
            self.after(2000, self.schedule_stats_update)
