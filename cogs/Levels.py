# levels.py

import discord
from discord.ext import commands
import json
import random

# Level verilerini tutacağımız bir json dosyası oluşturalım
# Bu dosyada her kullanıcının sunucuya göre exp ve level değerlerini kaydedeceğiz
with open("levels.json", "w") as f:
    levels = {}
    json.dump(levels, f)

# Level sistemi için bir cogs sınıfı tanımlayalım
class Levels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Bir kullanıcı sunucuya katıldığında
    @commands.Cog.listener()
    async def on_member_join(self, member):
        # Json dosyasını açalım
        with open("levels.json", "r") as f:
            levels = json.load(f)
        # Kullanıcı için sunucuya özel bir veri oluşturalım
        await self.update_data(levels, member, member.guild)
        # Json dosyasını güncelleyelim
        with open("levels.json", "w") as f:
            json.dump(levels, f)

    # Bir kullanıcı mesaj gönderdiğinde
    @commands.Cog.listener()
    async def on_message(self, message):
        # Json dosyasını açalım
        with open("levels.json", "r") as f:
            levels = json.load(f)
        # Mesaj gönderen kullanıcıyı kontrol edelim
        if message.author.bot:
            return
        else:
            # Kullanıcı için sunucuya özel bir veri oluşturalım veya güncelleyelim
            await self.update_data(levels, message.author, message.guild)
            # Kullanıcıya rastgele bir exp ekleyelim
            await self.add_experience(levels, message.author, message.guild)
            # Kullanıcının seviye atlayıp atlamadığını kontrol edelim
            await self.level_up(levels, message.author, message.channel, message.guild)
        # Json dosyasını güncelleyelim
        with open("levels.json", "w") as f:
            json.dump(levels, f)

    # Kullanıcı için sunucuya özel bir veri oluşturan veya güncelleyen bir fonksiyon tanımlayalım
    async def update_data(self, levels, user, server):
        # Eğer kullanıcı ve sunucu kombinasyonu json dosyasında yoksa
        if not f"{user.id}-{server.id}" in levels:
            # Yeni bir veri oluşturalım
            levels[f"{user.id}-{server.id}"] = {}
            levels[f"{user.id}-{server.id}"]["exp"] = 0
            levels[f"{user.id}-{server.id}"]["level"] = 1

    # Kullanıcıya rastgele bir exp ekleyen bir fonksiyon tanımlayalım
    async def add_experience(self, levels, user, server):
        # Rastgele bir exp değeri belirleyelim (5 ile 10 arası)
        exp = random.randint(5, 10)
        # Kullanıcının exp değerini arttıralım
        levels[f"{user.id}-{server.id}"]["exp"] += exp

    # Kullanıcının seviye atlayıp atlamadığını kontrol eden bir fonksiyon tanımlayalım
    async def level_up(self, levels, user, channel, server):
        # Kullanıcının exp ve level değerlerini alalım
        exp = levels[f"{user.id}-{server.id}"]["exp"]
        level = levels[f"{user.id}-{server.id}"]["level"]
        # Kullanıcının level atlamak için gereken exp değerini hesaplayalım
        # Örneğin, her level için 100 exp gereksin
        level_up_exp = level * 500
        # Eğer kullanıcının exp değeri yeterliyse
        if exp >= level_up_exp:
            # Kullanıcının level değerini arttıralım
            levels[f"{user.id}-{server.id}"]["level"] += 1
            # Kullanıcıya bir mesaj gönderelim
            await channel.send(f":tada: Tebrikler {user.mention}, {levels[f'{user.id}-{server.id}']['level']} seviyeye yükseldin!")

    # Kullanıcının seviyesini gösteren bir komut tanımlayalım
    @commands.command()
    async def xp(self, ctx, member: discord.Member = None):
        # Json dosyasını açalım
        with open("levels.json", "r") as f:
            levels = json.load(f)
        # Eğer kullanıcı belirtilmediyse
        if not member:
            # Mesajı gönderen kullanıcının seviyesini gösterelim
            id = f"{ctx.author.id}-{ctx.guild.id}"
            level = levels[id]["level"]
            await ctx.send(f"Senin seviyen **{level}**!")
        else:
            # Belirtilen kullanıcının seviyesini gösterelim
            id = f"{member.id}-{ctx.guild.id}"
            level = levels[id]["level"]
            await ctx.send(f"**{member}** seviyesi **{level}**!")

# Botumuza cogs sınıfını ekleyelim
async def setup(bot):
    await bot.add_cog(Levels(bot))