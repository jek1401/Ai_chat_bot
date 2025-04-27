# bots/commands/help.py
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help_command(self, ctx):
        help_text = """
📜 **Команды бота:**

🔐 **Регистрация и вход**
`.register <имя> <пароль>` — зарегистрироваться  
`.login <имя> <пароль>` — войти в аккаунт  

🎭 **Персонализация**
`.choose` — выбрать личность и голос  
`.personalities` — список личностей  
`.voices` — список голосов  

❓ **ИИ**
`.ask <сообщение>` — текстовая генерация  
`.say <сообщение>` — голосовая генерация (стоит 5 поинтов)

💰 **Поинты**
`.points` — баланс поинтов (начисляются каждые 5 мин)

❓ **Помощь**
`.help` — это сообщение
"""
        await ctx.send(help_text)

# ⚠️ Обязательный async setup(bot) с await
async def setup(bot):
    await bot.add_cog(Help(bot))
