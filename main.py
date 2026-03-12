from pyrogram import Client, filters
import yt_dlp
import os
import asyncio

# التوكن الخاص بك
API_TOKEN = "8737851269:AAGGQsMJLDAqieEmICVcYe6v-i_hXx0wYwo"

app = Client("music_bot", bot_token=API_TOKEN, api_id=2040, api_hash="b18441a1ff607e106")

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("أهلاً بك مارك! أرسل لي رابط يوتيوب وسأقوم بتحويله إلى صوت.")

@app.on_message(filters.text & ~filters.command("start"))
async def play_music(client, message):
    url = message.text
    if "youtube.com" not in url and "youtu.be" not in url:
        return
    msg = await message.reply_text("جاري التجهيز... ⏳")
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3')
        await message.reply_audio(audio=file_path)
        await msg.delete()
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        await msg.edit(f"حدث خطأ: {e}")

async def main():
    async with app:
        print("البوت بدأ العمل بنجاح!")
        from pyrogram import idle
        await idle()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
