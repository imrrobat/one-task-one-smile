import csv
import os

task_file="tasks.csv"

def load_tasks():
    headers = ["id", "title", "category", "priority", "is_done", "done_date"]

    if not os.path.exists(task_file):
        with open(task_file, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)

    tasks = []
    with open(task_file, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["is_done"].lower() == "false":
                tasks.append(row)

    return tasks

def add_task(title: str, priority: int, category: str):
    if not os.path.exists(task_file):
        with open(task_file, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "title", "category", "priority", "is_done", "done_date"])
            
    last_id = 0
    with open(task_file, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            last_id = max(last_id, int(row["id"]))

    new_id = last_id + 1

    with open(task_file, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([new_id, title, category, priority, False, ""])

    print(f"✅ Task {new_id} added: {title}")