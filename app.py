# type_speed_pro_responsive.py
import tkinter as tk
from tkinter import ttk
import random
import time

WORDS = [
    "way","look","take","three","four","car","follow","a","but","which","got",
    "product","wind","who","king","far","have","always","list","from",
    "quick","brown","fox","jumps","over","lazy","dog"
]

# Theme
BG = "#FFF5E6"
PANEL_BG = "#FFFFFF"
PRIMARY = "#FF7F50"
MUTED = "#4A4A4A"
FONT_REGULAR = ("Courier New", 12)
FONT_BOLD = ("Courier New", 14, "bold")
FONT_TITLE = ("Courier New", 28, "bold")


class TypeSpeedProApp:
    def __init__(self, root):
        self.root = root
        root.title("TypeSpeed Pro")
        root.geometry("1000x720")
        root.minsize(800, 520)
        root.configure(bg=BG)

        style = ttk.Style(root)
        try:
            style.theme_use("clam")
        except Exception:
            pass
        style.configure("Card.TFrame", background=PANEL_BG)
        style.configure("Title.TLabel", background=BG, foreground=PRIMARY, font=FONT_TITLE)
        style.configure("Primary.TButton", background=PRIMARY, foreground="#fff")
        style.map("Primary.TButton", background=[("!disabled", PRIMARY)], foreground=[("!disabled", "#fff")])

        # state
        self.duration = 60
        self.time_left = 0
        self.timer_job = None
        self.started = False
        self.current_words = []
        self.current_index = 0
        self.total_typed_chars = 0
        self.correct_chars = 0
        self.errors = []
        self.results_visible = False

        self._build_ui()

    def _build_ui(self):
        # Header
        header = ttk.Frame(self.root, padding=(10, 8), style="Card.TFrame")
        header.pack(fill="x", pady=(8, 6))
        ttk.Label(header, text="TypeSpeed Pro", style="Title.TLabel").pack(anchor="center")

        # Tabs row
        tab_frame = ttk.Frame(self.root, padding=(6, 6), style="Card.TFrame")
        tab_frame.pack(fill="x", padx=12)
        ttk.Button(tab_frame, text="Typing Test", command=self._scroll_top, style="Primary.TButton").pack(side="left", padx=6)
        ttk.Button(tab_frame, text="Errors", command=self.toggle_errors_panel, style="Primary.TButton").pack(side="left", padx=6)

        # Scrollable canvas for content
        self.canvas = tk.Canvas(self.root, bg=BG, highlightthickness=0)
        self.vscroll = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vscroll.set)
        self.vscroll.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.content = ttk.Frame(self.canvas, style="Card.TFrame")
        self.content_id = self.canvas.create_window((0, 0), window=self.content, anchor="nw")

        # Make canvas resize its window width to match canvas width (keeps content responsive)
        def on_canvas_config(e):
            # update width of content window to canvas width minus scrollbar
            self.canvas.itemconfigure(self.content_id, width=e.width)
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.bind("<Configure>", on_canvas_config)

        # Update scrollregion when content changes
        def on_content_config(e):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.content.bind("<Configure>", on_content_config)

        # Choose Duration card
        choose_card = ttk.Frame(self.content, style="Card.TFrame", padding=10)
        choose_card.pack(fill="x", padx=40, pady=(12, 8))
        ttk.Label(choose_card, text="Choose Your Duration", font=FONT_BOLD, background=PANEL_BG, foreground=MUTED).pack(anchor="w")
        ttk.Label(choose_card, text="Select a time limit and start typing!", font=FONT_REGULAR, background=PANEL_BG, foreground=MUTED).pack(anchor="center", pady=8)

        dur_frame = ttk.Frame(choose_card, style="Card.TFrame")
        dur_frame.pack(pady=6)
        for secs in (30, 60, 120):
            b = ttk.Button(dur_frame, text=f"{secs} seconds", style="Primary.TButton", command=lambda s=secs: self.start_test(s))
            b.pack(side="left", padx=12, ipadx=6, ipady=6)

        # Typing area frame (responsive)
        self.typing_card = ttk.Frame(self.content, style="Card.TFrame", padding=8)
        # status and controls on top
        top_row = ttk.Frame(self.typing_card)
        top_row.pack(fill="x", pady=(6, 8))

        self.timer_lbl = ttk.Label(top_row, text="0s", font=FONT_REGULAR, background=PANEL_BG, foreground=MUTED)
        self.timer_lbl.pack(side="left", padx=(4, 16))
        self.wpm_lbl = ttk.Label(top_row, text="0 WPM", font=FONT_REGULAR, background=PANEL_BG, foreground=MUTED)
        self.wpm_lbl.pack(side="left", padx=(4, 16))
        self.acc_lbl = ttk.Label(top_row, text="100%", font=FONT_REGULAR, background=PANEL_BG, foreground=MUTED)
        self.acc_lbl.pack(side="left", padx=(4, 8))

        # progress full width
        self.progress = ttk.Progressbar(self.typing_card, orient="horizontal", mode="determinate")
        self.progress.pack(fill="x", padx=8, pady=(0, 8))

        # Flow frame holds word box and results panel side-by-side when wide
        self.flow_frame = ttk.Frame(self.typing_card)
        self.flow_frame.pack(fill="both", expand=True, padx=8, pady=8)

        # Left: word box (expands)
        left_frame = ttk.Frame(self.flow_frame)
        left_frame.pack(side="left", fill="both", expand=True)

        self.text_display = tk.Text(left_frame, height=8, wrap="word", font=("Courier New", 13),
                                    bg="white", padx=10, pady=10, state="disabled", bd=1, relief="solid")
        # make sure it expands
        self.text_display.pack(fill="both", expand=True)

        # Right: embedded results panel (hidden by default)
        self.results_panel = ttk.Frame(self.flow_frame, style="Card.TFrame", padding=8, width=320)
        # keep it from shrinking too small
        self.results_panel.pack(side="right", fill="y", padx=(12, 0), pady=4)
        self.results_panel.pack_forget()  # hidden initially

        # Results content
        stat_frame = ttk.Frame(self.results_panel)
        stat_frame.pack(fill="x", pady=(2,8))
        def make_stat(parent, small_text, big_text):
            f = ttk.Frame(parent, padding=4)
            small = ttk.Label(f, text=small_text, font=("Courier New", 10), foreground=MUTED)
            small.pack()
            big = ttk.Label(f, text=big_text, font=("Courier New", 12, "bold"), foreground=PRIMARY)
            big.pack()
            return f, big
        s1, self.res_wpm = make_stat(stat_frame, "Words Per Minute", "0")
        s2, self.res_acc = make_stat(stat_frame, "Accuracy", "100%")
        s3, self.res_time = make_stat(stat_frame, "Time Taken", "0s")
        s4, self.res_errs = make_stat(stat_frame, "Errors", "0")
        s1.grid(row=0, column=0, padx=6, pady=6, sticky="nsew")
        s2.grid(row=0, column=1, padx=6, pady=6, sticky="nsew")
        s3.grid(row=1, column=0, padx=6, pady=6, sticky="nsew")
        s4.grid(row=1, column=1, padx=6, pady=6, sticky="nsew")

        ttk.Label(self.results_panel, text="Errors (expected → typed)", font=("Courier New", 10), foreground=MUTED).pack(anchor="w", pady=(8,4))
        err_box_frame = ttk.Frame(self.results_panel)
        err_box_frame.pack(fill="both", expand=True)
        self.err_text = tk.Text(err_box_frame, height=8, wrap="word", font=("Courier New", 11), state="disabled", bd=1, relief="solid")
        self.err_text.pack(side="left", fill="both", expand=True)
        err_scroll = ttk.Scrollbar(err_box_frame, orient="vertical", command=self.err_text.yview)
        err_scroll.pack(side="right", fill="y")
        self.err_text.config(yscrollcommand=err_scroll.set)

        ttk.Button(self.results_panel, text="Try Again", command=self.reset_after_results, style="Primary.TButton").pack(fill="x", pady=(8,4))

        # Input entry under the flow_frame (full width)
        input_frame = ttk.Frame(self.typing_card)
        input_frame.pack(fill="x", padx=8, pady=(6,8))
        self.input_var = tk.StringVar()
        self.input_entry = ttk.Entry(input_frame, textvariable=self.input_var, font=("Courier New", 13))
        self.input_entry.pack(fill="x", expand=True)
        self.input_entry.bind("<space>", self.on_space)
        self.input_entry.bind("<Return>", self.on_space)

        # Controls row
        ctl_frame = ttk.Frame(self.typing_card)
        ctl_frame.pack(fill="x", padx=8, pady=(4,12))
        ttk.Button(ctl_frame, text="Stop Test", command=self.finish_test, style="Primary.TButton").pack(anchor="center")

        # typing_card initially hidden
        self.typing_card.pack_forget()

    # ===== logic =====
    def start_test(self, seconds):
        self.duration = seconds
        self.time_left = seconds
        self.started = False
        self.current_words = [random.choice(WORDS) for _ in range(80)]
        self.current_index = 0
        self.total_typed_chars = 0
        self.correct_chars = 0
        self.errors = []

        # show typing card and hide results panel
        self.typing_card.pack(fill="both", padx=24, pady=(8,12), expand=True)
        if self.results_visible:
            self.results_panel.pack_forget()
            self.results_visible = False

        self.update_text_display()
        self.progress["value"] = 0
        self.timer_lbl.config(text=f"{self.time_left}s")
        self.wpm_lbl.config(text="0 WPM")
        self.acc_lbl.config(text="100%")
        self.input_var.set("")
        self.input_entry.focus_set()

        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None

        self.input_entry.bind("<Key>", self._start_timer_once, add="+")

    def _start_timer_once(self, event=None):
        if not self.started:
            self.started = True
            self._tick()
        try:
            self.input_entry.unbind("<Key>")
        except Exception:
            pass

    def _tick(self):
        if self.time_left <= 0:
            self.finish_test()
            return
        self.time_left -= 1
        self.timer_lbl.config(text=f"{self.time_left}s")
        elapsed = self.duration - self.time_left
        if self.duration > 0:
            pct = (elapsed / self.duration) * 100
            self.progress["value"] = pct
        self.timer_job = self.root.after(1000, self._tick)

    def update_text_display(self):
        self.text_display.config(state="normal")
        self.text_display.delete("1.0", "end")
        for i, w in enumerate(self.current_words):
            if i == self.current_index:
                self.text_display.insert("end", w + " ", ("current",))
            else:
                self.text_display.insert("end", w + " ")
        self.text_display.tag_configure("current", font=("Courier New", 13, "bold"))
        self.text_display.config(state="disabled")

    def on_space(self, event=None):
        val = self.input_var.get().strip()
        expected = self.current_words[self.current_index] if self.current_index < len(self.current_words) else ""
        typed_len = len(val)
        self.total_typed_chars += typed_len
        local_correct = 0
        for i in range(max(len(expected), len(val))):
            if i < len(expected) and i < len(val) and expected[i] == val[i]:
                local_correct += 1
        self.correct_chars += local_correct
        if val != expected:
            self.errors.append({"index": self.current_index, "expected": expected, "typed": val})
        self.current_index += 1
        self.input_var.set("")
        self.update_text_display()
        elapsed_seconds = (self.duration - self.time_left) if self.duration else 0
        minutes = elapsed_seconds / 60 if elapsed_seconds > 0 else 1/60
        wpm = round((self.correct_chars / 5) / minutes) if minutes > 0 else 0
        acc = round((self.correct_chars / self.total_typed_chars) * 100) if self.total_typed_chars > 0 else 100
        self.wpm_lbl.config(text=f"{wpm} WPM")
        self.acc_lbl.config(text=f"{acc}%")
        return "break"

    def finish_test(self):
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None
        elapsed = (self.duration - self.time_left) if self.duration else 0
        minutes = elapsed / 60 if elapsed > 0 else 1/60
        wpm = round((self.correct_chars / 5) / minutes) if minutes > 0 else 0
        acc = round((self.correct_chars / self.total_typed_chars) * 100) if self.total_typed_chars > 0 else 100

        # modal dialog with results
        modal = tk.Toplevel(self.root)
        modal.title("Test Complete")
        modal.geometry("700x480")
        modal.transient(self.root)
        modal.grab_set()
        ttk.Label(modal, text="Test Complete!", font=FONT_BOLD).pack(pady=10)
        grid = ttk.Frame(modal)
        grid.pack(fill="x", padx=12)
        def add_stat(parent, small, big, col, row):
            f = ttk.Frame(parent, padding=6)
            f.grid(column=col, row=row, padx=6, pady=6, sticky="nsew")
            ttk.Label(f, text=small, foreground=MUTED).pack()
            ttk.Label(f, text=big, font=FONT_BOLD, foreground=PRIMARY).pack()
        add_stat(grid, "Words Per Minute", str(wpm), 0, 0)
        add_stat(grid, "Accuracy", f"{acc}%", 1, 0)
        add_stat(grid, "Time Taken", f"{elapsed}s", 0, 1)
        add_stat(grid, "Errors", str(len(self.errors)), 1, 1)

        err_frame = ttk.LabelFrame(modal, text="Errors (expected → typed)", padding=8)
        err_frame.pack(fill="both", expand=True, padx=12, pady=10)
        err_text = tk.Text(err_frame, height=8, wrap="word", state="normal")
        err_text.pack(fill="both", expand=True, side="left")
        err_scroll = ttk.Scrollbar(err_frame, orient="vertical", command=err_text.yview)
        err_scroll.pack(side="right", fill="y")
        err_text.config(yscrollcommand=err_scroll.set)
        if not self.errors:
            err_text.insert("end", "No typing errors — nice!\n")
        else:
            for i, e in enumerate(self.errors, 1):
                err_text.insert("end", f"{i}. (word #{e['index']+1}) expected: '{e['expected']}'  → typed: '{e['typed']}'\n")
        err_text.config(state="disabled")

        def modal_try_again():
            modal.destroy()
            self.reset_after_results()
        btn_frame = ttk.Frame(modal)
        btn_frame.pack(pady=8)
        ttk.Button(btn_frame, text="Try Again", command=modal_try_again, style="Primary.TButton").pack(side="left", padx=6)
        ttk.Button(btn_frame, text="Close", command=modal.destroy).pack(side="right", padx=6)

        # update embedded panel for errors tab
        self._populate_embedded_results(wpm, acc, elapsed, len(self.errors))

    def _populate_embedded_results(self, wpm, acc, elapsed, num_errors):
        self.res_wpm.config(text=str(wpm))
        self.res_acc.config(text=f"{acc}%")
        self.res_time.config(text=f"{elapsed}s")
        self.res_errs.config(text=str(num_errors))
        self.err_text.config(state="normal")
        self.err_text.delete("1.0", "end")
        if not self.errors:
            self.err_text.insert("end", "No typing errors — nice!\n")
        else:
            for i, e in enumerate(self.errors, 1):
                self.err_text.insert("end", f"{i}. (word #{e['index']+1}) expected: '{e['expected']}'  → typed: '{e['typed']}'\n")
        self.err_text.config(state="disabled")

    def toggle_errors_panel(self):
        if self.results_visible:
            self.results_panel.pack_forget()
            self.results_visible = False
        else:
            elapsed = (self.duration - self.time_left) if self.duration else 0
            minutes = elapsed / 60 if elapsed > 0 else 1/60
            wpm = round((self.correct_chars / 5) / minutes) if minutes > 0 else 0
            acc = round((self.correct_chars / self.total_typed_chars) * 100) if self.total_typed_chars > 0 else 100
            self._populate_embedded_results(wpm, acc, elapsed, len(self.errors))
            # show both typing area and results panel (side-by-side if there's enough width)
            self.typing_card.pack(fill="both", padx=24, pady=(8,12), expand=True)
            self.results_panel.pack(side="right", fill="y", padx=(12,0), pady=4)
            self.results_visible = True
            self.results_panel.focus_set()

    def reset_after_results(self):
        try:
            self.results_panel.pack_forget()
            self.typing_card.pack_forget()
        except Exception:
            pass
        self.results_visible = False
        self.progress["value"] = 0
        self.timer_lbl.config(text="0s")
        self.wpm_lbl.config(text="0 WPM")
        self.acc_lbl.config(text="100%")
        self.input_var.set("")
        self.started = False
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None
        self.total_typed_chars = 0
        self.correct_chars = 0

    def _scroll_top(self):
        self.canvas.yview_moveto(0)

if __name__ == "__main__":
    root = tk.Tk()
    app = TypeSpeedProApp(root)
    root.mainloop()
