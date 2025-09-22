import csv
import os
import jdatetime

task_file="tasks.csv"
data_file = "data.csv"

def summary_info():
    if not os.path.exists(task_file):
        return {"total": 0, "month_total": 0, "today_total": 0}

    total = 0
    month_total = 0
    today_total = 0

    today_j = jdatetime.date.today()
    current_year = today_j.year
    current_month = today_j.month
    current_day = today_j.day

    with open(task_file, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["is_done"].lower() != "true":
                continue 

            try:
                priority = int(row["priority"])
            except ValueError:
                continue  

            total += priority

            done_date_str = row["done_date"].strip()
            if done_date_str:
                try:
                    done_date = jdatetime.date.fromisoformat(done_date_str)
                    if done_date.year == current_year and done_date.month == current_month:
                        month_total += priority
                    if done_date.year == current_year and done_date.month == current_month and done_date.day == current_day:
                        today_total += priority
                except Exception:
                    continue 

    return {"total": total, "month_total": month_total, "today_total": today_total}

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

    print(f"✅ Task {new_id} added.")
    
def mark_task_done(title: str, done_date_str: str):
    if not os.path.exists(task_file):
        print("File does not exist")
        return False

    updated = False
    tasks = []
    
    with open(task_file, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        for row in reader:
            if row["title"] == title and row["is_done"] == "False" and not updated:
                row["is_done"] = "True"
                row["done_date"] = done_date_str
                updated = True
            tasks.append(row)

    with open(task_file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(tasks)

    if updated:
        print(f"✅ Task marked as done")
        return True
    else:
        print(f"Task not found or already done")
        return False

def get_task(title: str):
    if not os.path.exists(task_file):
        return None

    with open(task_file, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["title"] == title:
                return row

    return None


def delete_task(title: str):
    if not os.path.exists(task_file):
        print("File does not exist")
        return False

    tasks_kept = []
    task_deleted = None

    with open(task_file, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        for row in reader:
            if row["title"] == title and task_deleted is None:
                task_deleted = row
            else:
                tasks_kept.append(row)

    with open(task_file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(tasks_kept)

    if task_deleted:
        print(f"✅ Task '{title}' deleted")
        return True
    else:
        print(f"Task '{title}' not found")
        return False


def load_data_file():
    if not os.path.exists(data_file):
        with open(data_file, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["score", "count_tasks"])
            writer.writerow([0, 0])
        return {"score": 0, "count_tasks": 0}

    data_dict = {}
    with open(data_file, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for key, value in row.items():
                try:
                    data_dict[key] = int(value)
                except ValueError:
                    data_dict[key] = value
            break 
    return data_dict


def update_data(score_inc=0, count_tasks_inc=0):
    if not os.path.exists(data_file):
        with open(data_file, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["score", "count_tasks"])
            writer.writerow([0, 0])

    data_dict = {}
    with open(data_file, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                data_dict["score"] = int(row["score"])
            except ValueError:
                data_dict["score"] = 0
            try:
                data_dict["count_tasks"] = int(row["count_tasks"])
            except ValueError:
                data_dict["count_tasks"] = 0
            break 

    data_dict["score"] += score_inc
    data_dict["count_tasks"] += count_tasks_inc

    with open(data_file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["score", "count_tasks"])
        writer.writeheader()
        writer.writerow(data_dict)

    return data_dict

def today_log(date_str: str):
    if not os.path.exists(task_file):
        return []

    tasks = []
    with open(task_file, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["is_done"] == "True" and row["done_date"] == date_str:
                tasks.append(row)

    return tasks