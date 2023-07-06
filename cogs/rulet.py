import discord
from discord.ext import commands
import random
import json

class RussianRoulette(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rulet(self, ctx, bet: int):
        # Check if the user has enough money to bet
        with open("money.json", "r") as f:
            money = json.load(f)
        user_id = str(ctx.author.id)
        if user_id not in money:
            money[user_id] = 100 # Give the user some starting money
        if bet > money[user_id]:
            await ctx.send("Bahis yapacak kadar paran yok!")
            return
        # Choose a random chamber out of six
        chamber = random.randint(1, 2)
        await ctx.send("Tabancayı çeviriyorsun ve tetiği çekiyorsun...")
        if chamber == 1:
            # User loses and loses all their money
            await ctx.send("BANG! Öldün! Tüm paranı kaybettin.")
            money[user_id] = 0
        else:
            # User survives and gets triple the bet amount
            await ctx.send("Click! Hayattasın! Bahis miktarının üç katını alırsın.")
            money[user_id] += bet * 3
        # Save the updated money data
        with open("money.json", "w") as f:
            json.dump(money, f, indent=4)
        # Show the user their current balance
        await ctx.send(f"Güncel bakiyen {money[user_id]}.")

async def setup(bot):
    await bot.add_cog(RussianRoulette(bot))
