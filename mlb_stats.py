import requests
import json
from datetime import datetime, timedelta

CACHE_FILE = "cached_stats.json"
FRESHNESS_THRESHOLD = timedelta(hours=12)
SPORTRADAR_API_KEY = "your_sportradar_api_key"  # or load from .env
BASE_URL = "https://api.sportradar.com/mlb/trial/v8/en"

def should_fetch_new_stats():
    try:
        with open(CACHE_FILE, "r") as f:
            data = json.load(f)
            if not data:
                return True
            # Check if the last fetch time is older than the freshness threshold
            last_fetch_time = datetime.fromisoformat(data.get("last_fetch"))
            return datetime.now() - last_fetch_time > FRESHNESS_THRESHOLD
    except:
        return True

def update_last_fetch_time():
    with open(CACHE_FILE, "w") as f:
        json.dump({"last_fetch": datetime.now().isoformat()}, f)

def get_team_season_stats(team_name):
    # 🔁 Replace with logic using Sportradar team_id and stats endpoint
    return {
        "batting_avg": 0.254,
        "runs_per_game": 4.8
    }

def get_team_leaders(team_name):
    # 🔁 Replace with logic using Sportradar player stats
    return {
        "home_runs": 24,
        "top_pitcher_era": 2.73
    }