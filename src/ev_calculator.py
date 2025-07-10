# ev_calculator.py

from datetime import datetime
import csv

def decimal_to_implied_prob(decimal_odds):
    """Converts decimal odds to implied win probability."""
    return 1 / decimal_odds

def calculate_expected_value(win_prob, decimal_odds, stake=20):
    """Calculates expected value of a bet."""
    payout = (decimal_odds - 1) * stake
    ev = (win_prob * payout) - ((1 - win_prob) * stake)
    return round(ev, 2)

def log_ev_bet(bookmaker, matchup, team, odds, win_prob, ev, gpt_commentary=None, confidence=None, stake_pct=None):
    """Logs the details of a positive EV bet."""
    with open("bet_log.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            datetime.now().isoformat(),
            bookmaker,
            matchup,
            team,
            odds,
            f"{win_prob:.2%}",
            f"${ev:.2f}",
            confidence or "",
            stake_pct or "",
            gpt_commentary or ""
        ])
