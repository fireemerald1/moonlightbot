import discord
from discord.ext import commands, tasks
import random
import supabase
import asyncio

# Gantilah 'YOUR_BOT_TOKEN' dengan token botmu
TOKEN = DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
SUPABASE_URL = 'https://ydwmwvzetpejltemygpj.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlkd213dnpldHBlamx0ZW15Z3BqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDE2ODE0NDYsImV4cCI6MjA1NzI1NzQ0Nn0.XFRV79t6CY1dODHHQt3-zLeIOnI9kNkc5hhKOSX4rsY'

# itialize Supabase
supabase_client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

# Set bot command prefix
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f'Bot {bot.user} is online!')

# Check if user has Moderator role
async def has_moderator_role(ctx):
    role_moderator = discord.utils.get(ctx.guild.roles, id=1226909672750059541)
    return role_moderator in ctx.author.roles if role_moderator else False

# Check if user has Admin role
async def has_admin_role(ctx):
    role_admin = discord.utils.get(ctx.guild.roles, id=1227279982435500032)
    return role_admin in ctx.author.roles if role_admin else False

# Command Kick
@bot.command(name="kick")
async def kick(ctx, member: discord.Member, *, reason=None):
    if not await has_moderator_role(ctx):
        await ctx.send("You do not have permission to use this command.")
        return
    await member.kick(reason=reason)
    await ctx.send(f'{member.name} has been kicked!')

# Command Ban
@bot.command(name="ban")
async def ban(ctx, member: discord.Member, *, reason=None):
    if not await has_moderator_role(ctx):
        await ctx.send("You do not have permission to use this command.")
        return
    await member.ban(reason=reason)
    await ctx.send(f'{member.name} has been banned!')

# Command Unban
@bot.command(name="unban")
async def unban(ctx, *, member_name):
    if not await has_moderator_role(ctx):
        await ctx.send("You do not have permission to use this command.")
        return
    banned_users = await ctx.guild.bans()
    for ban_entry in banned_users:
        user = ban_entry.user
        if user.name == member_name:
            await ctx.guild.unban(user)
            await ctx.send(f'{user.name} has been unbanned!')
            return
    await ctx.send(f'User {member_name} not found')

# Command Clear Messages
@bot.command(name="clear")
async def clear(ctx, amount: int):
    if not await has_moderator_role(ctx):
        await ctx.send("You do not have permission to use this command.")
        return
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f'{amount} messages have been deleted!', delete_after=3)

# Command Warn System
@bot.command(name="warn")
async def warn(ctx, member: discord.Member):
    if not await has_moderator_role(ctx):
        await ctx.send("You do not have permission to use this command.")
        return
    response = supabase_client.table("warns").select("jumlah").eq("nama", member.name).execute()
    warn_count = response.data[0]['jumlah'] + 1 if response.data else 1
    
    supabase_client.table("warns").upsert({"nama": member.name, "jumlah": warn_count}).execute()
    await ctx.send(f'{member.name} has received a warning! Total: {warn_count}')
    
    if warn_count == 5:
        await member.timeout(discord.utils.utcnow() + discord.timedelta(hours=3), reason="Received 5 warnings")
        await ctx.send(f'{member.name} has been muted for 3 hours!')
    elif warn_count == 7:
        await member.timeout(discord.utils.utcnow() + discord.timedelta(days=1), reason="Received 7 warnings")
        await ctx.send(f'{member.name} has been muted for 1 day!')
    elif warn_count >= 10:
        await member.ban(reason="Received 10 warnings")
        await ctx.send(f'{member.name} has been banned!')

# Command Edit Moderator Role (Admin Only)
@bot.command(name="edit_desc")
async def edit_desc(ctx, name: discord.Member, role: str, *, new_description):
    if not await has_admin_role(ctx):
        await ctx.send("You do not have permission to use this command.")
        return
    response = supabase_client.table("moderators").update({"role": role, "deskripsi": new_description}).eq("nama", name).execute()
    await ctx.send(f'Moderator {name} role and description have been updated!') if response.data else await ctx.send(f'Moderator {name} not found!')

@bot.command(name="add_mods")
async def add_mods(ctx, member: discord.Member, *, description):
    if not await has_admin_role(ctx):
        await ctx.send("You do not have permission to use this command.")
        return

    # Ambil semua ID yang ada di database
    response = supabase_client.table("moderators").select("id").execute()
    existing_ids = {entry["id"] for entry in response.data} if response.data else set()

    # Cari ID terkecil yang belum digunakan
    new_id = 1
    while new_id in existing_ids:
        new_id += 1  # Cari ID berikutnya yang tidak digunakan

    # Tambahkan peran Moderator ke user
    role_moderator = discord.utils.get(ctx.guild.roles, id=1226909672750059541)
    if role_moderator:
        await member.add_roles(role_moderator)

    # Masukkan data dengan ID yang baru
    supabase_client.table("moderators").insert({
        "id": new_id,
        "nama": member.name,
        "role": "Moderator",
        "deskripsi": description
    }).execute()

    await ctx.send(f'{member.name} has been added as a Moderator')
    
# Command Help (Displays all moderators, admins, owners)
@bot.command(name="modhelp")
async def modhelp(ctx):
    response = supabase_client.table("moderators").select("id, nama, role, deskripsi").order("id", desc=False).execute()
    if response.data:
        embed = discord.Embed(title="Moderator List", color=discord.Color.blue())
        for mod in response.data:
            embed.add_field(name=f'[{mod["id"]}] {mod["nama"]} - {mod["role"]}', value=mod["deskripsi"], inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send("No moderators registered yet.")


@bot.command(name="help")
async def custom_help(ctx):
    embed = discord.Embed(title="Bot Commands", description="Here are the available commands:", color=discord.Color.blue())
    
    embed.add_field(name="🔹 General Commands", value="`!help` - Show this message\n`!modhelp` - List of moderators", inline=False)
    embed.add_field(name="🔹 Moderator Commands", value="`!kick @user` - Kick a member\n`!ban @user` - Ban a member\n`!clear [number]` - Delete messages\n`!warn @user` - Warn a user", inline=False)
    embed.add_field(name="🔹 Admin Commands", value="`!add_mods @user [desc]` - Add a moderator\n`!edit_desc @user [role] [desc]` - Edit moderator role & description", inline=False)
    
    await ctx.send(embed=embed)

# Run the bot
bot.run(TOKEN)
