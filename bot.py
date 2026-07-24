import discord
from discord.ext import commands

# Включаем нужные доступы (интенты)
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Создаем бота
bot = commands.Bot(command_prefix="!", intents=intents)

# ID канала, где бот будет красиво оформлять сделки. 
# Замените 0 на реальный ID вашего канала в Discord (например: 123456789012345678)
TRADE_CHANNEL_ID = 1502292137889501235  

@bot.event
async def on_ready():
    print(f"Бот {bot.user.name} успешно запущен и готов к работе!")

@bot.event
async def on_message(message):
    # Игнорируем сообщения от самого бота
    if message.author == bot.user:
        return

    # Проверяем, что сообщение написано именно в канале для сделок
    if message.channel.id == TRADE_CHANNEL_ID:
        
        # Проверяем, прикрепил ли пользователь скриншот (картинку)
        image_url = None
        if message.attachments:
            for attachment in message.attachments:
                if attachment.content_type and attachment.content_type.startswith("image/"):
                    image_url = attachment.url
                    break

        # Если в сообщении есть картинка или текст, оформляем красивую карточку
        if image_url or message.content:
            # 1. Создаем красивую Embed-карточку
            embed = discord.Embed(
                title="📊 Новая сделка в комьюнити!",
                description=message.content if message.content else "Без описания",
                color=0x00ff00  # Зеленый цвет боковой панели карточки
            )
            
            # Добавляем автора сделки с его аватаркой
            embed.set_author(name=message.author.display_name, icon_url=message.author.display_avatar.url)
            
            # Добавляем скриншот графика, если он есть
            if image_url:
                embed.set_image(url=image_url)
                
            # Подпись внизу карточки
            embed.set_footer(text="Удачных торгов! Соблюдайте риск-менеджмент.")

            # 2. Удаляем исходное хаотичное сообщение пользователя
            try:
                await message.delete()
            except discord.Forbidden:
                print("У бота нет прав на удаление сообщений! Дайте ему роль Администратора на сервере.")

            # 3. Отправляем красивую карточку в этот же канал
            await message.channel.send(embed=embed)

    # Позволяет боту обрабатывать другие команды, если они будут добавлены позже
    await bot.process_commands(message)

# Сюда вместо ВАШ_СЕКРЕТНЫЙ_ТОКЕН_БОТА вставьте токен из Developer Portal
# Кавычки вокруг токена обязательно должны остаться!
bot.run("MTUzMDM0MTI0MDg1ODQ3NjYzNA.Gq0HQe.OnIXbu7KydkWpP4JZw4OStp1d_BlW5JeTuVqCo")
