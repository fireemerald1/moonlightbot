import discord
from discord.ext import commands, tasks
import random
import supabase
import asyncio
import os

# Gantilah 'YOUR_BOT_TOKEN' dengan token botmu
TOKEN = DISCORD_TOKEN = os.getenv"DISCORD_TOKEN"
SUPABASE_URL = 'uh... no ig'
SUPABASE_KEY = 'balls'

# itialize Supabase
supabase_client = supabase.create_clientSUPABASE_URL, SUPABASE_KEY

# Set bot command prefix
intents = discord.Intents.default
intents.messages = True
intents.guilds = True
intents.members = True
intents.message_content = True

bot = commands.Botcommand_prefix='!', intents=intents, help_command=None

@bot.event
async def on_ready:
    printf'Bot {bot.user} is online!'

# Check if user has Moderator role
async def has_moderator_rolectx:
    role_moderator = discord.utils.getctx.guild.roles, id=1226909672750059541
    return role_moderator in ctx.author.roles if role_moderator else False

# Check if user has Admin role
async def has_admin_rolectx:
    role_admin = discord.utils.getctx.guild.roles, id=1227279982435500032
    return role_admin in ctx.author.roles if role_admin else False

# Command Kick
@bot.commandname="kick"
async def kickctx, member: discord.Member, *, reason=None:
    if not await has_moderator_rolectx:
        await ctx.send"You do not have permission to use this command."
        return
    await member.kickreason=reason
    await ctx.sendf'{member.name} has been kicked!'

# Command Ban
@bot.commandname="ban"
async def banctx, member: discord.Member, *, reason=None:
    if not await has_moderator_rolectx:
        await ctx.send"You do not have permission to use this command."
        return
    await member.banreason=reason
    await ctx.sendf'{member.name} has been banned!'

# Command Unban
@bot.commandname="unban"
async def unbanctx, *, member_name:
    if not await has_moderator_rolectx:
        await ctx.send"You do not have permission to use this command."
        return
    banned_users = await ctx.guild.bans
    for ban_entry in banned_users:
        user = ban_entry.user
        if user.name == member_name:
            await ctx.guild.unbanuser
            await ctx.sendf'{user.name} has been unbanned!'
            return
    await ctx.sendf'User {member_name} not found'

# Command Clear Messages
@bot.commandname="clear"
async def clearctx, amount: int:
    if not await has_moderator_rolectx:
        await ctx.send"You do not have permission to use this command."
        return
    await ctx.channel.purgelimit=amount + 1
    await ctx.sendf'{amount} messages have been deleted!', delete_after=3

# Command Warn System
@bot.commandname="warn"
async def warnctx, member: discord.Member:
    if not await has_moderator_rolectx:
        await ctx.send"You do not have permission to use this command."
        return
    response = supabase_client.table"warns".select"jumlah".eq"nama", member.name.execute
    warn_count = response.data[0]['jumlah'] + 1 if response.data else 1

    supabase_client.table"warns".upsert{"nama": member.name, "jumlah": warn_count}.execute
    await ctx.sendf'{member.name} has received a warning! Total: {warn_count}'

    if warn_count == 5:
        await member.timeoutdiscord.utils.utcnow + discord.timedeltahours=3, reason="Received 5 warnings"
        await ctx.sendf'{member.name} has been muted for 3 hours!'
    elif warn_count == 7:
        await member.timeoutdiscord.utils.utcnow + discord.timedeltadays=1, reason="Received 7 warnings"
        await ctx.sendf'{member.name} has been muted for 1 day!'
    elif warn_count >= 10:
        await member.banreason="Received 10 warnings"
        await ctx.sendf'{member.name} has been banned!'

# Command Edit Moderator Role Admin Only
@bot.commandname="edit_desc"
async def edit_descctx, name: discord.Member, role: str, *, new_description:
    if not await has_admin_rolectx:
        await ctx.send"You do not have permission to use this command."
        return
    response = supabase_client.table"moderators".update{"role": role, "deskripsi": new_description}.eq"nama", name.execute
    await ctx.sendf'Moderator {name} role and description have been updated!' if response.data else await ctx.sendf'Moderator {name} not found!'

@bot.commandname="add_mods"
async def add_modsctx, member: discord.Member, *, description:
    if not await has_admin_rolectx:
        await ctx.send"You do not have permission to use this command."
        return

    # Ambil semua ID yang ada di database
    response = supabase_client.table"moderators".select"id".execute
    existing_ids = {entry["id"] for entry in response.data} if response.data else set

    # Cari ID terkecil yang belum digunakan
    new_id = 1
    while new_id in existing_ids:
        new_id += 1  # Cari ID berikutnya yang tidak digunakan

    # Tambahkan peran Moderator ke user
    role_moderator = discord.utils.getctx.guild.roles, id=1226909672750059541
    if role_moderator:
        await member.add_rolesrole_moderator

    # Masukkan data dengan ID yang baru
    supabase_client.table"moderators".insert{
        "id": new_id,
        "nama": member.name,
        "role": "Moderator",
        "deskripsi": description
    }.execute

    await ctx.sendf'{member.name} has been added as a Moderator'

# Command Help Displays all moderators, admins, owners
@bot.commandname="modhelp"
async def modhelpctx:
    response = supabase_client.table"moderators".select"id, nama, role, deskripsi".order"id", desc=False.execute
    if response.data:
        embed = discord.Embedtitle="Moderator List", color=discord.Color.blue
        for mod in response.data:
            embed.add_fieldname=f'[{mod["id"]}] {mod["nama"]} - {mod["role"]}', value=mod["deskripsi"], inline=False
        await ctx.sendembed=embed
    else:
        await ctx.send"No moderators registered yet."


@bot.commandname="help"
async def custom_helpctx:
    embed = discord.Embedtitle="Bot Commands", description="Here are the available commands:", color=discord.Color.blue

    embed.add_fieldname="🔹 General Commands", value="`!help` - Show this message\n`!modhelp` - List of moderators", inline=False
    embed.add_fieldname="🔹 Moderator Commands", value="`!kick @user` - Kick a member\n`!ban @user` - Ban a member\n`!clear [number]` - Delete messages\n`!warn @user` - Warn a user", inline=False
    embed.add_fieldname="🔹 Admin Commands", value="`!add_mods @user [desc]` - Add a moderator\n`!edit_desc @user [role] [desc]` - Edit moderator role & description", inline=False

    await ctx.sendembed=embed

# Run the bot
bot.runTOKEN
