from discord.ext import commands
import discord
from dotenv import load_dotenv
import os
from openai import OpenAI
import sqlite3
import json

load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENAI_KEY"),
)
DISCORD = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.typing = True
bot = commands.Bot(command_prefix='.', intents=intents)


def init_db():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                userID TEXT PRIMARY KEY,
                messages TEXT
            )
        """)
    conn.commit()


def user_check(user_id, limit):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE userID=(?)", (user_id,))
    result = cur.fetchone()
    conn.close()
    if result is None or len(json.loads(result[1])) <= limit:
        return True
    else:
        return False


def fetch_messages(user_id):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE userID=(?)", (user_id,))
    response = cur.fetchone()
    con.close()
    if response is None:
        return []
    return json.loads(response[1])


def save_messages(user_id, messages):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute("INSERT OR REPLACE INTO users (userID, messages) VALUES (?, ?)", (user_id, json.dumps(messages)))
    con.commit()
    con.close()


@bot.command('text')
async def openai_input_text(ctx, *, message):
    if not user_check(ctx.author.id, 10):
        await ctx.send('You are currently over the allowed quota for text responses. Thank you for trying us out!')
        return
    messages = fetch_messages(ctx.author.id)
    messages.append(
        {"role": "user", "content": message},
    )
    async with ctx.typing():
        try:
            chat_completion = client.chat.completions.create(
                model="gpt-4o-mini", messages=messages
            )
            reply = chat_completion.choices[0].message.content
            await ctx.send(reply)
            messages.append(
                {"role": "assistant", "content": reply},
            )
            save_messages(ctx.author.id, messages)
        except Exception as e:
            print(e)
            await ctx.send('Error')


@bot.command('image')
async def openai_input_image(ctx, *, message):
    if not user_check(ctx.author.id, 3):
        await ctx.send('You are currently over the allowed quota for image responses. Thank you for trying us out!')
        return
    async with ctx.typing():
        try:
            response = client.images.generate(
                model="dall-e-2",
                prompt=message,
                size="512x512",
                quality="standard",
                n=1,
            )
            reply = response.data[0].url
            await ctx.send(reply)
        except Exception as e:
            print(e)
            await ctx.send('Error')

init_db()
bot.run(DISCORD)
