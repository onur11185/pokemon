import aiohttp  
import random
import discord

class MyPokemon:
    pokemons = {}
    total = 0

    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1000)
        self.name = None
        self.hp = 100
        self.power = random.randint(10, 30)
        self.level = 1
        self.ability = None
        MyPokemon.total += 1

        if pokemon_trainer not in MyPokemon.pokemons:
            MyPokemon.pokemons[pokemon_trainer] = self


    async def stats(self):
        return (
            f"Trainer: {self.pokemon_trainer}\n"
            f"Level: {self.level}\n"
            f"HP: {self.hp}\n"
            f"Attack: {self.power}"
        )
    
    async def get_name(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  
        async with aiohttp.ClientSession() as session:  
            async with session.get(url) as response:  
                if response.status == 200:
                    data = await response.json()  
                    return data['forms'][0]['name']  
                else:
                    return "Pikachu"  

        

    async def show_img(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    image_url = data["sprites"]["front_default"]
                    return image_url if image_url else None
                else:
                    return "başarısız"
                

    async def get_ability(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    abilities = data['abilities']
                    if abilities:
                        return abilities[0]['ability']['name']  
                return "Unknown"

    async def stat_embed(self):
        embed = discord.Embed(title=f"{self.name} - Level {self.level}", description=f"Trainer: {self.pokemon_trainer}")
        embed.add_field(name="HP", value=str(self.hp), inline=True)
        embed.add_field(name="Power", value=str(self.power), inline=True)
        embed.add_field(name="Ability", value=self.ability or "Unknown", inline=True)
        img_url = await self.show_img()
        if img_url:
            embed.set_image(url=img_url)
        return embed
    

    async def attack(self, enemy):
        if isinstance(self,Wizard):
            chance = random.randint(1,15)
            if chance == 1:
                return "sihirbaz pokemon savaşta bir kalkan kullandı"
            
            if enemy.hp > self.power:
                enemy.hp -= self.power
                return f"Pokemon eğitmeni @{self.pokemon_trainer} @{enemy.pokemon_trainer}'ne saldırdı"
            
            else:
                enemy.hp = 0
                return f"Pokemon eğitmeni @{self.pokemon_trainer} @{enemy.pokemon_trainer}'nı yendi"


class Wizard(MyPokemon):
    pass


class Fighter(MyPokemon):
    async def attack(self, enemy):
        super_power = random.randint(5,15)
        self.power += super_power
        result = await super().attack(enemy)
        self.power -= super_power
        return result + f"\nDövüşçü Pokemon süper saldırı kullandı. Eklenen güç {super_power}"