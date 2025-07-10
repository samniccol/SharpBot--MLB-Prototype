# mlb_run_assistant.py
import json
from fetch_mlb_odds import fetch_mlb_odds
from mlb_stats import get_team_season_stats, get_team_leaders
from gpt_advisor import generate_betting_advice
from mlb_injury_scraper import scrape_mlb_injuries
import time
import os
import csv
import subprocess
from watchlist_monitor import monitor_watchlist
# Config
STATS_CACHE_FILE = "cached_stats.json"
WATCHLIST_FILE = "watchlist.json"

def launch_gui():
    subprocess.run(["python", "watchlist_gui.py"])

def main():
    while True:
        print("\n=== 🧠 Betting Assistant ===")
        print("1. Start Monitor Loop")
        print("2. Manage Watchlist (GUI)")
def main_menu():
    while True:
        print("\n=== 🧠 Betting Assistant ===")
        print("1. Start Monitor Loop")
        print("2. Manage Watchlist (GUI)")
        print("3. Exit")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            while True:
                monitor_watchlist()
                time.sleep(1800)
        elif choice == "2":
            launch_gui()
        elif choice == "3":
            print("👋 Exiting.")
            break
        else:
            print("❌ Invalid choice. Try again.")

def write_to_csv(data, filename="betting_data.csv"):
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["bookmaker", "team", "odds", "win_prob", "ev", "is_positive_ev"])
        for game in data:
            for bet in game.get("odds", []):
                writer.writerow([
                    bet["bookmaker"],
                    bet["team"],
                    bet["odds"],
                    bet["win_prob"],
                    bet["ev"],
                    bet["is_positive_ev"]
                ])

def enrich_game_data_with_stats(game_data):
    """Injects season stats and leaders into each game dictionary."""
    for game in game_data:
        home = game["home"]
        away = game["away"]
        game["home"]["stats"] = get_team_season_stats(home)
        game["home"]["leaders"] = get_team_leaders(home)
        game["away"]["stats"] = get_team_season_stats(away)
        game["away"]["leaders"] = get_team_leaders(away)
    game["team1_injuries"] = scrape_mlb_injuries(home)
    game["team2_injuries"] = scrape_mlb_injuries(away)
    game["odds"] = {
        "spread": -5.5,
        "moneyline_team1": +160,
        "moneyline_team2": -190,
        "over_under": 162.5
    }
    game["news_headlines"] = [...] # Placeholder for news headlines
    game["betting_recommendation"] = None
def create_game_data(game):
    game_data = {
        "team1": game["home"]["team"],
        "team2": game["away"]["team"],
        "game_time": game["game_time"],
        "team1_stats": game["home"].get("stats", {}),
        "team2_stats": game["away"].get("stats", {}),
        "team1_injuries": [],
        "team2_injuries": [],
        "odds": {
            "spread": -5.5,
            "moneyline_team1": +160,
            "moneyline_team2": -190,
            "over_under": 162.5
        },
        "news_headlines": [],
        "betting_recommendation": None
    }
    return game_data


def save_cached_stats(game_data):
    with open(STATS_CACHE_FILE, "w") as f:
        json.dump(game_data, f)
        print("📈 Fetching MLB odds...")
        game_data = fetch_mlb_odds()
        print("📊 Raw game_data:", game_data)

def load_cached_stats(stats_cache_file="cached_stats.json"):
    if not os.path.exists(stats_cache_file):
        print("❌ No cached stats found.")
        return None
    with open(stats_cache_file, "r") as f:
        return json.load(f)

    if cached:
        print("✅ Using cached stats from the last 12 hours.")
        enriched_games = cached
    save_cached_stats(enriched_games)

    print("💡 Generating advice from GPT...")
    for game in enriched_games:
        advice = generate_betting_advice(game)
        home_team = game['home']['team']
        away_team = game['away']['team']
        print(f"\n🧠 Game: {home_team} vs {away_team}")
        print(f"GPT Insight: {advice}")

    for game in enriched_games:
        for bet in game.get("odds", []):
            bet["is_positive_ev"] = bet["ev"] > 0

def main():
    print("📈 Fetching MLB odds...")
    game_data = fetch_mlb_odds()
    print("📊 Raw game_data:", game_data)

    if not game_data:
        print("❌ No games found or failed to fetch odds.")
        return

    cached = load_cached_stats()
    if cached:
        print("✅ Using cached stats from the last 12 hours.")
        enriched_games = cached
    else:
        enrich_game_data_with_stats(game_data)
        enriched_games = game_data
        save_cached_stats(enriched_games)

    print("💡 Generating advice from GPT...")
    for game in enriched_games:
        advice = generate_betting_advice(game)
        home_team = game['home']['team']
        away_team = game['away']['team']
        print(f"\n🧠 Game: {home_team} vs {away_team}")
        print(f"GPT Insight: {advice}")

    write_to_csv(enriched_games)
    print("💾 Betting data saved to betting_data.csv")
