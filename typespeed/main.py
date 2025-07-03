from utils import get_text
import time
import random
import tkinter as tk
from tkinter import font, messagebox
from error_utils import generate_user_friendly_errors

class TypingSpeedTest:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")
        self.root.geometry("800x600")
        self.root.configure(bg='#F0F0F0')

        # Custom fonts
        self.title_font = font.Font(family="Helvetica", size=24, weight="bold")
        self.text_font = font.Font(family="Courier New", size=16)
        self.result_font = font.Font(family="Arial", size=14, weight="bold")

        # Initialize variables
        self.start_time = None
        self.running = False
        self.original_text = ""

        # Build UI
        self.setup_ui()
        self.new_test()

    def setup_ui(self):
        self.header = tk.Label(self.root, text="Typing Speed Test", font=self.title_font, bg='#F0F0F0', fg='#2C3E50')
        self.header.pack(pady=20)

        self.sample_frame = tk.Frame(self.root, bg='white', padx=20, pady=20)
        self.sample_frame.pack(pady=10, fill=tk.X, padx=40)

        self.sample_label = tk.Label(
            self.sample_frame,
            text="",
            font=self.text_font,
            bg='white',
            fg='#34495E',
            wraplength=700,
            justify=tk.LEFT
        )
        self.sample_label.pack()

        self.input_text = tk.Text(
            self.root,
            font=self.text_font,
            height=5,
            width=60,
            padx=10,
            pady=10,
            wrap=tk.WORD,
            bg='#FFFFFF'
        )
        self.input_text.pack(pady=20)
        self.input_text.bind("<KeyPress>", self.start_timer)

        self.btn_frame = tk.Frame(self.root, bg='#F0F0F0')
        self.btn_frame.pack(pady=10)

        self.restart_btn = tk.Button(
            self.btn_frame,
            text="New Test",
            font=self.text_font,
            command=self.new_test,
            bg='#3498DB',
            fg='white'
        )
        self.restart_btn.pack(side=tk.LEFT, padx=10)

        self.done_btn = tk.Button(
            self.btn_frame,
            text="Done",
            font=self.text_font,
            command=self.show_done_results,
            bg='#2ECC71',
            fg='white'
        )
        self.done_btn.pack(side=tk.LEFT, padx=10)

        self.result_label = tk.Label(
            self.root,
            text="Click the text area below to start typing!",
            font=self.result_font,
            bg='#F0F0F0',
            fg='#27AE60'
        )
        self.result_label.pack(pady=20)

    def new_test(self):
        self.original_text = get_text()
        self.sample_label.config(text=self.original_text)
        self.input_text.delete('1.0', tk.END)
        self.result_label.config(text="Click the text area below to start typing!", fg='#27AE60')
        self.running = False
        self.start_time = None
        self.input_text.config(bg='#FFFFFF', state=tk.NORMAL)
        self.input_text.focus_set()
        self.done_btn.config(state=tk.NORMAL)
        self.input_text.delete('1.0', tk.END)

    def start_timer(self, event):
        if not self.running:
            self.running = True
            self.start_time = time.time()
            self.input_text.config(bg='#F9EBEA')
            self.result_label.config(text="Typing...", fg='#E74C3C')
            self.root.after(100, self.update_timer)

        self.check_completion()

    def update_timer(self):
        if self.running:
            elapsed = time.time() - self.start_time
            wpm = self.calculate_wpm(elapsed)
            self.result_label.config(text=f"Elapsed Time: {elapsed:.1f}s | WPM: {wpm}")
            self.root.after(1000, self.update_timer)

    def calculate_wpm(self, elapsed):
        typed_text = self.input_text.get('1.0', 'end-1c')
        typed_words = len(typed_text.split())
        return int(typed_words / (elapsed / 60)) if elapsed > 0 else 0

    def check_completion(self):
        user_input = self.input_text.get('1.0', 'end-1c')
        if user_input == self.original_text:
            self.show_final_results()

    def show_final_results(self):
        self.running = False
        self.input_text.config(state=tk.DISABLED)
        elapsed_time = time.time() - self.start_time
        user_input = self.input_text.get('1.0', 'end-1c')

        min_length = min(len(self.original_text), len(user_input))
        correct = sum(1 for o, t in zip(self.original_text, user_input) if o == t)
        accuracy = (correct / len(self.original_text)) * 100 if len(self.original_text) > 0 else 0
        wpm = self.calculate_wpm(elapsed_time)

        result_text = (
            f"Time: {elapsed_time:.2f}s | WPM: {wpm} | Accuracy: {accuracy:.1f}%\n"
            "Press 'New Test' to try again!"
        )

        if user_input == self.original_text:
            result_text = "Perfect! " + result_text

        self.result_label.config(text=result_text, fg='#27AE60')
        self.input_text.config(bg='#EAFAF1')
        self.done_btn.config(state=tk.DISABLED)

    def show_done_results(self):
        if not self.running:
            return

        self.running = False
        self.input_text.config(state=tk.DISABLED)

        elapsed_time = time.time() - self.start_time
        user_input = self.input_text.get('1.0', 'end-1c')
        wpm = self.calculate_wpm(elapsed_time)

        result_text = (
            f"Finished!\nTime: {elapsed_time:.2f}s | WPM: {wpm}\n"
            "Press 'New Test' to try again!"
        )

        self.result_label.config(text=result_text, fg='#2980B9')
        self.input_text.config(bg='#E8F8F5')
        self.done_btn.config(state=tk.DISABLED)

        # self.show_typing_errors(user_input)
        self.show_error_popup(self.original_text, user_input)

    # 🔍 Error Display Box
    def show_typing_errors(self, user_input):
        error_list = []
        original = self.original_text
        min_len = min(len(original), len(user_input))

        for i in range(min_len):
            if original[i] != user_input[i]:
                error_list.append(f"Position {i+1}: Expected '{original[i]}', but got '{user_input[i]}'")

        if len(user_input) > len(original):
            extra = user_input[len(original):]
            error_list.append(f"Extra characters: '{extra}'")
        elif len(user_input) < len(original):
            missing = original[len(user_input):]
            error_list.append(f"Missing characters: '{missing}'")

        if error_list:
            error_window = tk.Toplevel(self.root)
            error_window.title("Typing Errors")
            error_window.geometry("500x300")
            error_window.configure(bg='white')

            title = tk.Label(error_window, text="Typing Errors", font=self.title_font, fg='red', bg='white')
            title.pack(pady=10)

            error_box = tk.Text(error_window, font=self.text_font, wrap=tk.WORD, bg='#FCF3CF', fg='black')
            error_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

            error_text = "\n".join(error_list)
            error_box.insert(tk.END, error_text)
            error_box.config(state=tk.DISABLED)
        else:
            messagebox.showinfo("Great!", "No typing errors found. Well done!")

    # def show_error_popup(self, expected, typed):
    #     result = generate_user_friendly_errors(expected, typed)
    #     win = tk.Toplevel(self.root)
    #     win.title("Typing Errors")
    #     win.geometry("600x400")
    #     win.configure(bg='white')

    #     txt = tk.Text(win, wrap='word', font=("Courier New", 12), bg='white', fg='black')
    #     txt.pack(expand=True, fill='both', padx=10, pady=10)

    #     scroll = tk.Scrollbar(txt, command=txt.yview)
    #     txt.configure(yscrollcommand=scroll.set)
    #     scroll.pack(side=tk.RIGHT, fill=tk.Y)

    #     txt.insert(tk.END, result)
    #     txt.config(state='disabled')
    def show_error_popup(self, expected_text, user_input):
        from error_utils import generate_user_friendly_errors

        raw_output = generate_user_friendly_errors(expected_text, user_input)

        # Create a popup window
        popup = tk.Toplevel(self.root)
        popup.title("Typing Errors")
        popup.geometry("600x400")
        popup.configure(bg="#FDFEFE")

        # Scrollable Text Widget
        text_widget = tk.Text(popup, wrap=tk.WORD, font=("Courier New", 12))
        text_widget.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Define bold tag
        text_widget.tag_configure("bold", font=("Courier New", 12, "bold"))

        # Insert content and apply bold for **...**
        idx = 0
        while idx < len(raw_output):
            if raw_output[idx:idx+2] == "**":
                idx += 2
                bold_start = idx
                while idx < len(raw_output) and raw_output[idx:idx+2] != "**":
                    idx += 1
                bold_text = raw_output[bold_start:idx]
                text_widget.insert(tk.END, bold_text, "bold")
                idx += 2  # Skip closing **
            else:
                text_widget.insert(tk.END, raw_output[idx])
                idx += 1

        text_widget.config(state=tk.DISABLED)


# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    app = TypingSpeedTest(root)
    root.mainloop()
