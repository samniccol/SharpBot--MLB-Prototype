# watchlist_monitor.py

import json
from datetime import datetime, timedelta
import time

WATCHLIST_FILE = "watchlist.json"

def load_watchlist():
    try:
        with open(WATCHLIST_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_watchlist(watchlist):
    with open(WATCHLIST_FILE, "w") as f:
        json.dump(watchlist, f, indent=2)

def prune_and_get_active_watchlist():
    now = datetime.utcnow()
    watchlist = load_watchlist()

    fresh_watchlist = []
    for game in watchlist:
        try:
            start_time = datetime.fromisoformat(game["start_time"])
            if start_time + timedelta(hours=6) > now:
                fresh_watchlist.append(game)
        except Exception as e:
            print(f"⚠️ Error parsing start_time: {e}")

    save_watchlist(fresh_watchlist)
    return fresh_watchlist

def update_odds(game_id):
    print(f"📊 Updating odds for {game_id}")

def update_injuries(game_id):
    print(f"🩼 Checking injuries for {game_id}")

def generate_gpt_advice(game_id):
    print(f"🤖 GPT analyzing {game_id}")

def monitor_game(game):
    game_id = game["game_id"]
    print(f"👁️ Monitoring game: {game_id}")
    
    # Plug in your real logic here:
    update_odds(game_id)
    update_injuries(game_id)
    generate_gpt_advice(game_id)

def monitor_watchlist():
    now = datetime.utcnow()
    watchlist = prune_and_get_active_watchlist()

    for game in watchlist:
        start_time = datetime.fromisoformat(game["start_time"])
        if now >= start_time - timedelta(hours=1):
            monitor_game(game)
        else:
            print(f"⏳ Too early to monitor {game['game_id']} (starts at {start_time})")
