# fetch_mlb_odds.py (Finalized)
import requests
import csv
from datetime import datetime
from ev_calculator import calculate_expected_value, decimal_to_implied_prob
from dotenv import load_dotenv
from dotenv import load_dotenv
load_dotenv(dotenv_path="mlb_odds_api_keys.env")
import os
import statsapi
import json
from gpt_advisor import generate_betting_advice
from mlb_injury_scraper import scrape_mlb_injuries, group_injuries_by_team

injuries = scrape_mlb_injuries()
injuries_by_team = group_injuries_by_team(injuries)

def add_injury_info_to_games(games):
    for game in games:
        game['home']['injuries'] = injuries_by_team.get(game['home']['team'], "No injuries reported.")
        game['away']['injuries'] = injuries_by_team.get(game['away']['team'], "No injuries reported.")
    return games

# Fetch MLB odds and standings, calculate expected value, and log bets
def get_team_standings():
    try:
        data = statsapi.get("standings", {"leagueId": "103,104", "season": 2024})
        return {
            team['team']['name']: f"{team['wins']}-{team['losses']}"
            for team in data['records']
        }
    except Exception as e:
        print(f"⚠️ Failed to fetch standings: {e}")
        return {}

load_dotenv()
API_KEY = os.getenv("MLB_ODDS_API_KEY")

SPORT = "baseball_mlb"
REGION = "us"
MARKET = "h2h"
ODDS_FORMAT = "decimal"
DATE_FORMAT = "iso"

def log_ev_bet(bookmaker, matchup, team, odds, win_prob, ev):
    with open("bet_log.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            datetime.now().isoformat(),
            bookmaker,
            matchup,
            team,
            odds,
            f"{win_prob:.2%}",
            f"${ev:.2f}" if ev is not None else "N/A"
        ])

def get_live_scores():
    try:
        return {
            f"{g['away_name']} @ {g['home_name']}": f"{g.get('away_score', 0)}-{g.get('home_score', 0)}"
            for g in statsapi.schedule(sportId=1)
        }
    except Exception as e:
        print(f"⚠️ Failed to fetch scores: {e}")
        return {}

def fetch_mlb_odds(return_json=False):
    url = f"https://api.the-odds-api.com/v4/sports/{SPORT}/odds/"
    params = {
        "apiKey": API_KEY,
        "regions": REGION,
        "markets": MARKET,
        "oddsFormat": ODDS_FORMAT,
        "dateFormat": DATE_FORMAT
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"❌ API Error: {response.status_code} - {response.text}")
        return []

    games = response.json()
    standings = get_team_standings()
    scores = get_live_scores()
    structured_output = []

    for game in games:
        home = new_func(game)
        away = game["away_team"]
        matchup = f"{away} @ {home}"

        game_data = {
            "matchup": matchup,
            "home": {
                 "team": home,
                "record": standings.get(home, "N/A"),
                    },
            "away": {
                "team": away,
                "record": standings.get(away, "N/A"),
            },
            "score": scores.get(matchup, "Not started"),
            "odds": []
        }

        for site in game.get('bookmakers', []):
            for market in site.get('markets', []):
                for outcome in market.get('outcomes', []):
                    team = outcome['name']
                    odds = outcome['price']
                    implied_prob = decimal_to_implied_prob(odds)
                    win_prob = implied_prob + 0.05
                    ev = calculate_expected_value(win_prob, odds)

                    ev_data = {
                        "bookmaker": site['title'],
                        "team": team,
                        "odds": odds,
                        "win_prob": round(win_prob, 4),
                        "ev": ev,
                        "is_positive_ev": ev > 0
                    }

                    if ev > 0:
                        log_ev_bet (site['title'], matchup, team, odds, win_prob, ev)

                    game_data["odds"].append(ev_data)

        structured_output.append(game_data)

    if return_json:
        return structured_output

    with open("mlb_betting_data.json", "w") as f:
        json.dump(structured_output, f, indent=4)

    return games, standings, scores

def new_func(game):
    home = game["home_team"]
    return home

if __name__ == "__main__":
    data = fetch_mlb_odds(return_json=True)

    if data:
        print("\n🤖 GPT Advice:\n")
        advice = generate_betting_advice(data)
        print(advice)
    else:
        print("⚠️ No games returned, skipping GPT advice.")
