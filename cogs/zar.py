import discord
from discord.ext import commands
import random
import json

class DiceGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def dice(self, ctx, bet: int):
        # Kullanıcının bahis yapacak kadar parası olup olmadığını kontrol et
        with open("money.json", "r") as f:
            money = json.load(f)
        user_id = str(ctx.author.id)
        if user_id not in money:
            money[user_id] = 100 # Kullanıcıya başlangıç parası ver
        if bet > money[user_id]:
            await ctx.send("Bahis yapacak kadar paran yok!")
            return
        # İki zar at ve karşılaştır
        dice1 = random.randint(1, 3)
        dice2 = random.randint(1, 3)
        await ctx.send(f"{dice1} ve {dice2} attın.")
        if dice1 > dice2:
            # Kullanıcı kazanır ve bahis miktarının iki katını alır
            await ctx.send("Kazandın! Bahis miktarının iki katını alırsın.")
            money[user_id] += bet * 2
        elif dice1 < dice2:
            # Kullanıcı kaybeder ve bahis miktarını kaybeder
            await ctx.send("Kaybettin! Bahis miktarını kaybedersin.")
            money[user_id] -= bet
        else:
            # Berabere ve hiçbir şey olmaz
            await ctx.send("Berabere! Hiçbir şey olmaz.")
        # Güncellenmiş para verilerini kaydet
        with open("money.json", "w") as f:
            json.dump(money, f, indent=4)
        
        paran = money[user_id]
        # Kullanıcıya güncel bakiyesini göster{format(result, ',')}
        await ctx.send(f"Güncel bakiyen **{format(paran, ',')}**.")

async def setup(bot):
    await bot.add_cog(DiceGame(bot))
