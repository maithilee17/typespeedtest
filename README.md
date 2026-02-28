# ⌨️ TypeSpeed Pro — Typing Speed Test (Tkinter)

TypeSpeed Pro is a modern and responsive **typing speed test desktop application** built using **Python and Tkinter**.  
It allows users to measure their **Words Per Minute (WPM), Accuracy, and Errors** in a clean and distraction-free interface.

---

## 🚀 Features

- ⏱️ Multiple test durations (30, 60, 120 seconds)
- ⚡ Real-time WPM calculation
- 🎯 Accuracy tracking
- ❌ Detailed error tracking (expected vs typed)
- 📊 Progress bar and timer
- 🧾 Results summary popup
- 📱 Responsive and modern UI
- 🔁 Try Again option
- 🖥️ Lightweight — no external dependencies

---

## 🛠️ Tech Stack

- Python 3.x
- Tkinter (GUI library)
- ttk (Themed Tkinter widgets)
- Standard Python libraries (random, time)

---

## 📂 Project Structure

```
Type_Speed_Pro/
│
├── app.py
├── venv/ (optional virtual environment)
└── README.md
```

---

## ⚙️ Requirements

- Python 3.8 or higher
- Tkinter (included with Python)

Check Python version:

```
python --version
```

---

## ▶️ How to Run

### Step 1: Open terminal in project folder

```
cd Type_Speed_Pro
```

### Step 2: Run the application

```
python app.py
```

OR

```
py app.py
```

---

## 🧠 How It Works

1. Select test duration (30 / 60 / 120 seconds)
2. Start typing the displayed words
3. The timer starts automatically when you begin typing
4. App calculates:
   - Words Per Minute (WPM)
   - Accuracy (%)
   - Errors
5. Results are shown after test completion

---

## 📊 Metrics Explained

**WPM (Words Per Minute)**  
```
WPM = (Correct Characters / 5) ÷ Time in Minutes
```

**Accuracy**
```
Accuracy = (Correct Characters / Total Typed Characters) × 100
```

---

## 🎨 UI Features

- Modern clean design
- Responsive layout
- Scrollable content
- Error analysis panel
- Progress tracking

---

## 🔮 Future Enhancements

- User profiles
- High score tracking
- Difficulty levels
- Dark mode
- Sound feedback
- Online leaderboard

---

## 👨‍💻 Developer

**Maithilee Bhatkar**

---

## 📜 License

MIT License — Free for personal and commercial use.

---

## ⭐ Support

If you like this project:

- Give it a ⭐ on GitHub
- Share with others
- Suggest improvements
