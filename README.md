# IGDB Twitch Chat Bot

A Python script that queries the [IGDB API](https://api-docs.igdb.com/) for game info and displays it in Twitch chat via [Streamer.bot](https://streamer.bot). Chatters use the `!ttb` command to look up any game's release date, rating, and time-to-beat estimates.

## Example Output

```
!ttb Elden Ring
Elden Ring | Released: February 24, 2022 | Rating: 93.4/100
Speedrun: 41 hrs | Normal: 123 hrs | Completionist: 172 hrs
```

## Features

- Fuzzy search matching (doesn't require exact game titles)
- Prefers exact name matches, then falls back to oldest release date to prioritize originals over sequels/remakes
- Displays IGDB user rating and release date
- Shows speedrun, normal, and completionist time-to-beat estimates when available
- Graceful handling of missing data (no crashes on incomplete API responses)

## Setup

### 1. Get Twitch API Credentials

Register an application at [dev.twitch.tv](https://dev.twitch.tv/console) to get your Client ID and Client Secret. These same credentials work for IGDB since Twitch owns IGDB.

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Environment Variables

Copy the example env file and fill in your credentials:

```bash
cp .env.example .env
```

Then set the variables in your shell before running:

```bash
export TWITCH_CLIENT_ID=your_client_id_here
export TWITCH_CLIENT_SECRET=your_client_secret_here
```

### 4. Test from the Command Line

```bash
python igdb_bot_public.py Elden Ring
```

### 5. Connect to Streamer.bot

1. Create a new **Action** with these sub-actions:
   - **Run a Program**: Target `wsl`, Arguments `python3 "/path/to/igdb_bot_public.py" %rawInput%`, Wait maximum `15` seconds
   - **Send Message to Channel**: `%output0%`
   - **Send Message to Channel**: `%output1%`
2. Create a new **Command** (e.g. `!ttb`) with Location set to **Start**
3. Add a **Command trigger** on your action linking it to the `!ttb` command

## Tech Stack

- Python 3
- Twitch OAuth API (client credentials flow)
- IGDB API (game search + time-to-beat endpoints)
- Streamer.bot (Twitch chat integration)
