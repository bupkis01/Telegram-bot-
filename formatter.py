import json      
    
# Load emoji icons for leagues        
with open("leagues.json", encoding="utf-8") as f:        
    LEAGUES = json.load(f)        
    
# Load team emoji icons        
with open("teams.json", encoding="utf-8") as f:        
    TEAMS = json.load(f)        
    
# Load grouped league aliases and flatten        
with open("league_aliases_grouped.json", encoding="utf-8") as f:        
    grouped_aliases = json.load(f)        
    
LEAGUE_ALIASES = {}        
for group in grouped_aliases.values():        
    LEAGUE_ALIASES.update(group)        
    
# Load league priority      
with open("league_priority.json", encoding="utf-8") as f:        
    league_priority = json.load(f)      
    
# Function to convert score into emoji    
def score_to_emoji(score):
    score_map = {
        0: '0️⃣', 1: '1️⃣', 2: '2️⃣', 3: '3️⃣', 4: '4️⃣', 5: '5️⃣',
        6: '6️⃣', 7: '7️⃣', 8: '8️⃣', 9: '9️⃣', 10: '🔟'
    }
    return score_map.get(score, str(score))    
    
# Format today's fixture    
def format_fixtures(matches):        
    if not matches:        
        return "⚠️ No matches scheduled for today."        
    
    # Sort by league priority        
    matches.sort(key=lambda x: league_priority.index(        
        LEAGUE_ALIASES.get(x.get("league", ""), x.get("league", ""))        
    ) if LEAGUE_ALIASES.get(x.get("league", ""), x.get("league", "")) in league_priority else len(league_priority))        
    
    message = "📌 𝗧𝗼𝗱𝗮𝘆'𝘀 𝗠𝗮𝘁𝗰𝗵𝗲𝘀\n\n"        
    last_league = None        
    
    for match in matches:        
        raw_league = match.get("league", "Unknown League")        
        league_name = LEAGUE_ALIASES.get(raw_league, raw_league)        
        league_icon = LEAGUES.get(league_name, "🔰")        
    
        if league_name != last_league:        
            message += f"\n{league_icon} *{league_name}*\n"        
    
        home_team = TEAMS.get(match.get("home", ""), {}).get("home", "⚪")        
        away_team = TEAMS.get(match.get("away", ""), {}).get("away", "⚫")        
        match_text = f"""        
{home_team} *{match.get('home', '')}* 🆚 *{match.get('away', '')}* {away_team}              
🕡 {match.get('local_time', '')} Local | {match.get('utc_time', '')} UTC 🌐            
"""        
        message += match_text        
        last_league = league_name        
    
    return message.strip()        
    
# Format match results with emoji scores    
def format_match_result(match):        
    raw_league = match.get("league", "Unknown League")        
    league_name = LEAGUE_ALIASES.get(raw_league, raw_league)        
    league_icon = LEAGUES.get(league_name, "🔰")        
    
    home_team = TEAMS.get(match.get("home", ""), {}).get("home", "⚪")        
    away_team = TEAMS.get(match.get("away", ""), {}).get("away", "⚫")        
    
    # Convert scores to emojis    
    home_score = score_to_emoji(match.get('home_score', 0))        
    away_score = score_to_emoji(match.get('away_score', 0))    
    
    # League hashtag (formatted to lowercase and without spaces)    
    league_hashtag = f"#{league_name.replace(' ', '').lower()}"    
    
    return f"""        
📌 𝗠𝗮𝘁𝗰𝗵 𝗘𝗻𝗱𝗲𝗱 | 𝗙𝗧            
    
{league_icon} *{league_name}*             
{home_team} *{match.get('home', '')}* {home_score} - {away_score} *{match.get('away', '')}* {away_team}      
    
                                               {league_hashtag}      
""".strip()
