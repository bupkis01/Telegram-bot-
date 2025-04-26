# get_fixtures.py

import requests
from datetime import datetime, timedelta
import pytz

ESPN_FIXTURES_URL = "https://site.api.espn.com/apis/site/v2/sports/soccer/{}/scoreboard"
IST = pytz.timezone("Asia/Kolkata")

def is_within_custom_window(match_time_utc):
    now_ist = datetime.now(IST)
    start_window = now_ist.replace(hour=9, minute=15, second=0, microsecond=0)
    if now_ist.hour < 1:
        start_window -= timedelta(days=1)
    end_window = start_window + timedelta(days=1) - timedelta(minutes=1)
    match_time_ist = match_time_utc.astimezone(IST)
    return start_window <= match_time_ist <= end_window

def convert_match_time(iso_time):
    try:
        utc_time = datetime.fromisoformat(iso_time[:-1]).replace(tzinfo=pytz.utc)
        local_time = utc_time.astimezone(IST)
        return local_time.strftime("%H:%M"), utc_time
    except Exception as e:
        print(f"⚠️ Time conversion error: {e}")
        return "Unknown", None

def get_fixtures(league="eng.1", filter_by_window=False):
    try:
        print(f"📡 Fetching fixtures for {league}...")
        response = requests.get(ESPN_FIXTURES_URL.format(league))
        response.raise_for_status()

        data = response.json()
        events = data.get("events", [])

        fixtures = []
        for event in events:
            try:
                competition = event["competitions"][0]
                competitors = competition["competitors"]
                match_time = competition["date"]
                local_time, match_time_utc = convert_match_time(match_time)

                if filter_by_window and (not match_time_utc or not is_within_custom_window(match_time_utc)):
                    continue

                home = [t for t in competitors if t["homeAway"] == "home"][0]
                away = [t for t in competitors if t["homeAway"] == "away"][0]

                fixtures.append({
                    "match_id":      event["id"],
                    "home":          home["team"]["displayName"],
                    "away":          away["team"]["displayName"],
                    "local_time":    local_time,
                    "utc_time":      match_time_utc.strftime("%H:%M") if match_time_utc else "Unknown",
                    "status":        event["status"]["type"]["name"].upper(),
                    "league":        data.get("leagues", [{}])[0].get("name", "Unknown League"),
                    "home_score":    int(home.get("score", 0)),
                    "away_score":    int(away.get("score", 0)),
                    "utc_datetime":  match_time_utc.isoformat() if match_time_utc else ""
                })
            except KeyError as e:
                print(f"⚠️ Missing data in API response: {e}")
                continue

        # Remove duplicate matches based on match_id
        unique_fixtures = {}
        for match in fixtures:
            unique_fixtures[match["match_id"]] = match

        final_fixtures = list(unique_fixtures.values())
        print(f"✅ {len(final_fixtures)} fixtures fetched.")
        return final_fixtures

    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching fixtures: {e}")
        return []
