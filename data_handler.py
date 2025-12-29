# data_handler.py - ENHANCED
import json
import os
from datetime import datetime, timedelta

DATA_FILE = "user_data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {
            "character": "goku",
            "habits": [],
            "aura_points": 0,
            "history": {},
            "settings": {
                "theme": "dark",
                "notifications": True,
                "daily_reminder": "20:00"
            }
        }
    
    with open(DATA_FILE, "r") as f:
        try:
            data = json.load(f)
            # Ensure all required fields exist
            data.setdefault("settings", {})
            data.setdefault("history", {})
            data.setdefault("habits", [])
            data.setdefault("aura_points", 0)
            return data
        except json.JSONDecodeError:
            return get_default_data()

def get_default_data():
    return {
        "character": "goku",
        "habits": [],
        "aura_points": 0,
        "history": {},
        "settings": {
            "theme": "dark",
            "notifications": True,
            "daily_reminder": "20:00"
        }
    }

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_habit(data, habit, category="General"):
    habit_obj = {
        "name": habit,
        "category": category,
        "created": datetime.now().isoformat(),
        "streak": 0,
        "total_completions": 0
    }
    
    if habit not in [h["name"] for h in data["habits"]]:
        data["habits"].append(habit_obj)
    save_data(data)

def mark_habit_done(data, habit_name, date=None):
    if date is None:
        date = str(datetime.now().date())
    
    if date not in data["history"]:
        data["history"][date] = []
    
    if habit_name not in data["history"][date]:
        data["history"][date].append(habit_name)
        data["aura_points"] += 10
        
        # Update habit streak
        for habit in data["habits"]:
            if habit["name"] == habit_name:
                habit["streak"] += 1
                habit["total_completions"] += 1
                break
    
    save_data(data)
    return data["aura_points"]

def get_streak(data):
    """Calculate current streak in days"""
    if not data["history"]:
        return 0
    
    dates = sorted([datetime.strptime(d, "%Y-%m-%d") for d in data["history"].keys()])
    today = datetime.now().date()
    streak = 0
    
    for i in range(len(dates)-1, -1, -1):
        if dates[i].date() == today - timedelta(days=streak):
            streak += 1
        else:
            break
    
    return streak