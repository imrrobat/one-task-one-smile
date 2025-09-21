# OTOS - One Task One Smile ✅😊

OTOS is a simple task management application built with **Python** and **NiceGUI**.  
The goal is to bring productivity and positivity together: **Complete one task, earn one smile!**

---

## ✨ Features
- Add new tasks with:
  - Title  
  - Category (Work, Personal Growth, Fun/Relaxation)  
  - Priority (1–10)  
- View all tasks in a clean dashboard  
- Mark tasks as done (automatically records the done date)  
- Track your overall progress and smiles  
- Data is stored in simple CSV files (`tasks.csv`, `data.csv`)  

---

## 📂 Project Structure
```

.
├── main.py        # Main application
├── tasks.csv      # Task data (ignored in git)
├── data.csv       # Global stats (ignored in git)
└── README.md

```

---

## 🚀 Installation & Usage
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/one-task-one-smile.git
   cd one-task-one-smile
```

2. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Linux/Mac
   venv\Scripts\activate      # On Windows
   ```

3. Install dependencies:

   ```bash
   pip install nicegui jdatetime
   ```

4. Run the app:

   ```bash
   python main.py
   ```

5. Open the app in your browser at:

   ```
   http://localhost:8080
   ```

6. See day progress in:

   ```
   http://localhost:8080/today
   ```
---

## 📝 Notes

* `tasks.csv` and `data.csv` are created automatically if they don't exist.
* Both files are ignored in Git (`.gitignore`), so your personal tasks and stats remain private.

---

## 💡 Idea

The philosophy behind OTOS is simple:

> Every small step you complete should bring you a smile.
> One Task = One Smile.

---

## 📜 License

This project is licensed under the MIT License.
Feel free to use, modify, and share it.
