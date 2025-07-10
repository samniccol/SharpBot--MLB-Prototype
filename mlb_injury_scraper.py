import requests
from bs4 import BeautifulSoup
import json
import random

# URL to scrape
MLB_URL = "https://www.rotowire.com/baseball/injury-report.php"

# Rotate User-Agents
HEADERS_LIST = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
]
def get_random_headers():
    return random.choice(HEADERS_LIST)

def scrape_mlb_injuries():
    try:
        url = MLB_URL
        headers = get_random_headers()
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        # TEMP debugging: print first part of HTML
        print(soup.prettify()[:2000])

        table = soup.find("table", class_="tablesorter")
        if not table:
            print("❌ Injury table not found.")
            return []

        rows = table.find_all("tr")[1:]  # skip header
        injuries = []

        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 5:
                continue
            player = cols[0].get_text(strip=True)
            team = cols[1].get_text(strip=True)
            position = cols[2].get_text(strip=True)
            injury = cols[3].get_text(strip=True)
            status = cols[4].get_text(strip=True)

            injuries.append({
                "player": player,
                "team": team,
                "position": position,
                "injury": injury,
                "status": status
            })

        return injuries

    except Exception as e:
        print(f"⚠️ Error: {e}")
        return []

def group_injuries_by_team(injuries):
    grouped = {}
    for injury in injuries:
        team = injury["team"]
        if team not in grouped:
            grouped[team] = []
        grouped[team].append(
            f"{injury['player']} ({injury['position']}) - {injury['injury']} - {injury['status']}"
        )
    return grouped

def save_injuries_to_cache(data, filename="cached_injuries.json"):
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
        print(f"✅ Injuries cached to {filename}")
    except Exception as e:
        print(f"❌ Failed to save injury data: {e}")

# Run directly
if __name__ == "__main__":
    print("🔍 Scraping MLB injuries from Rotowire...")
    injuries = scrape_mlb_injuries()
    grouped = group_injuries_by_team(injuries)
    save_injuries_to_cache(grouped)

    # Preview
    for team in list(grouped.keys())[:3]:
        print(f"\n🔵 {team}:\n" + "\n".join(grouped[team]))
