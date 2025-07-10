new_script = """
# gpt_advisor.py
from dotenv import load_dotenv
...
def generate_betting_advice(...):
    ...
"""
print("✅ gpt_advisor.py loaded successfully")

from dotenv import load_dotenv
import openai
import os

# Load API key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_betting_advice(game_data, season_stats=None, player_stats=None, live_scores=None):
    if not game_data:
        return "⚠️ No game data provided."

    formatted_games = ""

    for game in game_data:
        matchup = game.get("matchup", "Unknown")
        home = game.get("home", {}).get("team", "Unknown")
        away = game.get("away", {}).get("team", "Unknown")
        score = game.get("score", "N/A")

        injuries_home = game.get("home", {}).get("injuries", "Not available")
        injuries_away = game.get("away", {}).get("injuries", "Not available")
        news_home = game.get("home", {}).get("news", "No updates.")
        news_away = game.get("away", {}).get("news", "No updates.")

        formatted_games += f"\n⚾ {matchup} | Score: {score}\n"
        formatted_games += f"🔍 {home} Injuries: {injuries_home}\n"
        formatted_games += f"📰 {home} News: {news_home}\n"
        formatted_games += f"🔍 {away} Injuries: {injuries_away}\n"
        formatted_games += f"📰 {away} News: {news_away}\n"

        for odd in game.get("odds", []):
            formatted_games += (
                f"  {odd['bookmaker']} → {odd['team']} @ {odd['odds']} | "
                f"WinProb: {odd['win_prob']:.2%} | EV: ${odd['ev']:.2f}\n"
            )

    formatted_stats = ""
    if any([season_stats, player_stats, live_scores]):
        formatted_stats += f"\n📊 Season Stats:\n{season_stats}\n"
        formatted_stats += f"\n🏃 Player Stats:\n{player_stats}\n"
        formatted_stats += f"\n🔴 Live Game Info:\n{live_scores}\n"

    prompt = f"""
You are a professional sports betting analyst.

You will be given game matchups, injuries, news, odds, season data, and player performance info.
Identify bets with positive expected value (EV) and explain your reasoning.

For EACH bet recommendation, return:

1. 🎯 Team and odds  
2. 💬 Reason why the bet is valuable  
3. 🔢 Confidence score from 1 to 10  
4. 💰 Recommended stake size (1%–5% of bankroll)  

Format:

BET:
Team: [team name]  
Odds: [decimal odds]  
Confidence: [1–10]  
Stake Recommendation: [1%–5%]  
Reasoning: [short explanation]

---

Today’s games and data:
{formatted_games}

{formatted_stats}
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a professional sports betting analyst."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1600
        )

        message = response['choices'][0].get('message', {}).get('content')
        return message or "⚠️ GPT response was empty or malformed."

    except Exception as e:
        return f"❌ GPT error: {str(e)}"
