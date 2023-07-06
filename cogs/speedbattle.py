import discord
from discord.ext import commands
import random
import json

class RaceGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.match = None # A tuple of (player1, player2, bet)

    @commands.command()
    async def speed(self, ctx, bet: int):
        # Check if the user has enough money to bet
        with open("money.json", "r") as f:
            money = json.load(f)
        user_id = str(ctx.author.id)
        if user_id not in money:
            money[user_id] = 100 # Give the user some starting money
        if bet > money[user_id]:
            await ctx.send("Bahis yapacak kadar paran yok!")
            return
        # Check if there is an ongoing match or not
        if self.match is None:
            # No match, create a new one with the user as player1
            self.match = (ctx.author, None, bet)
            await ctx.send(f"Yarışa katıldın. Bahis miktarın {bet}. Başka bir oyuncu bekliyorsun...")
        else:
            # There is a match, check if the user is already in it or not
            player1, player2, match_bet = self.match
            if ctx.author == player1:
                # The user is already in the match, do nothing
                await ctx.send("Zaten yarışa katıldın. Başka bir oyuncu bekliyorsun...")
            elif ctx.author == player2:
                # The user is already in the match, do nothing
                await ctx.send("Zaten yarışa katıldın. Yarış başlamak üzere...")
            else:
                # The user is not in the match, join as player2 and start the game
                if bet != match_bet:
                    # The bet amount must be equal to the match bet amount
                    await ctx.send(f"Yarışa katılmak için bahis miktarın {match_bet} olmalı.")
                    return
                self.match = (player1, ctx.author, bet)
                await ctx.send(f"Yarışa katıldın. Bahis miktarın {bet}. Yarış başlıyor...")
                await self.start_race(ctx)

    async def start_race(self, ctx):
        # Start the race game between the two players
        player1, player2, bet = self.match
        # Choose a random speed for each player between 1 and 10
        speed1 = random.randint(1, 10)
        speed2 = random.randint(1, 10)
        await ctx.send(f"{player1.name} hızı: {speed1}")
        await ctx.send(f"{player2.name} hızı: {speed2}")
        if speed1 > speed2:
            # Player1 wins and gets double the bet amount
            await ctx.send(f"{player1.name} yarışı kazandı! Bahis miktarının iki katını alır.")
            self.update_money(player1.id, bet * 2)
            self.update_money(player2.id, -bet)
        elif speed1 < speed2:
            # Player2 wins and gets double the bet amount
            await ctx.send(f"{player2.name} yarışı kazandı! Bahis miktarının iki katını alır.")
            self.update_money(player1.id, -bet)
            self.update_money(player2.id, bet * 2)
        else:
            # Tie and nothing happens
            await ctx.send("Yarış berabere bitti! Hiçbir şey olmaz.")
        # Show the players their current balance
        await ctx.send(f"{player1.name} güncel bakiyesi: {self.get_money(player1.id)}")
        await ctx.send(f"{player2.name} güncel bakiyesi: {self.get_money(player2.id)}")
        # Reset the match to None
        self.match = None

    def get_money(self, user_id):
        # Get the money value of a user from money.json
        with open("money.json", "r") as f:
            money = json.load(f)
        user_id = str(user_id)
        if user_id not in money:
            money[user_id] = 100 # Give the user some starting money
        return money[user_id]

    def update_money(self, user_id, amount):
        # Update the money value of a user in money.json by adding or subtracting an amount
        with open("money.json", "r") as f:
            money = json.load(f)
        user_id = str(user_id)
        if user_id not in money:
            money[user_id] = 100 # Give the user some starting money
        money[user_id] += amount
        with open("money.json", "w") as f:
            json.dump(money, f, indent=4)

async def setup(bot):
    await bot.add_cog(RaceGame(bot))
