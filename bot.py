import os
import asyncio

from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream
import yt_dlp


API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")


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
        "outtmpl": "%(id)s.%(ext)s",
    }

    loop = asyncio.get_running_loop()

    def download():
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=True)

            if "entries" in info:
                info = info["entries"][0]

            return ydl.prepare_filename(info)

    return await loop.run_in_executor(None, download)


@app.on_message(filters.command("play"))
async def play_music(client, message):

    if len(message.command) < 2:
        await message.reply_text(
            "🎵 `/play song name` භාවිතා කරන්න."
        )
        return

    query = " ".join(message.command[1:])

    await message.reply_text(
        f"🔎 සින්දුව හොයනවා...\n\n🎵 {query}"
    )

    try:
        audio_file = await get_audio(query)

        await call_py.join_group_call(
            message.chat.id,
            MediaStream(audio_file)
        )

        await message.reply_text(
            f"▶️ දැන් play වෙනවා:\n🎵 {query}"
        )

    except Exception as e:
        await message.reply_text(
            f"❌ Play කරන්න බැරි වුණා.\n\n{e}"
        )


@app.on_message(filters.command("stop"))
async def stop_music(client, message):

    try:
        await call_py.leave_group_call(message.chat.id)
        await message.reply_text("⏹ Music stopped.")

    except Exception:
        await message.reply_text(
            "❌ Voice chat එකේ music play වෙන්නේ නැහැ."
        )


print("🎵 Music Bot Started...")

call_py.start()
app.run()
