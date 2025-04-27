import discord
from discord.ext import commands
from discord.ui import Button, View
import sqlite3
from tgbot.config import DB_PATH, active_sessions, personalities_list, voices

class Personalization(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def choose(self, ctx):
        view = View()
        for p in personalities_list[:5]:
            view.add_item(Button(label=p, style=discord.ButtonStyle.primary, custom_id=f"personality_{p}"))
        await ctx.send("👤 Выберите личность:", view=view)

        view_voice = View()
        for v in voices[:5]:
            view_voice.add_item(Button(label=v, style=discord.ButtonStyle.secondary, custom_id=f"voice_{v}"))
        await ctx.send("🎤 Выберите голос:", view=view_voice)

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        user = active_sessions.get(interaction.user.id)
        if not user:
            return await interaction.response.send_message("❌ Пожалуйста, войдите с `.login`", ephemeral=True)

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        if interaction.data["custom_id"].startswith("personality_"):
            personality = interaction.data["custom_id"].split("_", 1)[1]
            c.execute("UPDATE users SET personality = ? WHERE name = ?", (personality, user))
            await interaction.response.send_message(f"✅ Личность установлена: {personality}", ephemeral=True)

        elif interaction.data["custom_id"].startswith("voice_"):
            voice = interaction.data["custom_id"].split("_", 1)[1]
            c.execute("UPDATE users SET voice = ? WHERE name = ?", (voice, user))
            await interaction.response.send_message(f"✅ Голос установлен: {voice}", ephemeral=True)

        conn.commit()
        conn.close()

# 👇 это обязательный async setup для discord.py 2.x
async def setup(bot):
    await bot.add_cog(Personalization(bot))


