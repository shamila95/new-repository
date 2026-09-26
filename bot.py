import os
import asyncio
import pyrogram.errors

try:
    pyrogram.errors.GroupcallForbidden
except AttributeError:
    class GroupcallForbidden(Exception):
        pass
    pyrogram.errors.GroupcallForbidden = GroupcallForbidden

from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream
import yt_dlp


API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
BOT_TOKEN = os.environ["BOT_TOKEN"]

app = Client(
    "music_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

call_py = PyTgCalls(app)


async def get_audio(query):
    ydl_opts = {
        "format": "bestaudio/best",
        "quiet": True,
        "no_warnings": True,
        "default_search": "ytsearch1",
        "noplaylist": True,
        "outtmpl": "/tmp/music_%(id)s.%(ext)s",
    }

    loop = asyncio.get_running_loop()

    def download():
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=True)

            if "entries" in info:
                info = info["entries"][0]

            return ydl.prepare_filename(info)

    return await loop.run_in_executor(None, download)


@app.on_message(filters.command("start"))
async def start_handler(client, message):
    await message.reply_text(
        "🎵 Music Bot is online!\n\n"
        "▶️ /play song name\n"
        "⏹ /stop"
    )


@app.on_message(filters.command("play"))
async def play_handler(client, message):

    if len(message.command) < 2:
        await message.reply_text(
            "🎵 භාවිතා කරන්න:\n/play song name"
        )
        return

    query = " ".join(message.command[1:])

    status = await message.reply_text(
        f"🔎 සින්දුව හොයනවා...\n🎵 {query}"
    )

    try:
        audio_file = await get_audio(query)

        await call_py.play(
            message.chat.id,
            MediaStream(audio_file)
        )

        await status.edit_text(
            f"▶️ දැන් play වෙනවා:\n🎵 {query}"
        )

    except Exception as e:
        await status.edit_text(
            f"❌ Play කරන්න බැරි වුණා.\n\n"
            f"{type(e).__name__}: {e}"
        )


@app.on_message(filters.command("stop"))
async def stop_handler(client, message):

    try:
        await call_py.leave_group_call(message.chat.id)
        await message.reply_text("⏹ Music stopped.")

    except Exception as e:
        await message.reply_text(
            f"❌ Stop කරන්න බැරි වුණා.\n\n"
            f"{type(e).__name__}: {e}"
        )


print("🎵 Music Bot Started...")

call_py.start()
app.run()
