import os
# IMPORT DOTENV
from dotenv import load_dotenv
# LOAD DOTENV
load_dotenv()
# SET DISCORD TOKEN
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
import discord
from discord.ext import commands
from random import *
# ======= MODIFIER =======
credit = 0
sacCreditTaken = False
RETURNVALUE = 1
luckMultiplier = 1
cycle = 999999999999999999999999999
sacAmount = 0
# =======================

rarityNames = ['Common', 'Uncommon', 'Rare', 'Epic', 'Legendary', 'Mythic', 'Ultra', 'Super', 'Omega', 'Fabled', 'Divine', 'Supreme', 'Omnipotent', 'Astral', 'Celestial', 'Seraphic', 'Transcendent', 'Quantum', 'Galactic', 'Eternal', 'cHa0s', 'Quantum Shard']
rarityCredits = [-5, 1, 2, 5, 10, 25, 100, 250, 1000, 2500, 10000, 25000, 100000, 250000, 1000000, 2500000, 10000000, 25000000, 100000000, 250000000, 1000000000, 10**20]

mobType = ['Ladybug', 'Bee', 'Hornet', 'Spider', 'Baby Ant', 'Worker Ant', 'Soldier Ant', 'Queen Ant', 'Ant Burrow', 'Dandelion', 'Rock', 'Centipede', 'Evil Centipede', 'Dark Ladybug', 'Beetle', 'Scorpion', 'Cactus', 'Sandstorm', 'Fire Ant Burrow', 'Fire Ant', 'Fire Queen Ant', 'Desert Centipede', 'Locust', 'Desert Moth', 'Shiny Ladybug', 'Crab', 'Jellyfish', 'Shell', 'Starfish', 'Sponge', 'Leech', 'Sea Urchin', 'Bubble', 'Plastic', 'Square', 'Evil Desert Centipede', 'Pentagon', 'H͏̀͏E̸̵̷̡̛͞͠X̢́͢͡͠Á̵̧̧́̕͝G҉̨̛͞OǸ͘͜͟͏']
mobMulti = [1, 1.5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1, -1, 1, 1, 1, 1.5, 1, 1, 2, 1.5, 1, 1, 5, 1, 1, 1.5, 1, 1, 1, 1, 1, 3, 10, -2, 100, -666]

AUTHORIZED_USERS = [
    1185855185327763517, 1041613194382286878, 1200672063711612969, 1198052229513486358
]
# Colors for each rarity
rarityColors = [
    0x85e066,  # Common
    0xf3d859,  # Unusual
    0x5b5bca,  # Rare
    0x8d2ec7,  # Epic
    0xd72e23,  # Legendary
    0x1fdbde,  # Mythic
    0xff2b75,  # Ultra
    0x2bffa3,  # Super
    0x484848,  # Omega
    0xff5500,  # Fabled
    0x67549c,  # Divine
    0xb15ed9,  # Supreme
    0x888888,  # Omnipotent
    0x056308,  # Astral
    0x00bffe,  # Celestial
    0xc87e5c,  # Seraphic
    0xffffff,  # Transcendent
    0x61ffde,  # Quantum
    0xba607a,  # Galactic
    0x5a8c7d,  # Eternal
    0x20258a,  # cHa0s
]

# Bot setup
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='!',
                   intents=intents,
                   case_insensitive=True)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

# Global variable to save the last sacrificer
lastSacrificer = None

@bot.command(name='sac')
async def sac(ctx, amount: int):
    global sacAmount, luckMultiplier, cycle, lastSacrificer
    sacAmount = float(amount)
    luckMultiplier = max(0.207125*(2.34915*sacAmount+463.458)**0.5-4.48083, 1)

    if sacAmount >= 100 and sacAmount < 1000:
        cycle = 3
    elif sacAmount >= 1000 and sacAmount < 10000:
        cycle = 12
    elif sacAmount >= 10000 and sacAmount < 100000:
        cycle = 20
    elif sacAmount >= 100000 and sacAmount < 1000000:
        cycle = 25
    else:
        cycle = 30

    # Save the sacrificer's name
    lastSacrificer = ctx.author.mention

    embed = discord.Embed(
        title="The Flowr Gods Heed Your Sacrifice . . .",
        description=f"A **{round(luckMultiplier, 1)}x Luck Frenzy** has been activated, and will apply to the next {cycle} spins!",
        color=0xFFFF00  # Yellow color for sac embed
    )

    embed.add_field(name="Sacrificed Social Credit", value=f"{sacAmount:,}", inline=False)
    embed.add_field(name="Successful Sacrifice", value=f"{ctx.author.mention} now has **???** credits!", inline=False)
    await ctx.send(embed=embed)


@bot.command(name='spin')
async def spin(ctx):
    global credit, sacCreditTaken, cycle, luckMultiplier, lastSacrificer

    if cycle <= 0:
        await ctx.send("No active luck frenzy! Use `!sac` first.")
        return


    randomValue = random()
    rng = randomValue / luckMultiplier - 1 * 1 + 1
    rarity = 0

    if rng < 0.55:
        rarity += 1
    if rng < 0.35:
        rarity += 1
    if rng < 0.2:
        rarity += 1
    if rng < 0.1:
        rarity += 1
    if rng < 0.05:
        rarity += 1
    if rng < 0.02:
        rarity += 1
    if rng < 0.01:
        rarity += 1
    if rng < 0.005:
        rarity += 1
    if rng < 0.0025:
        rarity += 1
    if rng < 0.001:
        rarity += 1
    if rng < 0.00044:
        rarity += 1
    if rng < 0.00014:
        rarity += 1
    if rng < 0.00004:
        rarity += 1
    if rng < 0.00001:
        rarity += 1
    if rng < 0.000004:
        rarity += 1
    if rng < 0.000001:
        rarity += 1
    if rng < 0.0000004:
        rarity += 1
    if rng < 0.0000001:
        rarity += 1
    if rng < 0.00000004:
        rarity += 1
    if rng < 0.00000001:
        rarity += 1
    if rng == 0:
        rarity += 1

    mobNum = randint(0, len(mobType) - 3)
    if random() < 0.001:
        mobNum = len(mobType) - 2
    if random() < 0.0002 and rarity >= 8:
        mobNum = len(mobType) - 1

    # Calculate the credit gain
    multiplier = mobMulti[mobNum]
    creditGain = round(rarityCredits[rarity] * multiplier)
    credit += round(RETURNVALUE * creditGain)

    embed = discord.Embed(
        title=f"{rarityNames[rarity]} {mobType[mobNum]}",
        description=f"You got a **{rarityNames[rarity]} {mobType[mobNum]}**!",
        color=rarityColors[rarity]  # Color depends on rarity
    )


    # Add FRENZY section
    frenzy_text = f"{luckMultiplier:.1f}x luck from {lastSacrificer}'s sacrifice!" if lastSacrificer else "No active frenzy."
    embed.add_field(
        name="FRENZY",
        value=frenzy_text,
        inline=False
    )


    # Add Evil Mob Multiplier if the multiplier is negative
    if multiplier < 0:
        embed.add_field(
            name="Evil Mob Multiplier!",
            value=f"x{multiplier}",
            inline=False
        )


    # Rarity emojis (indexed to match rarityNames)
    rarityEmojis = [
        "<:rarity00_Common:1532939862544482324>",       # Common
        "<:rarity01_Unusual:1532939864742297721>",      # Uncommon
        "<:rarity02_Rare:1532939867032653988>",         # Rare
        "<:rarity03_Epic:1532939857683550388>",         # Epic
        "<:rarity04_Legendary:1532939860220969050>",    # Legendary
        "<:rarity05_Mythic:1532939850481930300>",       # Mythic
        "<:rarity06_Ultra:1532939852939661504>",        # Ultra
        "<:rarity07_Super:1532939855288471622>",        # Super
        "<:rarity08_Omega:1532939843489890366>",        # Omega
        "<:rarity09_Fabled:1532939846023118848>",       # Fabled
        "<:rarity10_Divine:1532939848539832380>",       # Divine
        "<:rarity11_Supreme:1532939838804852806>",      # Supreme
        "<:rarity12_Omnipotent:1532939841124171847>",   # Omnipotent
        "<:rarity13_Astral:1532939832580640828>",       # Astral
        "<:rarity14_Celestial:1532939834409095260>",    # Celestial
        "<:rarity15_Seraphic:1532939836934066286>",     # Seraphic
        "<:rarity16_Transcendent:1532939825840128000>", # Transcendent
        "<:rarity17_Ethereal:1532939828297990195>",     # Quantum
        "<:rarity18_Galactic:1532939830432891043>",     # Galactic
        "<:rarity19_Eternal:1532939818965663794>",      # Eternal
        "<:rarity23_Chaos:1532939816499548331>",        # cHa0s
        "<:rarity20_Apotheotic:1532939820916015208>",   # Quantum Shard
    ]

    # Add Social Credit section
    rarity_emoji = rarityEmojis[rarity]
    ohno = "<:ohno:1532954047357653062>" if creditGain < 0 else ""
    sign = "+" if creditGain > 0 else ""
    embed.add_field(
        name=f"{sign}{creditGain:,} SOCIAL CREDIT 🎰 {ohno}",
        value=f"{rarityCredits[rarity]:,} {rarity_emoji} x{multiplier} ({mobType[mobNum]})",
        inline=False
    )


    await ctx.send(embed=embed)

    # Decrease the cycle count and reset if necessary
    cycle -= 1
    if cycle <= 0:
        luckMultiplier = 1
        lastSacrificer = None  # Clear the sacrificer
        await ctx.send("Luck Frenzy ended!")


@bot.command(name="tax")
async def tax(ctx, credit: int):
    # Calculate tax, subtracted credit, and transferred credit rounded to nearest integer
    tax = round(credit * 0.1)
    subtracted_credit = credit + tax
    transferred_credit = credit

    # Create the response message
    response = (
        f"Tax = {tax}\n"
        f"Credit subtracted = {subtracted_credit}\n"
        f"Credit transferred = {transferred_credit}"
    )

    # Send the response to the Discord channel
    await ctx.send(response)

@bot.command(name='debug')
async def debug(ctx):
    rarity_data = [
        {"name": "Common", "chance": "45.0%", "color": 0x85e066},
        {"name": "Unusual", "chance": "20.0%", "color": 0xf3d859},
        {"name": "Rare", "chance": "15.0%", "color": 0x5b5bca},
        {"name": "Epic", "chance": "10.0%", "color": 0x8d2ec7},
        {"name": "Legendary", "chance": "5.0%", "color": 0xd72e23},
        {"name": "Mythic", "chance": "3.0%", "color": 0x1fdbde},
        {"name": "Ultra", "chance": "1.0%", "color": 0xff2b75},
        {"name": "Super", "chance": "0.5%", "color": 0x2bffa3},
        {"name": "Omega", "chance": "0.25%", "color": 0x484848},
        {"name": "Fabled", "chance": "0.1%", "color": 0xff5500},
        {"name": "Divine", "chance": "0.05%", "color": 0x67549c},
        {"name": "Supreme", "chance": "0.03%", "color": 0xb15ed9},
        {"name": "Omnipotent", "chance": "0.01%", "color": 0x888888},
        {"name": "Astral", "chance": "0.003%", "color": 0x056308},
        {"name": "Celestial", "chance": "0.001%", "color": 0x00bffe},
        {"name": "Seraphic", "chance": "0.0003%", "color": 0xc87e5c},
        {"name": "Transcendent", "chance": "0.0001%", "color": 0xffffff},
        {"name": "Quantum", "chance": "0.00003%", "color": 0x61ffde},
        {"name": "Galactic", "chance": "0.00001%", "color": 0xba607a},
        {"name": "Eternal", "chance": "0.000003%", "color": 0x5a8c7d},
        {"name": "cHa0s", "chance": "0.000001%", "color": 0x20258a},
    ]

    for rarity in rarity_data:
        embed = discord.Embed(
            title=f"Rarity: {rarity['name']}",
            description=f"Chance: {rarity['chance']}",
            color=rarity["color"]
        )

        await ctx.send(embed=embed)

random_words = ["scammer",
                 "pls bioevent",
                 "beggar",
                 "pls carry me",
                 "ayoub fan",
                 "ayoub bigest fan",
                 "fire exe, pls ban me",
                 "fire exe hater",
                 "CASE OH 2.0",
                 "im gay",
                 "local femboy",
                 "im a furry :3",
                 "pls banish me"]

@bot.command(name="owoify")
@commands.has_permissions(administrator=True)
async def owoify(ctx, user: discord.Member):
    if ctx.author.id not in AUTHORIZED_USERS:
        await ctx.send("You are not authorized to use this command.")
        return
    original_text = user.display_name

    if random.choice([True, False]):
        owoified_text = original_text.replace('r', 'w').replace('R', 'W')
    else:
        additions = ["owo", ":3", "nyaa~~", "femboy", "furry", "please fuck me"]
        owoified_text = original_text + " " + random.choice(additions)

    try:
        await user.edit(nick=owoified_text)
        embed = discord.Embed(
            title="OwOify",
            description=f"{user.mention}, your nickname has been changed to: **{owoified_text}**",
            color=discord.Color.purple()
        )

        await ctx.send(embed=embed)
    except discord.Forbidden:
        await ctx.send("I do not have permission to change this user's nickname.")
    except discord.HTTPException as e:
        await ctx.send(f"An error occurred while trying to change the nickname: {e}")


@bot.command(name="change_name")
@commands.has_permissions(administrator=True)
async def change_name(ctx, member: discord.Member):
    if ctx.author.id not in AUTHORIZED_USERS:
        await ctx.send("You are not authorized to use this command.")
        return
    new_nickname = random.choice(random_words)

    try:
        await member.edit(nick=new_nickname)
        embed = discord.Embed(
            title="Nickname Changed",
            description=f"{member.mention}'s nickname has been changed to **{new_nickname}**",
            color=discord.Color.gold()
        )

        await ctx.send(embed=embed)
    except discord.Forbidden:
        await ctx.send("I don't have permission to change that user's nickname.")
    except discord.HTTPException as e:
        await ctx.send(f"An error occurred: {e}")

ROLE_ID = 1226909672750059541

@bot.command(name='promote')
async def promote_command(ctx, member: discord.Member):
    if ctx.author.id in AUTHORIZED_USERS:
        role = discord.utils.get(ctx.guild.roles, id=ROLE_ID)
        if role:
            await member.add_roles(role)
            await ctx.send(
                f'{member.mention} has been given the role {role.name}.'
            )
        else:
            await ctx.send('Role not found.')
    else:
        await ctx.send('You are not choosen to use this command.')


@bot.command(name='demote')
async def demote_command(ctx, member: discord.Member):
    if ctx.author.id in AUTHORIZED_USERS:
        role = discord.utils.get(ctx.guild.roles, id=ROLE_ID)
        if role:

            await member.remove_roles(role)
            await ctx.send(
                f'{member.mention} has had the role {role.name} removed.'
            )
        else:
            await ctx.send('Role not found.')
    else:
        await ctx.send('You are not choosen to use this command.')



ROLE_ID = 1232786203749646357

@bot.command(name='be_monke')
async def be_monke_command(ctx, member: discord.Member):
    if ctx.author.id in AUTHORIZED_USERS:
        role = discord.utils.get(ctx.guild.roles, id=ROLE_ID)
        if role:
            await member.add_roles(role)
            await ctx.send(
                f'{member.mention} has been given the role {role.name}.'
            )
        else:
            await ctx.send('Role not found.')
    else:
        await ctx.send('You are not choosen to use this command.')


@bot.command(name='no_monke')
async def no_monke_command(ctx, member: discord.Member):
    if ctx.author.id in AUTHORIZED_USERS:
        role = discord.utils.get(ctx.guild.roles, id=ROLE_ID)
        if role:

            await member.remove_roles(role)
            await ctx.send(
                f'{member.mention} has had the role {role.name} removed.'
            )
        else:
            await ctx.send('Role not found.')
    else:
        await ctx.send('You are not choosen to use this command.')


bot.run(DISCORD_TOKEN)
