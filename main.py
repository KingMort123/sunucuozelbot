import discord
from discord.ext import commands
import os
import asyncio
import json
import time
import random

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())

async def load_extensions():
  for f in os.listdir("./cogs"):
    if f.endswith(".py"):
      await bot.load_extension("cogs." + f[:-3])


# Cog dosyalarının sonunda .py olduğunu varsayıyoruz
asyncio.run(load_extensions())

@bot.event
async def on_ready():
    global money
    with open("money.json", "r") as f:
        money = json.load(f)
    print("Bot is ready.")


@bot.command()
@commands.is_owner()
async def paragonder(ctx, miktar: int, kullanıcı: discord.Member):
    # money sözlüğünde kullanıcının ID'sini anahtar olarak kullan
    user_id = str(kullanıcı.id)
    # eğer kullanıcı sözlükte yoksa, yeni bir anahtar-değer çifti oluştur
    if user_id not in money:
        money[user_id] = 0
    # değer olarak miktarı ekle
    money[user_id] += miktar
    # money.json dosyasını güncelle
    with open("money.json", "w") as f:
        json.dump(money, f)
    # bir mesaj gönder
    await ctx.send(f"{kullanıcı.mention} adlı kullanıcıya {miktar} para gönderildi.")

cooldown_message_sent = False

import asyncio

cooldown_message_sent = False

@bot.event
async def on_command_error(ctx, error):
  global cooldown_message_sent
  if isinstance(error, commands.CommandOnCooldown):
    if not cooldown_message_sent:
      await ctx.send(f'Bu komutu tekrar kullanmak için **{error.retry_after:.2f}** saniye beklemeniz gerekiyor.')
      cooldown_message_sent = True
      await asyncio.sleep(error.retry_after) # cooldown süresi kadar bekler
      cooldown_message_sent = False

@bot.command()
async def baskin(ctx):
    await ctx.send("Baskın yapılıyor... Yakalandınız tazminat davası cezası yediniz -6 milyar TCoin.")

bot.run("NzUyMTQ4MDE3ODI1NDQ3OTc3.G_v9Ko.WpIep1A3cwyAj4TX1kVATL7hp9E5eJrLLzL3Po")