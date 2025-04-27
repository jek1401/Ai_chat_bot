import sqlite3
from discord.ext import commands, tasks
from tgbot.config import DB_PATH, active_sessions

class Points(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.give_points.start()

    def cog_unload(self):
        self.give_points.cancel()

    @tasks.loop(minutes=5)
    async def give_points(self):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("UPDATE users SET points = points + 1")
        conn.commit()
        conn.close()

    @commands.command()
    async def points(self, ctx):
        user = active_sessions.get(ctx.author.id)
        if not user:
            return await ctx.send("❌ Сначала войдите в аккаунт с `.login`.")

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT points FROM users WHERE name = ?", (user,))
        row = c.fetchone()
        conn.close()

        await ctx.send(f"💰 У вас {row[0]} поинтов.")


# обязательно async-setup для расширения
async def setup(bot):
    await bot.add_cog(Points(bot))
