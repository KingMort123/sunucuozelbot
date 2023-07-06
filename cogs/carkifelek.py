# Bu kodu sadece örnek olarak veriyorum, çalıştığından emin değilim.
# Verileri json dosyasından çekmek ve yazmak için json modülünü kullanacağım.
# Çarkıfelek komutu için discord.ext.commands modülünü kullanacağım.
# Rastgele bir değer seçmek için random modülünü kullanacağım.

import discord
from discord.ext import commands
import json
import random

# Çarkıfelek komutunu içeren bir sınıf oluşturalım
class Carkifelek(commands.Cog):
  # Sınıfın başlatıcı fonksiyonunu tanımlayalım
  def __init__(self, bot):
    # Bot değişkenini sınıfın bir özelliği olarak kaydedelim
    self.bot = bot
    # Çarktaki olası değerleri ve katlarını bir sözlük olarak tanımlayalım
    self.cark = {
      "🍒": -1,
      "🍋": 2,
      "🍇": 2,
      "🍉": -1,
      "🍊": -1,
      "🍎": -1,
      "🍓": -1,
      "🍀": 3,
      "💥": 0
    }
  
  # Çarkıfelek komutunu tanımlayalım
  @commands.command()
  @commands.cooldown (1, 10, commands.BucketType.user) 
  async def carkifelek(self, ctx, amount: int):
    if amount>500000:
      await ctx.send("En fazla 500,000 oynayabilirsin.")
    else:
      # Kullanıcının kimliğini alalım
      user_id = str(ctx.author.id)
      # Json dosyasını açalım
      with open("money.json", "r") as f:
        # Json verisini bir sözlük olarak yükleyelim
        data = json.load(f)
      # Sözlükte kullanıcı kimliğinin olup olmadığını kontrol edelim
      if user_id in data:
        # Kullanıcı kayıtlıysa sözlükten para değerini alalım
        para = data[user_id]
        # Para değerinin yeterli olup olmadığını kontrol edelim
        if para >= amount:
          # Sözlükteki para değerini güncelleyelim
          data[user_id] = para
          # Json dosyasını yazma modunda açalım
          with open("money.json", "w") as f:
            # Sözlüğü json verisi olarak dosyaya yazalım
            json.dump(data, f)
          # Çark animasyonunu göstermek için bir mesaj gönderelim
          mesaj = await ctx.send("Çark dönüyor...")
          # Çarktaki değerlerden rastgele birini seçelim
          sonuc = random.choice(list(self.cark.keys()))
          # Sonucun katını alalım
          kat = self.cark[sonuc]
          # Girilen miktarı kat ile çarpalım
          kazanc = amount * kat
          # Para değerine kazancı ekleyelim
          para += kazanc
          # Sözlükteki para değerini güncelleyelim
          data[user_id] = para
          # Json dosyasını yazma modunda açalım
          with open("money.json", "w") as f:
            # Sözlüğü json verisi olarak dosyaya yazalım
            json.dump(data, f)
          # Mesajı sonuçla güncelleyelim
          await mesaj.edit(content=f"Çark durdu: {sonuc}\n{ctx.author.mention}, **{amount}** para yatırdın ve **{kazanc}** para kazandın!")
        else:
          # Para değeri yetersizse bir hata mesajı gönderelim
          await ctx.send(f"{ctx.author.mention}, çarkıfelek oynamak için yeterli paran yok.")
      else:
        # Kullanıcı kayıtlı değilse bir hata mesajı gönderelim
        await ctx.send(f"{ctx.author.mention}, kayıtlı değilsin. Lütfen önce kayit komutunu kullan.")

# Sınıfın bot tarafından yüklenmesini sağlayalım
async def setup(bot):
  await bot.add_cog(Carkifelek(bot))
