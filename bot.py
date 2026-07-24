import discord
from discord.ext import commands
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

# --- БЛОК ОБМАНА ХОСТИНГА (Живет на бесплатном тарифе) ---
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

def run_web_server():
    server = HTTPServer(('0.0.0.0', 10000), HealthCheckHandler)
    server.serve_forever()

# Запускаем веб-сервер в отдельном потоке
threading.Thread(target=run_web_server, daemon=True).start()
# --------------------------------------------------------

# Включаем нужные доступы (интенты)
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Создаем бота
bot = commands.Bot(command_prefix="!", intents=intents)

# ID канала, где бот будет красиво оформлять сделки.
TRADE_CHANNEL_ID = 1502292137889501235  # ЗАМЕНИТЕ НА ВАШ ID КАНАЛА

@bot.event
async def on_ready():
    print(f"Бот {bot.user.name} успешно запущен бесплатно!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.channel.id == TRADE_CHANNEL_ID:
        image_url = None
        if message.attachments:
            for attachment in message.attachments:
                if attachment.content_type and attachment.content_type.startswith("image/"):
                    image_url = attachment.url
                    break

        if image_url or message.content:
            embed = discord.Embed(
                title="📊 Новая сделка в комьюнити!",
                description=message.content if message.content else "Без описания",
                color=0x00ff00
            )
            embed.set_author(name=message.author.display_name, icon_url=message.author.display_avatar.url)
            
            if image_url:
                embed.set_image(url=image_url)
                
            embed.set_footer(text="Удачных торгов! Соблюдайте риск-менеджмент.")

            try:
                await message.delete()
            except discord.Forbidden:
                print("Дайте боту роль Администратора!")

            await message.channel.send(embed=embed)

    await bot.process_commands(message)

# ЗАМЕНИТЕ НА ВАШ СЕКРЕТНЫЙ ТОКЕН
bot.run("JbKxcj_zQJHHSH3_PPXfSH1UfZSaA8vi")
