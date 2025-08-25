# Initialization
import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import csv
import os

# Creating a list with all the swears from the CSV files given, possible to add if needed
swears = []
for filename in os.listdir('Swear/'):
    with open(os.path.join('Swear/', filename), newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
        swears.append(data)

load_dotenv()

# Taking the token from the .env file to connect the bot
token = os.getenv("DISCORD_TOKEN")

#Intents are the options that you can enable, for more informations look at the bot's dashbord pannel on discord developer website
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.message_content = True

# Choosing the prefix to use for the bot
bot = commands.Bot(command_prefix='!', intents=intents)


# Sending a message when the bot is ready to be used
@bot.event
async def on_ready():
    """
    in : the bot is ready
    out : Bot is ready message
    """
    print(f"Im ready, {bot.user.name}")


# Welcoming message when a user joins the server
@bot.event
async def on_member_join(member):
    """
    in : a member that joined
    out : Welcome message
    """
    bonjour_aurevoir=1409526596905467925
    channel=bot.get_channel(bonjour_aurevoir)

    await channel.send(f"{member.name} has joined the server")
    await member.send(f"Welcome {member.name} to the server {member.guild.name}!")


# Goodbye message when a user leaves the server
@bot.event
async def on_member_remove(member):
    """
    in : a member that left
    out : Goodbye message
    """
    bonjour_aurevoir=1409526596905467925
    channel=bot.get_channel(bonjour_aurevoir)
    id = member.id
    await channel.send(f"{member.name} has left the server :'(")

# Hello command
@bot.command()
async def hello(ctx):
    """
    in : !hello
    out : Goodbye
    """
    if ctx.channel.id == 1409527307239948410:  # id of the bot only channel
        await ctx.send("Goodbye")
    else:
        await ctx.message.delete()
        await ctx.send(f"Sorry {ctx.author.mention}, you cannot send messages in this channel, please do so in the <#1409527307239948410> channel.")

# Clear command
@bot.command()
async def clear(ctx, number: int):
    """
    in : !clear <number>
    out : Deletes <number> messages
    """
    if ctx.author.guild_permissions.administrator: #if user is admin on the server
        await ctx.channel.purge(limit=number) #delete the last <number> messages
        await ctx.send(f"I deleted {number} messages.")
    else:
        await ctx.message.delete()
        await ctx.send(f"Sorry {ctx.author.mention}, you do not have permission to use this command.")

# Profanity filter
@bot.event
async def on_message(message):
    """
    in : a message
    out : the same message if it passes the filter else None
    """
    if message.author == bot.user:
        return

    if message.content.startswith('!'): #the commands are not filtered
        await bot.process_commands(message)
        return
    
    #go through the swear words and compare with the message content
    for table in swears:
        for row in table:
            for word in row:
                if word.lower() in message.content.lower():
                    await message.delete()
                    await message.channel.send(f"{message.author.mention}, merci de rester poli.")
                    return
                      
    await bot.process_commands(message)

# Mute command
@bot.command()
async def mute(ctx, member: discord.Member):
    """
    in : !mute <user>
    out : Mutes a user
    """
    if ctx.author.guild_permissions.administrator: #if user has the admin perms
        if member is None:  #if member does not exists
            await ctx.send("Please mention a user that exists.")
            return
        else:
            role = discord.utils.get(ctx.guild.roles, name="muted")
            if role: #if the role exists
                await member.add_roles(role)
                await ctx.send(f"{member.mention} has been assigned the muted role.")
            else:
                role = await ctx.guild.create_role(name="muted", colour=discord.Colour(000000))
                await member.add_roles(role)
                await ctx.send(f"{member.mention} has been assigned the muted role.")
    else:
        await ctx.send(f"Sorry {ctx.author.mention}, you do not have permission to use this command.")

# Unmute command
@bot.command()
async def unmute(ctx, member: discord.Member):
    """
    in : !unmute <user>
    out : Unmutes a user
    """
    if ctx.author.guild_permissions.administrator: #if user has the admin perms
        role = discord.utils.get(ctx.guild.roles, name="muted")
        if role: #if the role exists
            await member.remove_roles(role)
            await ctx.send(f"{member.mention} has been unmuted.")
        else:
            await ctx.send(f"{member.mention} is not muted.")
    else:
        await ctx.send(f"Sorry {ctx.author.mention}, you do not have permission to use this command.")

# Ban command
@bot.command()
async def ban(ctx, member: discord.Member):
    """
    in : !ban <user>
    out : Bans a user
    """
    if ctx.author.guild_permissions.administrator: #if user has the admin perms
        await ctx.send("Please provide a reason for the ban :")
        reason = await bot.wait_for("message", check=lambda msg: msg.author == ctx.author) #wait for the user's response
        await member.ban(reason=reason.content)
        await ctx.send(f"{member.mention} has been banned.")
    else:
        await ctx.send(f"Sorry {ctx.author.mention}, you do not have permission to use this command.")

# Kick command
@bot.command()
async def kick(ctx, member: discord.Member):
    """
    in : !kick <user>
    out : Kicks a user
    """
    if ctx.author.guild_permissions.administrator: #if user has the admin perms
        await member.kick()
        await ctx.send(f"{member.mention} has been kicked.")
    else:
        await ctx.send(f"Sorry {ctx.author.mention}, you do not have permission to use this command.")

# Making the bot run with the token saw previously
bot.run(token)
