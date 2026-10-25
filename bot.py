import asyncio, json, os, random
from pathlib import Path
from urllib.parse import quote_plus
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
SUBS_FILE = Path("subscribers.json")
INTERVAL = 30 * 60

SONGS = [
("我不难过","孙燕姿"),("我怀念的","孙燕姿"),("七里香","周杰伦"),
("晴天","周杰伦"),("搁浅","周杰伦"),("玻璃","Gareth.T"),
("那天下雨了","周杰伦"),("唯一","邓紫棋"),("告白气球","周杰伦"),
("花海","周杰伦"),("明明就","周杰伦"),("情歌","梁静茹"),
("爱情转移","陈奕迅"),("特别的人","方大同"),("恋人","李荣浩"),
("甲乙丙丁 Strangers","李佳薇"),("自由的你","邓紫棋"),("稻香","周杰伦"),
("夜曲","周杰伦"),("等你下课","周杰伦 & 杨瑞代")
]
subscribers = set()

def load_subscribers():
    global subscribers
    try: subscribers = {int(x) for x in json.loads(SUBS_FILE.read_text(encoding="utf-8"))}
    except (OSError, ValueError, TypeError): subscribers = set()

def save_subscribers():
    SUBS_FILE.write_text(json.dumps(sorted(subscribers)), encoding="utf-8")

def make_song():
    title, artist = random.choice(SONGS)
    q = quote_plus(f"{artist} {title} official audio")
    spotify_q = quote_plus(f"{artist} {title}")
    text = (f"🎵 <b>TOSHIRO 中文音乐</b>\n\n"
            f"🎧 <b>{title}</b>\n👤 歌手：{artist}\n\n"
            "选择平台收听：")
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("▶ YouTube", url=f"https://www.youtube.com/results?search_query={q}"),
        InlineKeyboardButton("🎧 Spotify", url=f"https://open.spotify.com/search/{spotify_q}")
    ]])
    return text, keyboard

async def send_song(chat_id, bot):
    text, keyboard = make_song()
    await bot.send_message(chat_id, text, parse_mode="HTML", reply_markup=keyboard, disable_web_page_preview=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        "🎶 <b>TOSHIRO Chinese Music Bot</b>\n\n"
        "/subscribe — song every 30 minutes\n/unsubscribe — stop songs\n"
        "/song — get a song now\n/status — subscription status\n\n"
        "Add me to a group, then use /subscribe in that group.",
        parse_mode="HTML")

async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    if not chat: return
    if chat.id in subscribers:
        await update.effective_message.reply_text("Already subscribed to songs in this chat.")
        return
    subscribers.add(chat.id); save_subscribers()
    await update.effective_message.reply_text("✅ Subscribed! I’ll send a Chinese song every 30 minutes.")
    await send_song(chat.id, context.bot)

async def unsubscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    if not chat: return
    subscribers.discard(chat.id); save_subscribers()
    await update.effective_message.reply_text("🛑 Automatic song messages stopped for this chat.")

async def song(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat: await send_song(update.effective_chat.id, context.bot)

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    if chat:
        msg = "🟢 This chat receives a song every 30 minutes." if chat.id in subscribers else "⚪ Not subscribed. Send /subscribe."
        await update.effective_message.reply_text(msg)

async def music_loop(app: Application):
    while True:
        await asyncio.sleep(INTERVAL)
        for chat_id in list(subscribers):
            try: await send_song(chat_id, app.bot)
            except Exception as exc: print(f"Send failed for {chat_id}: {exc}")

async def post_init(app: Application):
    load_subscribers()
    app.create_task(music_loop(app))

def main():
    if not TOKEN:
        raise SystemExit("Set TELEGRAM_BOT_TOKEN in your host's environment variables.")
    load_subscribers()
    app = Application.builder().token(TOKEN).post_init(post_init).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("subscribe", subscribe))
    app.add_handler(CommandHandler("unsubscribe", unsubscribe))
    app.add_handler(CommandHandler("song", song))
    app.add_handler(CommandHandler("status", status))
    print("TOSHIRO Chinese Music Bot running.")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__": main()
