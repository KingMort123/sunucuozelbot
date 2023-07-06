import discord
from discord.ext import commands

class DM(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def dm(self, ctx, member: discord.Member, *, message: str):
        # Check if the member is valid
        if member is None:
            await ctx.send("Lütfen geçerli bir üye etiketleyin.")
            return
        
        # Check if the message is empty
        if message == "":
            await ctx.send("Lütfen bir mesaj yazın.")
            return
        
        # Send the message to the member's DM
        await member.send(message)

        # Send a confirmation message to the context channel
        await ctx.send(f"{member.name} adlı üyeye DM'den mesaj yollandı.")

# Add the cog to the bot
async def setup(bot):
    await bot.add_cog(DM(bot))
