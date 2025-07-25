import discord
from discord.ext import commands
from config import token
from logic import MyPokemon as Pokemon


intents = discord.Intents.default()  
intents.messages = True              
intents.message_content = True       
intents.guilds = True                

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Giriş yapıldı:  {bot.user.name}')  

@bot.command()
async def go(ctx):
    author = ctx.author.name
    if author not in Pokemon.pokemons:
        pokemon = Pokemon(author)
        pokemon.name = await pokemon.get_name()
        pokemon.ability = await pokemon.get_ability()

        await ctx.send(f"Pokémonunuzun ismi: {pokemon.name}\nYeteneği: {pokemon.ability}\nHP: {pokemon.hp}\nPower: {pokemon.power}")

        image_url = await pokemon.show_img()
        if image_url:
            embed = discord.Embed(title=f"{pokemon.name} - {pokemon.ability}")
            embed.set_image(url=image_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Pokémonun görüntüsü yüklenemedi!")
    else:
        await ctx.send("Zaten kendi Pokémonunuzu oluşturdunuz!")


@bot.command()
async def stat(ctx):
    author = ctx.author.name
    pokemon = Pokemon.pokemons.get(author)

    if pokemon:
        embed = await pokemon.stat_embed()
        await ctx.send(embed=embed)
    else:
        await ctx.send("Henüz bir Pokémon oluşturmadınız! `!go` ile başlayın.")


@bot.command()
async def reset(ctx):
    author = ctx.author.name
    if author in Pokemon.pokemons:
        del Pokemon.pokemons[author]
        await ctx.send("Pokémon sıfırlandı. `!go` ile yeni bir tane oluştur.")
    else:
        await ctx.send("Zaten bir Pokémonunuz yok.")


@bot.command()
async def attack(ctx):
    target = ctx.message.mentions[0] if ctx.message.mentions else None  # Mesajda belirtilen kullanıcıyı alırız
    if target:  # Kullanıcının belirtilip belirtilmediğini kontrol ederiz
        # Hem saldırganın hem de hedefin Pokémon sahibi olup olmadığını kontrol ederiz
        if target.name in Pokemon.pokemons and ctx.author.name in Pokemon.pokemons:
            enemy = Pokemon.pokemons[target.name]  # Hedefin Pokémon'unu alırız
            attacker = Pokemon.pokemons[ctx.author.name]  # Saldırganın Pokémon'unu alırız
            result = await attacker.attack(enemy)  # Saldırıyı gerçekleştirir ve sonucu alırız
            await ctx.send(result)  # Saldırı sonucunu göndeririz
        else:
            await ctx.send("Savaş için her iki tarafın da Pokémon sahibi olması gerekir!")  # Katılımcılardan birinin Pokémon'u yoksa bilgilendiririz
    else:
        await ctx.send("Saldırmak istediğiniz kullanıcıyı etiketleyerek belirtin.")  # Saldırmak için kullanıcıyı etiketleyerek belirtmesini isteriz
        


@bot.command()
async def feed(ctx):
    author = ctx.author.name
    if author in Pokemon.pokemons:
        pokemon = Pokemon.pokemons[author]
        response = await pokemon.feed()
        await ctx.send(response)
    else:
        await ctx.send("pokemon yok")


bot.run(token)

