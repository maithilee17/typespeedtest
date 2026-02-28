# type_speed_pro.py
import tkinter as tk
from tkinter import ttk, messagebox
import random
import time

WORDS = [
    "way","look","take","three","four","car","follow","a","but","which","got",
    "product","wind","who","king","far","have","always","list","from",
    "quick","brown","fox","jumps","over","lazy","dog"
]

class TypeSpeedPro:
    def __init__(self, root):
        self.root = root
        root.title("TypeSpeed Pro")
        root.geometry("900x700")
        root.resizable(False, False)

        # State
        self.duration = 60
        self.time_left = 0
        self.timer_job = None
        self.started = False
        self.start_time = None

        self.current_words = []
        self.current_index = 0
        self.total_typed_chars = 0
        self.correct_chars = 0
        self.errors = []  # list of dicts: {index, expected, typed}

        self._build_ui()

    def _build_ui(self):
        # Header
        header = ttk.Frame(self.root)
        header.pack(pady=12)
        title = ttk.Label(header, text="TypeSpeed Pro", font=("Helvetica", 30, "bold"), foreground="#6f7bf2")
        title.pack()

        # Tabs area (we only have Typing Test and Errors button)
        tab_frame = ttk.Frame(self.root)
        tab_frame.pack(pady=10, fill="x", padx=40)
        self.typing_tab_btn = ttk.Button(tab_frame, text="Typing Test", command=lambda: None)
        self.typing_tab_btn.pack(side="left")
        self.errors_tab_btn = ttk.Button(tab_frame, text="Errors", command=self.show_errors_modal)
        self.errors_tab_btn.pack(side="left", padx=(8,0))

        # Main card
        container = ttk.Frame(self.root)
        container.pack(pady=20, fill="both", expand=True, padx=40)

        # Choose duration card
        choose_card = ttk.LabelFrame(container, text="Choose Your Duration", padding=16)
        choose_card.pack(fill="x", padx=50, pady=(0,16))

        label = ttk.Label(choose_card, text="Select a time limit and start typing!", foreground="#666")
        label.pack(pady=(0,10))

        dur_frame = ttk.Frame(choose_card)
        dur_frame.pack()
        for secs in (30, 60, 120):
            b = ttk.Button(dur_frame, text=f"{secs} seconds", command=lambda s=secs: self.start_test(s))
            b.pack(side="left", padx=10, ipadx=8, ipady=6)

        # Typing area (initially hidden via pack_forget)
        self.typing_card = ttk.Frame(container)
        # Status row
        status = ttk.Frame(self.typing_card)
        status.pack(fill="x", pady=(6,12))
        self.timer_lbl = ttk.Label(status, text="0s", font=("Helvetica", 14))
        self.timer_lbl.pack(side="left", padx=6)
        self.wpm_lbl = ttk.Label(status, text="0 WPM", font=("Helvetica", 14))
        self.wpm_lbl.pack(side="left", padx=18)
        self.acc_lbl = ttk.Label(status, text="100%", font=("Helvetica", 14))
        self.acc_lbl.pack(side="left", padx=18)

        # Progress bar
        self.progress = ttk.Progressbar(self.typing_card, orient="horizontal", length=760, mode="determinate")
        self.progress.pack(pady=10)

        # Text display (read-only)
        text_frame = ttk.Frame(self.typing_card, padding=8)
        text_frame.pack(fill="both", pady=8)
        self.text_display = tk.Text(text_frame, height=6, wrap="word", font=("Helvetica", 14), state="disabled", padx=10, pady=10)
        self.text_display.pack(fill="both")

        # Input
        input_frame = ttk.Frame(self.typing_card)
        input_frame.pack(fill="x", pady=(10,6))
        self.input_var = tk.StringVar()
        self.input_entry = ttk.Entry(input_frame, textvariable=self.input_var, font=("Helvetica", 14))
        self.input_entry.pack(fill="x", padx=10, ipady=6)
        self.input_entry.bind("<space>", self.on_space)
        self.input_entry.bind("<Return>", self.on_space)

        # Controls
        ctl_frame = ttk.Frame(self.typing_card)
        ctl_frame.pack(pady=12)
        self.stop_btn = ttk.Button(ctl_frame, text="Stop Test", command=self.finish_test)
        self.stop_btn.pack()

        # Results modal is Toplevel created when needed

    def start_test(self, seconds):
        # Reset state
        self.duration = seconds
        self.time_left = seconds
        self.started = False
        self.start_time = None
        self.current_words = [random.choice(WORDS) for _ in range(80)]
        self.current_index = 0
        self.total_typed_chars = 0
        self.correct_chars = 0
        self.errors = []

        # Show typing card
        self.typing_card.pack(fill="both", padx=50, pady=8)
        self.update_text_display()
        self.progress["value"] = 0
        self.timer_lbl.config(text=f"{self.time_left}s")
        self.wpm_lbl.config(text="0 WPM")
        self.acc_lbl.config(text="100%")

        # focus input
        self.input_var.set("")
        self.input_entry.focus_set()

        # If previous timer running, cancel
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None

        # start on first input to follow same behaviour as web version
        # We'll still show time but only begin counting after first typed char
        # (Start timer on first input event)
        self.input_entry.bind("<Key>", self._start_timer_on_first_key, add="+")
        # ensure modal hidden if present
        # (If user had result modal open previously, it's separate Toplevel so nothing to hide here)

    def _start_timer_on_first_key(self, event):
        # Only start the timer once
        if not self.started:
            self.started = True
            self.start_time = time.time()
            self._tick()

        # unbind this small starter so it doesn't run repeatedly
        try:
            self.input_entry.unbind("<Key>", None)
        except Exception:
            pass

    def _tick(self):
        # Called every 1s when timer running
        if self.time_left <= 0:
            self.finish_test()
            return
        self.time_left -= 1
        self.timer_lbl.config(text=f"{self.time_left}s")
        elapsed = self.duration - self.time_left
        if self.duration > 0:
            pct = (elapsed / self.duration) * 100
            self.progress["value"] = pct
        # schedule next
        self.timer_job = self.root.after(1000, self._tick)

    def update_text_display(self):
        # Render words with current word highlighted (simple bold)
        self.text_display.config(state="normal")
        self.text_display.delete("1.0", "end")
        for i,w in enumerate(self.current_words):
            if i == self.current_index:
                self.text_display.insert("end", w + " ", ("current",))
            else:
                self.text_display.insert("end", w + " ")
        self.text_display.tag_configure("current", font=("Helvetica", 14, "bold"))
        self.text_display.config(state="disabled")

    def on_space(self, event=None):
        val = self.input_var.get().strip()
        expected = ""
        if self.current_index < len(self.current_words):
            expected = self.current_words[self.current_index]
        else:
            expected = ""

        # Update typed counts
        typed_len = len(val)
        self.total_typed_chars += typed_len
        # count correct characters
        local_correct = 0
        maxlen = max(len(val), len(expected))
        for i in range(maxlen):
            if i < len(val) and i < len(expected) and val[i] == expected[i]:
                local_correct += 1
        self.correct_chars += local_correct

        if val != expected:
            self.errors.append({"index": self.current_index, "expected": expected, "typed": val})

        # move on
        self.current_index += 1
        self.input_var.set("")
        self.update_text_display()

        # Update WPM and accuracy
        elapsed_seconds = (self.duration - self.time_left) if self.duration else 1
        minutes = elapsed_seconds / 60 if elapsed_seconds > 0 else 1/60
        wpm = round((self.correct_chars / 5) / minutes) if minutes > 0 else 0
        acc = round((self.correct_chars / self.total_typed_chars) * 100) if self.total_typed_chars > 0 else 100

        self.wpm_lbl.config(text=f"{wpm} WPM")
        self.acc_lbl.config(text=f"{acc}%")

        return "break"

    def finish_test(self):
        # stop timer
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None
        elapsed = (self.duration - self.time_left) if self.duration else 0
        minutes = elapsed / 60 if elapsed > 0 else 1/60
        wpm = round((self.correct_chars / 5) / minutes) if minutes > 0 else 0
        acc = round((self.correct_chars / self.total_typed_chars) * 100) if self.total_typed_chars > 0 else 100

        # Show results modal (Toplevel)
        self._show_result_modal(wpm, acc, elapsed, len(self.errors))

    def _show_result_modal(self, wpm, acc, elapsed_seconds, num_errors):
        top = tk.Toplevel(self.root)
        top.title("Test Complete")
        top.geometry("700x520")
        top.resizable(False, False)
        # Make modal (block main window)
        top.transient(self.root)
        top.grab_set()

        h = ttk.Label(top, text="Test Complete!", font=("Helvetica", 22, "bold"))
        h.pack(pady=14)

        # Grid of results
        grid = ttk.Frame(top)
        grid.pack(pady=8, padx=12, fill="x")

        def box(parent, small, big):
            f = ttk.Frame(parent, relief="flat", padding=12)
            s = ttk.Label(f, text=small, foreground="#888")
            s.pack()
            b = ttk.Label(f, text=big, font=("Helvetica", 18, "bold"), foreground="#6f7bf2")
            b.pack()
            return f

        r1c1 = box(grid, "Words Per Minute", str(wpm))
        r1c1.grid(row=0, column=0, padx=8, pady=8, sticky="nsew")
        r1c2 = box(grid, "Accuracy", f"{acc}%")
        r1c2.grid(row=0, column=1, padx=8, pady=8, sticky="nsew")
        r2c1 = box(grid, "Time Taken", f"{elapsed_seconds}s")
        r2c1.grid(row=1, column=0, padx=8, pady=8, sticky="nsew")
        r2c2 = box(grid, "Errors", str(num_errors))
        r2c2.grid(row=1, column=1, padx=8, pady=8, sticky="nsew")

        # Errors list
        errors_frame = ttk.LabelFrame(top, text="Errors (expected → typed)")
        errors_frame.pack(fill="both", padx=12, pady=10, expand=True)
        errors_box = tk.Text(errors_frame, height=8, state="normal")
        errors_box.pack(fill="both", padx=6, pady=6, expand=True)
        if not self.errors:
            errors_box.insert("end", "No typing errors — nice!\n")
        else:
            for i, e in enumerate(self.errors, 1):
                errors_box.insert("end", f"{i}. (word #{e['index']+1}) expected: '{e['expected']}'  → typed: '{e['typed']}'\n")
        errors_box.config(state="disabled")

        # Try again
        btn = ttk.Button(top, text="Try Again", command=lambda: (top.destroy(), self._reset_after_modal()))
        btn.pack(pady=10)

    def _reset_after_modal(self):
        # hide typing area and reset UI so user can pick duration
        try:
            self.typing_card.pack_forget()
        except Exception:
            pass
        self.progress["value"] = 0
        self.timer_lbl.config(text="0s")
        self.wpm_lbl.config(text="0 WPM")
        self.acc_lbl.config(text="100%")
        self.input_var.set("")
        self.started = False
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None

    def show_errors_modal(self):
        # If errors exist from last run show them; else show message
        top = tk.Toplevel(self.root)
        top.title("Errors")
        top.geometry("600x360")
        top.resizable(False, False)
        top.transient(self.root)
        top.grab_set()

        h = ttk.Label(top, text="Typing Errors", font=("Helvetica", 16, "bold"))
        h.pack(pady=10)
        frame = ttk.Frame(top)
        frame.pack(fill="both", expand=True, padx=10, pady=8)
        box = tk.Text(frame, height=12)
        box.pack(fill="both", expand=True)
        if not self.errors:
            box.insert("end", "No errors recorded yet. Run a test first.\n")
        else:
            for i, e in enumerate(self.errors, 1):
                box.insert("end", f"{i}. (word #{e['index']+1}) expected: '{e['expected']}'  → typed: '{e['typed']}'\n")
        box.config(state="disabled")
        btn = ttk.Button(top, text="Close", command=top.destroy)
        btn.pack(pady=8)


if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style(root)
    # optional: set theme
    try:
        style.theme_use("clam")
    except Exception:
        pass
    app = TypeSpeedPro(root)
    root.mainloop()
