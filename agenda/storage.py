import json
import os
from models import Task

FILE_PATH = "tasks.json"

def save_tasks(tasks):
    with open(FILE_PATH, "w") as f:
        json.dump([task.to_dict() for task in tasks], f)

def load_tasks():
    if not os.path.exists(FILE_PATH):
        return []
    with open(FILE_PATH, "r") as f:
        data = json.load(f)
        return [Task.from_dict(d) for d in data]
