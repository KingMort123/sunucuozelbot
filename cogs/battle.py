import discord
from discord.ext import commands
import random
import json

class BattleGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.match = None # A tuple of (player1, player2, bet)
        self.animals = ["aslan", "kaplan", "ayı", "timsah", "kartal", "köpekbalığı", "fil", "goril"] # A list of possible animals
        self.weapons = ["kılıç", "balta", "mızrak", "ok", "bıçak", "sopa", "zincir", "kama"] # A list of possible weapons

    @commands.command()
    async def battle(self, ctx, bet: int):
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
            await ctx.send(f"Savaşa katıldın. Bahis miktarın {bet}. Başka bir oyuncu bekliyorsun...")
        else:
            # There is a match, check if the user is already in it or not
            player1, player2, match_bet = self.match
            if ctx.author == player1:
                # The user is already in the match, do nothing
                await ctx.send("Zaten savaşa katıldın. Başka bir oyuncu bekliyorsun...")
            elif ctx.author == player2:
                # The user is already in the match, do nothing
                await ctx.send("Zaten savaşa katıldın. Savaş başlamak üzere...")
            else:
                # The user is not in the match, join as player2 and start the game
                if bet != match_bet:
                    # The bet amount must be equal to the match bet amount
                    await ctx.send(f"Savaşa katılmak için bahis miktarın {match_bet} olmalı.")
                    return
                self.match = (player1, ctx.author, bet)
                await ctx.send(f"Savaşa katıldın. Bahis miktarın {bet}. Savaş başlıyor...")
                await self.start_battle(ctx)

    async def start_battle(self, ctx):
        # Start the battle game between the two players
        player1, player2, bet = self.match
        # Choose a random animal and weapon for each player
        animal1 = random.choice(self.animals)
        weapon1 = random.choice(self.weapons)
        animal2 = random.choice(self.animals)
        weapon2 = random.choice(self.weapons)
        await ctx.send(f"{player1.name} hayvanı: {animal1}")
        await ctx.send(f"{player1.name} silahı: {weapon1}")
        await ctx.send(f"{player2.name} hayvanı: {animal2}")
        await ctx.send(f"{player2.name} silahı: {weapon2}")
        # Calculate the score for each player based on some arbitrary rules
        score1 = self.calculate_score(animal1, weapon1, animal2, weapon2)
        score2 = self.calculate_score(animal2, weapon2, animal1, weapon1)
        if score1 > score2:
            # Player1 wins and gets double the bet amount
            await ctx.send(f"{player1.name} savaşı kazandı! Bahis miktarının iki katını alır.")
            self.update_money(player1.id, bet * 2)
            self.update_money(player2.id, -bet)
        elif score1 < score2:
            # Player2 wins and gets double the bet amount
            await ctx.send(f"{player2.name} savaşı kazandı! Bahis miktarının iki katını alır.")
            self.update_money(player1.id, -bet)
            self.update_money(player2.id, bet * 2)
        else:
            # Tie and nothing happens
            await ctx.send("Savaş berabere bitti! Hiçbir şey olmaz.")
        # Show the players their current balance
        await ctx.send(f"{player1.name} güncel bakiyesi: {self.get_money(player1.id)}")
        await ctx.send(f"{player2.name} güncel bakiyesi: {self.get_money(player2.id)}")
        # Reset the match to None
        self.match = None

    def calculate_score(self, animal, weapon, opponent_animal, opponent_weapon):
        # A function that returns a score for a player based on some arbitrary rules
        score = 0
        # Add some points based on the animal's strength
        if animal == "aslan":
            score += 8
        elif animal == "kaplan":
            score += 7
        elif animal == "ayı":
            score += 9
        elif animal == "timsah":
            score += 6
        elif animal == "kartal":
            score += 5
        elif animal == "köpekbalığı":
            score += 4
        elif animal == "fil":
            score += 10
        elif animal == "goril":
            score += 7
        # Add some points based on the weapon's power
        if weapon == "kılıç":
            score += 8
        elif weapon == "balta":
            score += 7
        elif weapon == "mızrak":
            score += 6
        elif weapon == "ok":
            score += 5
        elif weapon == "bıçak":
            score += 4
        elif weapon == "sopa":
            score += 3
        elif weapon == "zincir":
            score += 4
        elif weapon == "kama":
            score += 3
        # Add or subtract some points based on the animal and weapon combination
        if animal == "aslan" and weapon == "kılıç":
            score += 2 # A lion with a sword is very strong
        elif animal == "fil" and weapon == "ok":
            score -= 2 # An elephant with an arrow is not very effective
        elif animal == "kartal" and weapon == "mızrak":
            score += 2 # An eagle with a spear can fly and attack from above
        elif animal == "timsah" and weapon == "sopa":
            score -= 2 # A crocodile with a stick is not very threatening
        # Add or subtract some points based on the opponent's animal and weapon combination
        if opponent_animal == "aslan" and opponent_weapon == "kılıç":
            score -= 2 # The opponent is very strong
        elif opponent_animal == "fil" and opponent_weapon == "ok":
            score += 2 # The opponent is not very effective
        elif opponent_animal == "kartal" and opponent_weapon == "mızrak":
            score -= 2 # The opponent can fly and attack from above
        elif opponent_animal == "timsah" and opponent_weapon == "sopa":
            score += 2 # The opponent is not very threatening
        return score

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
    await bot.add_cog(BattleGame(bot))
