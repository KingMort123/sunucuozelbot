# blackjack.py
import discord
from discord.ext import commands
import json
import random
import asyncio

class Blackjack(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # desteyi oluştur
        self.deck = [
            "A♠", "A♥", "A♦", "A♣",
            "2♠", "2♥", "2♦", "2♣",
            "3♠", "3♥", "3♦", "3♣",
            "4♠", "4♥", "4♦", "4♣",
            "5♠", "5♥", "5♦", "5♣",
            "6♠", "6♥", "6♦", "6♣",
            "7♠", "7♥", "7♦", "7♣",
            "8♠", "8♥", "8♦", "8♣",
            "9♠", "9♥", "9♦", "9♣",
            "10♠", "10♥", "10♦", "10♣",
            "J♠", "J♥", "J♦", "J♣",
            "Q♠", "Q♥", "Q♦", "Q♣",
            "K♠", "K♥", "K♦", "K♣"
        ]
        # kartların değerlerini belirle
        self.values = {
            'A': 1,
            '2': 2,
            '3': 3,
            '4': 4,
            '5': 5,
            '6': 6,
            '7': 7,
            '8': 8,
            '9': 9,
            '10': 10,
            'J': 10,
            'Q': 10,
            'K': 10
        }

    @commands.command()
    @commands.cooldown (1, 10, commands.BucketType.user) 
    async def blackjack(self, ctx, bet: int):
        # money.json dosyasını aç
        with open("money.json", "r") as f:
            data = json.load(f)

        # kullanıcı kayıtlı değilse, kayıt komutunu kullanmasını söyle
        if str(ctx.author.id) not in data:
            await ctx.send("Kayıtlı değilsin. Lütfen .kayit komutunu kullan.")

        # kullanıcı kayıtlı ise, bahis miktarını kontrol et
        else:
            # bahis miktarı 0 veya daha küçükse, hata ver
            if bet <= 0:
                await ctx.send("Bahis miktarı 0 veya daha küçük olamaz.")
                return

            # bahis miktarı kullanıcının parasından fazlaysa, hata ver
            if bet > data[str(ctx.author.id)]:
                await ctx.send("Bahis miktarı paranızdan fazla olamaz.")
                return

            # bahis miktarını kullanıcının parasından düş
            data[str(ctx.author.id)] -= bet

            # money.json dosyasını güncelle
            with open("money.json", "w") as f:
                json.dump(data, f)

            # desteyi karıştır
            random.shuffle(self.deck)

            # oyuncu ve botun kartlarını ve değerlerini tutacak listeler oluştur
            player_cards = []
            player_value = 0
            bot_cards = []
            bot_value = 0

            # oyuncu ve bota ikişer kart dağıt
            for i in range(2):
                player_cards.append(self.deck.pop())
                bot_cards.append(self.deck.pop())

            # oyuncunun kartlarının değerini hesapla
            for card in player_cards:
                # kartın değerini al (sembolü sil)
                value = card[:-1]
                # değeri oyuncunun toplamına ekle
                player_value += self.values[value]
                # eğer as varsa ve toplam 21'i geçiyorsa, değeri 1 olarak say
                if value == 'A' and player_value > 21:
                    player_value -= 10

            # botun ilk kartının değerini hesapla (ikinci kart kapalı)
            value = bot_cards[0][:-1]
            bot_value += self.values[value]

            # oyuncu ve botun kartlarını göster
            await ctx.send(f"{ctx.author.mention}, kartların: {', '.join(player_cards)} | Toplam: {player_value}")
            await ctx.send(f"Botun kartları: {bot_cards[0]}, ❓ | Toplam: {bot_value}")

            # eğer oyuncu 21 yapmışsa, blackjack olur ve oyuncu kazanır
            if player_value == 21:
                await ctx.send(f"{ctx.author.mention}, blackjack yaptın! Tebrikler, kazandın! 💰")
                # bahis miktarının iki katını geri al
                data[str(ctx.author.id)] += bet * 2
                # money.json dosyasını güncelle
                with open("money.json", "w") as f:
                    json.dump(data, f)
                return

            # eğer oyuncu 21 yapmamışsa, oyun devam eder
            else:
                # oyuncuya kart isteyip istemediğini sor
                await ctx.send(f"{ctx.author.mention}, kart istiyor musun? (evet/hayır)")

                # oyuncunun cevabını bekleyen bir döngü başlat
                while True:
                    try:
                        # oyuncunun cevabını al (30 saniye içinde)
                        answer = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30)
                    except asyncio.TimeoutError:
                        # zaman aşımı olursa, oyunu bitir
                        await ctx.send(f"{ctx.author.mention}, zamanın doldu. Oyun bitti.")
                        return

                    # cevap evet ise, oyuncuya bir kart daha ver
                    if answer.content.lower() == 'evet':
                        player_cards.append(self.deck.pop())
                        # oyuncunun kartlarının değerini hesapla
                        for card in player_cards[-1:]:
                            value = card[:-1]
                            player_value += self.values[value]
                            if value == 'A' and player_value > 21:
                                player_value -= 10

                        # oyuncunun yeni kartlarını göster
                        await ctx.send(f"{ctx.author.mention}, yeni kartın: {player_cards[-1]} | Toplam: {player_value}")

                        # eğer oyuncu 21 yapmışsa, blackjack olur ve oyuncu kazanır
                        if player_value == 21:
                            await ctx.send(f"{ctx.author.mention}, blackjack yaptın! Tebrikler,                            kazandın! 💰")
                            # bahis miktarının iki katını geri al
                            data[str(ctx.author.id)] += bet * 2
                            # money.json dosyasını güncelle
                            with open("money.json", "w") as f:
                                json.dump(data, f)
                            return

                        # eğer oyuncu 21'i aşmışsa, oyuncu kaybeder
                        elif player_value > 21:
                            await ctx.send(f"{ctx.author.mention}, 21'i aştın. Kaybettin. 😢")
                            # bahis miktarını kaybet
                            # money.json dosyası zaten güncellendi
                            return

                        # eğer oyuncu 21'i aşmamışsa, oyuncuya kart isteyip istemediğini tekrar sor
                        else:
                            await ctx.send(f"{ctx.author.mention}, kart istiyor musun? (evet/hayır)")

                    # cevap hayır ise, oyuncu durur ve botun sırası gelir
                    elif answer.content.lower() == 'hayır':
                        await ctx.send(f"{ctx.author.mention}, durdun. Botun sırası.")
                        break

                    # cevap evet veya hayır dışında ise, geçerli bir cevap vermesini söyle
                    else:
                        await ctx.send(f"{ctx.author.mention}, lütfen geçerli bir cevap ver. (evet/hayır)")

                # botun ikinci kartının değerini hesapla
                value = bot_cards[1][:-1]
                bot_value += self.values[value]
                if value == 'A' and bot_value > 21:
                    bot_value -= 10

                # botun yeni kartlarını göster
                await ctx.send(f"Botun yeni kartları: {', '.join(bot_cards)} | Toplam: {bot_value}")

                # eğer bot 21 yapmışsa, blackjack olur ve bot kazanır
                if bot_value == 21:
                    await ctx.send(f"Bot blackjack yaptı! Kaybettin. 😢")
                    # bahis miktarını kaybet
                    # money.json dosyası zaten güncellendi
                    return

                # eğer bot 21 yapmamışsa, oyun devam eder
                else:
                    # bot 17 veya daha yüksek bir değere ulaşana kadar kart istemeye devam eder
                    while bot_value < 17:
                        bot_cards.append(self.deck.pop())
                        # botun kartlarının değerini hesapla
                        for card in bot_cards[-1:]:
                            value = card[:-1]
                            bot_value += self.values[value]
                            if value == 'A' and bot_value > 21:
                                bot_value -= 10

                        # botun yeni kartlarını göster
                        await ctx.send(f"Bot yeni bir kart aldı: {bot_cards[-1]} | Toplam: {bot_value}")

                    # eğer bot 21'i aşmışsa, bot kaybeder ve oyuncu kazanır
                    if bot_value > 21:
                        await ctx.send(f"Bot 21'i aştı! Tebrikler, kazandın! 💰")
                        # bahis miktarının iki katını geri al
                        data[str(ctx.author.id)] += bet * 2
                        # money.json dosyasını güncelle
                        with open("money.json", "w") as f:
                            json.dump(data, f)
                        return

                    # eğer bot da durmuşsa, kartların toplam değerine bakılır
                    else:
                        await ctx.send(f"Bot durdu. Sonuçlar:")

                        # oyuncu ve botun son kartlarını ve değerlerini göster
                        await ctx.send(f"{ctx.author.mention}, kartların: {', '.join(player_cards)} | Toplam: {player_value}")
                        await ctx.send(f"Botun kartları: {', '.join(bot_cards)} | Toplam: {bot_value}")

                        # daha yüksek değere sahip olan kazanır
                        if player_value > bot_value:
                            await ctx.send(f"{ctx.author.mention}, senin değerin daha yüksek. Tebrikler, kazandın! 💰")
                            # bahis miktarının iki katını geri al
                            data[str(ctx.author.id)] += bet * 2

                        # eğer değerler eşitse, berabere olur
                        elif player_value == bot_value:
                            await ctx.send(f"Değerler eşit. Berabere. 😐")
                            # bahis miktarını geri al
                            data[str(ctx.author.id)] += bet

                        # değilse, botun değeri daha yüksektir ve bot kazanır
                        else:
                            await ctx.send(f"Botun değeri daha yüksek. Kaybettin. 😢")
                            # bahis miktarını kaybet
                            # money.json dosyası zaten güncellendi

                        # money.json dosyasını güncelle
                        with open("money.json", "w") as f:
                            json.dump(data, f)
                        return

# cog'u yükle
async def setup(bot):
    await bot.add_cog(Blackjack(bot))
