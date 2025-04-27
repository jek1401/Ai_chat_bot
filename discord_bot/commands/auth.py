import discord
from discord.ext import commands
import asyncio
import sqlite3

from tgbot.config import DB_PATH, active_sessions
from proekt.data import database  # модуль БД

class StartView(discord.ui.View):
    def init(self, bot):
        super().init(timeout=60)
        self.bot = bot

    @discord.ui.button(label="🔑 Вход", style=discord.ButtonStyle.primary)
    async def login_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        await self.create_thread_for_user(interaction, "login")

    @discord.ui.button(label="📝 Регистрация", style=discord.ButtonStyle.success)
    async def register_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        await self.create_thread_for_user(interaction, "register")

    async def create_thread_for_user(self, interaction, action_type):
        thread = await interaction.channel.create_thread(
            name=f"{action_type.capitalize()} - {interaction.user.name}",
            type=discord.ChannelType.private_thread,
            invitable=False
        )
        await thread.add_user(interaction.user)

        await thread.send(
            f"👋 Привет, {interaction.user.mention}!\n"
            f"Пожалуйста, введи имя пользователя и пароль в формате: имя пароль для {action_type}."
        )

        def check(m):
            return m.channel == thread and m.author == interaction.user

        try:
            msg = await self.bot.wait_for('message', check=check, timeout=60)
            username, password = msg.content.strip().split(maxsplit=1)

            if action_type == "register":
                result = database.register_user(username, password)
                await thread.send(result)
            elif action_type == "login":
                success = database.login_user(interaction.user.id, username, password)
                if success:
                    await thread.send(f"🔐 Вход выполнен как {username}")
                else:
                    await thread.send("❌ Неверные данные для входа.")
        except asyncio.TimeoutError:
            await thread.send("⌛️ Время ожидания истекло.")
        except Exception as e:
            await thread.send(f"❌ Ошибка: {e}")
        finally:
            await asyncio.sleep(300)
            await thread.delete()

# 🧠 Cog с командой
class AuthCog(commands.Cog):
    def init(self, bot):
        self.bot = bot

    @commands.command()
    async def start(self, ctx):
        await ctx.send("🔐 Нажмите на кнопку для регистрации или входа в аккаунт!", view=StartView(self.bot))

# 📦 Setup
async def setup(bot):
    await bot.add_cog(AuthCog(bot))
