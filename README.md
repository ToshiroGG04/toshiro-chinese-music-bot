# TOSHIRO Chinese Music Bot

Sends a Chinese song recommendation immediately when a chat subscribes, then every 30 minutes while the bot stays online. It shares YouTube/Spotify search links instead of re-uploading copyrighted songs.

## Commands
- `/start` — help
- `/subscribe` — subscribe this chat and send the first song
- `/unsubscribe` — stop automatic songs
- `/song` — send one song now
- `/status` — check subscription

## Run locally
1. Create a bot with Telegram **@BotFather** using `/newbot`.
2. Set environment variable `TELEGRAM_BOT_TOKEN` to the token (keep it private).
3. Install Python 3.10+ and run:
   `pip install -r requirements.txt`
4. Start with: `python bot.py`
5. In Telegram send `/start`, then `/subscribe`. To post in a group, add the bot and run `/subscribe` in that group.

## Hosting
Deploy on a host that supports a persistent Python process. Set `TELEGRAM_BOT_TOKEN` as an environment variable and use `python bot.py` as the start command. Free hosts may sleep or stop bots. `subscribers.json` should be kept on persistent storage.

The starter song list is based on recent Chinese chart listings and is not a live chart feed. Edit `SONGS` in `bot.py` to customize it.
