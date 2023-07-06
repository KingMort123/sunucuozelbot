# Bu kodu sadece örnek olarak veriyorum, çalıştığından emin değilim.
# Verileri json dosyasından çekmek için json modülünü kullanacağım.
# Param komutu için discord.ext.commands modülünü kullanacağım.

import discord
from discord.ext import commands
import json

# Param komutunu içeren bir sınıf oluşturalım
class money(commands.Cog):
  # Sınıfın başlatıcı fonksiyonunu tanımlayalım
  def __init__(self, bot):
    # Bot değişkenini sınıfın bir özelliği olarak kaydedelim
    self.bot = bot
  
  # Param komutunu tanımlayalım
  @commands.command()
  @commands.cooldown (1, 10, commands.BucketType.user) 
  async def param(self, ctx):
    # Json dosyasını açalım
    with open("money.json", "r") as f:
      # Json verisini bir sözlük olarak yükleyelim
      data = json.load(f)
    # Sözlükten para değerini alalım
    # Kullanıcının kimliğini alalım
    user_id = str(ctx.author.id)
# Sözlükten kullanıcıya ait para değerini alalım
    result = data.get(user_id)

    # Sonucu kontrol edelim
    if result is None:
      # Para değeri bulunamadıysa bir hata mesajı gönderelim
      await ctx.send("Hiç TCoin yok")
    else:
      # Para değeri bulunduysa sonucu mesaj şeklinde gönderelim
      # Sonucu virgülden sonra iki basamak olacak şekilde yuvarlayalım
      await ctx.send(f"**{ctx.author.name}** kullanıcısının TCoin'leri: **{format(result, ',')}**")

  @commands.command()
  @commands.cooldown (1, 10, commands.BucketType.user) 
  async def kayit(self, ctx):
    # Kullanıcının kimliğini alalım
    user_id = str(ctx.author.id)
    # Json dosyasını açalım
    with open("money.json", "r") as f:
      # Json verisini bir sözlük olarak yükleyelim
      data = json.load(f)
    # Sözlükte kullanıcı kimliğinin olup olmadığını kontrol edelim
    if user_id in data:
      # Kullanıcı zaten kayıtlıysa bir uyarı mesajı gönderelim
      await ctx.send("Zaten kayıtlısın.")
    else:
      # Kullanıcı kayıtlı değilse sözlüğe kullanıcı kimliği ve para değeri ekleyelim
      data[user_id] = 50
      # Json dosyasını yazma modunda açalım
      with open("money.json", "w") as f:
        # Sözlüğü json verisi olarak dosyaya yazalım
        json.dump(data, f)
      # Kayıt işleminin başarılı olduğunu belirten bir mesaj gönderelim
      await ctx.send("Kaydın başarıyla yapıldı.")

  @commands.command()
  @commands.is_owner() # Bu dekoratörle komutu sadece botun sahibinin kullanabileceğini belirtelim
  async def para_gonder(self, ctx, member: discord.Member, amount: int):
    # Etiketlenen kullanıcının kimliğini alalım
    user_id = str(member.id)
    # Json dosyasını açalım
    with open("money.json", "r") as f:
      # Json verisini bir sözlük olarak yükleyelim
      data = json.load(f)
    # Sözlükte kullanıcı kimliğinin olup olmadığını kontrol edelim
    if user_id in data:
      # Kullanıcı kayıtlıysa sözlükteki para değerini güncelleyelim
      data[user_id] = amount
      # Json dosyasını yazma modunda açalım
      with open("money.json", "w") as f:
        # Sözlüğü json verisi olarak dosyaya yazalım
        json.dump(data, f)
      # Para gönderme işleminin başarılı olduğunu belirten bir mesaj gönderelim
      await ctx.send(f"{member.mention} adlı kullanıcının parası {amount} olarak güncellendi.")
    else:
      # Kullanıcı kayıtlı değilse bir hata mesajı gönderelim
      await ctx.send(f"{member.mention} adlı kullanıcı kayıtlı değil.")  

  @commands.command()
  async def gonder(self, ctx, member: discord.Member, miktar: int):
    sender_id = str(ctx.author.id) # gönderenin ID'sini alır
    receiver_id = str(member.id) # alıcının ID'sini alır
    with open("money.json", "r") as f: # json dosyasını okur
      data = json.load(f)
    if sender_id in data and receiver_id in data: # eğer gönderen ve alıcı json dosyasında varsa
      sender_balance = data[sender_id] # gönderenin para değerini alır
      receiver_balance = data[receiver_id] # alıcının para değerini alır
      if sender_balance >= miktar: # eğer gönderenin yeterli parası varsa
        sender_balance -= miktar # gönderenin parasından miktarı çıkarır
        receiver_balance += miktar # alıcının parasına miktarı ekler
        data[sender_id] = sender_balance # json dosyasındaki değeri günceller
        data[receiver_id] = receiver_balance # json dosyasındaki değeri günceller
        with open("money.json", "w") as f: # json dosyasını yazar
          json.dump(data, f)
        await ctx.send(f"{ctx.author.mention}, {member.mention}'a {miktar} para gönderdin.") # mesaj gönderir
      else: # eğer gönderenin yeterli parası yoksa
        await ctx.send(f"{ctx.author.mention}, yeterli paran yok.") # mesaj gönderir
    else: # eğer gönderen veya alıcı json dosyasında yoksa
      await ctx.send(f"{ctx.author.mention}, kayıtlı değilsin veya {member.mention} kayıtlı değil.") # mesaj gönderir

async def setup(bot):
  await bot.add_cog(money(bot))
