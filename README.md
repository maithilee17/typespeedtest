#  Typing Speed Test - Python Tkinter GUI Application

##  Project Overview

This **Typing Speed Test** is a Python GUI application built using **Tkinter** that allows users to test and improve their typing speed and accuracy. The app displays a randomly chosen text for the user to type and calculates typing metrics such as **Words Per Minute (WPM)**, **accuracy**, and **time taken**. Additionally, the application highlights typing errors and provides detailed feedback in a pop-up window.

---

##  What I Learned From This Project

### 1] GUI Design with Tkinter
- Designing professional and responsive GUI layouts using `Frame`, `Label`, `Text`, `Button`, and `Toplevel` widgets.
- Customizing widget fonts, colors, paddings, and layouts using `tkinter.font` and geometry managers.
- Handling keyboard events (`<KeyPress>`) to trigger timers and capture user input dynamically.

### 2] Timer & Real-Time Feedback
- Implementing real-time timers using `time.time()` and `after()` loops to track typing duration.
- Displaying **WPM** dynamically while typing.

### 3] Typing Accuracy Evaluation
- Comparing expected and typed text character-by-character and word-by-word.
- Calculating **accuracy percentage** and identifying **extra/missing words** or incorrect characters.

### 4] Error Analysis with `difflib`
- Using Python’s `difflib.SequenceMatcher` to compare strings and highlight differences.
- Building a clear and user-friendly error display with bold highlights for mistakes using `Text` widget formatting.

### 5] Modular Python Coding
- Separating logic into multiple files for clean and maintainable structure:
  - `main.py`: Application logic and GUI
  - `utils.py`: Random sentence generator
  - `error_utils.py`: Typing error detection and formatting

---

##  Features

- 1. Clean and user-friendly GUI using Tkinter
- 2. Real-time typing timer with live WPM calculation
- 3. Accuracy calculation and performance summary
- 4. Intelligent error analysis (incorrect characters, extra/missing words)
- 5. Pop-up error report with highlighted mistakes
- 6. "New Test" button for multiple attempts

---

##  Technologies Used

| Category       | Tools / Libraries          |
|----------------|-----------------------------|
| Language       | Python 3.x                  |
| GUI Framework  | Tkinter                     |
| Utility Module | `difflib`, `random`, `time` |
| Fonts & Design | `tkinter.font`, `messagebox` |

---

##  How to Run the Project

###  Prerequisites
- Python 3.x installed on your system

###  File Structure
```

typing-speed-test/
│
├── main.py                 # Main application logic and GUI
├── utils.py                # Function to generate random texts
├── error\_utils.py          # Error checking and display functions
└── README.md               # Project documentation

````

###  Steps to Launch

1. **Clone Or Download the Repository**
  t

2. **Run the Application**

   ```bash
   python main.py
   ```

3. **Using the App**

   * Click in the text box to start typing.
   * As you type, real-time stats (WPM, time) are shown.
   * Click **"Done"** to finish typing and see results.
   * Get detailed typing errors in a popup.
   * Click **"New Test"** to try again with a different prompt.

---

##  Example Output

```
Elapsed Time: 12.3s | WPM: 40
Perfect! Time: 12.3s | WPM: 40 | Accuracy: 100.0%
Press 'New Test' to try again!
```

#### Typing Errors Pop-up

```
Total Mistakes: 3

Mistake at "programming" at character 5:
Expected: prog**ram**ming
Typed:    prog**lom**ming

✱ Extra words added: and engaging
✱ Missing words: your
```

---

##  Future Improvements

* [i]   Add audio feedback for typing speed
* [ii]  Store typing history in a file or database
* [iii] Add custom paragraph input for advanced tests
* [iv]  Display charts of performance over time

---

## License

This project is developed for educational purposes. Feel free to use and modify it as needed.

---

