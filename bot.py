import os
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream

API_ID = int(os.getenv("31190682"))
API_HASH = os.getenv( 69db130b89676fa8ed782575a8970bf2)
BOT_TOKEN = os.getenv(8982542199:AAElH4L-hEH875Vjj5pVqr1HudC0GOM5QnM)

app = Client(
    "music_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

call = PyTgCalls(app)


@app.on_message(filters.command(python bot.py))
async def start(client, message):
    await message.reply_text(
        "🎵 Music Bot is online!\n\n"
        "Use /play <YouTube URL> to play music."
    )


@app.on_message(filters.command("play"))
async def play(client, message):
    if len(message.command) < 2:
        await message.reply_text("❌ Use: /play <YouTube URL>")
        return

    url = message.command[1]

    try:
        await call.play(
            message.chat.id,
            MediaStream(url)
        )
        await message.reply_text("▶️ Playing music!")
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")


@app.on_message(filters.command("stop"))
async def stop(client, message):
    try:
        await call.leave_call(message.chat.id)
        await message.reply_text("⏹️ Stopped.")
    except Exception:
        await message.reply_text("❌ Nothing is playing.")


app.run()
