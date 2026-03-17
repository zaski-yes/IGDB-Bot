import requests
import sys
import os

from datetime import datetime

# Step 1: Access token from Twitch API

CLIENT_ID = os.environ.get("TWITCH_CLIENT_ID")
CLIENT_SECRET = os.environ.get("TWITCH_CLIENT_SECRET")

if not CLIENT_ID or not CLIENT_SECRET:
    print("Error: Missing TWITCH_CLIENT_ID or TWITCH_CLIENT_SECRET environment variables.")
    print("Set these before running the script.")
    sys.exit(1)

auth_url = "https://id.twitch.tv/oauth2/token"

auth_params = {
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "grant_type": "client_credentials"
}

auth_response = requests.post(auth_url, params=auth_params)
access_token = auth_response.json()["access_token"]

# Step 2: Search IGDB for a game

igdb_url = "https://api.igdb.com/v4/games"

headers = {
    "Client-ID": CLIENT_ID,
    "Authorization": f"Bearer {access_token}"
}

game_name = " ".join(sys.argv[1:])

if not game_name:
    print("Usage: python igdb_bot_public.py <game name>")
    print("Example: python igdb_bot_public.py Elden Ring")
    sys.exit(1)

body = f'search "{game_name}"; fields name, rating, first_release_date, summary; limit 10;'

game_response = requests.post(igdb_url, headers=headers, data=body)
game_data = game_response.json()

# Filter to games with release dates and sort oldest first
game_data = [g for g in game_data if g.get("first_release_date")]
game_data.sort(key=lambda g: g["first_release_date"])

if game_data:

    # Prefer exact name match, otherwise fall back to oldest release
    exact_match = [g for g in game_data if g.get("name", "").lower() == game_name.lower()]

    if exact_match:
        game = exact_match[0]
    else:
        game = game_data[0]

    timestamp = game.get("first_release_date")
    rating = game.get("rating")
    game_id = game["id"]
    matched_name = game.get("name", game_name)

    readable_date = datetime.fromtimestamp(timestamp).strftime("%B %d, %Y") if timestamp else "Unknown"
    rating_str = f"{round(rating, 1)}/100" if rating else "No rating"

    print(f"{matched_name} | Released: {readable_date} | Rating: {rating_str}")

    # Step 3: Get time-to-beat data

    ttb_url = "https://api.igdb.com/v4/game_time_to_beats"
    ttb_body = f"fields *; where game_id = {game_id}; limit 1;"
    ttb_response = requests.post(ttb_url, headers=headers, data=ttb_body)
    ttb_data = ttb_response.json()

    if ttb_data:
        hastily = ttb_data[0].get("hastily")
        normally = ttb_data[0].get("normally")
        completely = ttb_data[0].get("completely")

        parts = []
        if hastily:
            parts.append(f"Speedrun: {round(hastily / 3600)} hrs")
        if normally:
            parts.append(f"Normal: {round(normally / 3600)} hrs")
        if completely:
            parts.append(f"Completionist: {round(completely / 3600)} hrs")

        if parts:
            print(" | ".join(parts))
        else:
            print("No 'time to beat' data available.")
    else:
        print("No 'time to beat' data available.")

else:
    print(f"Game not found: {game_name}")
    print("Try a different spelling or title.")
