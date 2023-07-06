# calis.py
import discord
from discord.ext import commands
import json
import random
import asyncio

class Calis(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown (1, 10, commands.BucketType.user) 
    async def calis(self, ctx):
        # money.json dosyasını aç
        with open("money.json", "r") as f:
            data = json.load(f)

        # kullanıcı kayıtlı değilse, kayıt komutunu kullanmasını söyle
        if str(ctx.author.id) not in data:
            await ctx.send("Kayıtlı değilsin. Lütfen .kayit komutunu kullan.")

        # kullanıcı kayıtlı ise, çalışma animasyonu göster ve rastgele bir miktar para kazan
        else:
            await ctx.send(f"{ctx.author.mention} çalışmaya başladı 🛠️")
            # 3 saniye bekle
            await asyncio.sleep(3)
            # 10 ile 100 arasında rastgele bir miktar para seç
            amount = random.randint(10, 20000)
            # para miktarını kullanıcının hesabına ekle
            data[str(ctx.author.id)] += amount
            # money.json dosyasını güncelle
            with open("money.json", "w") as f:
                json.dump(data, f)
            # kullanıcıya kazandığı parayı bildir
            await ctx.send(f"{ctx.author.mention} çalışmayı bitirdi ve {amount} TCoin kazandı 💰")

# cog'u yükle
async def setup(bot):
    await bot.add_cog(Calis(bot))
