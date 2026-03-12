import os
import asyncio
import subprocess
from pyrogram import Client, filters
from aiohttp import web
import yt_dlp

# إعدادات البوت
API_TOKEN = "8737851269:AAGGQsMJLDAqieEmICVcYe6v-i_hXx0wYwo"
app = Client("music_bot", bot_token=API_TOKEN, api_id=2040, api_hash="b18441a1ff607e106")

async def handle(request):
    return web.Response(text="Bot is running!")

async def start_server():
    server = web.Application()
    server.router.add_get("/", handle)
    runner = web.AppRunner(server)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 10000)
    await site.start()

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("أهلاً بك! أنا أعمل الآن. أرسل رابط يوتيوب وسأحاول تحميله لك. 🎵")

@app.on_message(filters.text & ~filters.command("start"))
async def play_music(client, message):
    url = message.text
    if "youtube" not in url and "youtu.be" not in url:
        return
    
    msg = await message.reply_text("جاري التحميل... انتظر قليلاً ⏳")
    
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': '%(title)s.%(ext)s',
            'noplaylist': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
        await message.reply_audio(audio=filename, title=info.get('title'))
        await msg.delete()
        os.remove(filename)
    except Exception as e:
        await msg.edit(f"فشل التحميل. تأكد من الرابط.\nالخطأ: {str(e)[:50]}")

async def main():
    await start_server()
    async with app:
        await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
