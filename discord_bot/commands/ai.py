import discord
from discord.ext import commands
import sqlite3
import requests
import urllib.parse
import os

from tgbot.config import DB_PATH, VOICE_COST, active_sessions

class AI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ask(self, ctx, *, prompt: str):
        try:
            user = active_sessions.get(ctx.author.id)
            if not user:
                return await ctx.send("❌ Сначала войдите с `.login`")

            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("SELECT personality FROM users WHERE name = ?", (user,))
            row = c.fetchone()
            conn.close()

            personality = row[0] if row and row[0] else "Hacker"
            full_prompt = f"{personality}: {prompt}"
            encoded_prompt = urllib.parse.quote(full_prompt)
            url = f"https://text.pollinations.ai/{encoded_prompt}?model=openai-text"

            print(f"[ASK] Отправляю запрос: {url}")
            response = requests.get(url)
            print(f"[ASK] Код ответа: {response.status_code}")

            if response.ok:
                await ctx.send(response.text)
            else:
                await ctx.send(f"❌ Ошибка: {response.status_code}")
        except Exception as e:
            print(f"[ASK] Ошибка: {e}")
            await ctx.send(f"❌ Ошибка: {e}")

    @commands.command()
    async def say(self, ctx, *, prompt: str):
        try:
            user = active_sessions.get(ctx.author.id)
            if not user:
                return await ctx.send("❌ Сначала войдите с `.login`")

            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("SELECT voice, points FROM users WHERE name = ?", (user,))
            row = c.fetchone()

            if not row or not row[0]:
                conn.close()
                return await ctx.send("❌ Установите голос через `.choose`")

            voice, points = row
            if points < VOICE_COST:
                conn.close()
                return await ctx.send("❌ Недостаточно поинтов. Нужен минимум 5.")

            encoded_prompt = urllib.parse.quote(prompt)
            url = f"https://text.pollinations.ai/{encoded_prompt}?model=openai-audio&voice={voice}"

            print(f"[SAY] Отправляю запрос: {url}")
            print(f"[SAY] Используется голос: {voice}")
            response = requests.get(url)

            if response.ok:
                with open("voice.mp3", "wb") as f:
                    f.write(response.content)

                c.execute("UPDATE users SET points = points - ? WHERE name = ?", (VOICE_COST, user))
                conn.commit()

                await ctx.send("🔊 Вот ваш голосовой ответ:", file=discord.File("voice.mp3"))
                os.remove("voice.mp3")
            else:
                await ctx.send("❌ Ошибка при получении аудио.")
            conn.close()

        except Exception as e:
            print(f"[SAY] Ошибка: {e}")
            await ctx.send(f"❌ Ошибка: {e}")

# async setup-функция для загрузки команды ботом
async def setup(bot):
    await bot.add_cog(AI(bot))
