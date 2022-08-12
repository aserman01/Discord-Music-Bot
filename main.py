# -*- coding: utf-8 -*-

import discord
from discord.ext import commands
import youtube_dl
import os
from keep_alive import keep_alive
""""
import functools
import itertools
from async_timeout import timeout
"""

import nest_asyncio
nest_asyncio.apply()



client = commands.Bot(command_prefix="+")

#Gif
""""
@client.event
async def on_ready():
    for guild in client.guilds:
        for channel in guild.text_channels :
            if str(channel) == "bot" :
                await channel.send('Hey guys! Bot is active.')
                await channel.send(file=discord.File('bot_gif.gif'))
        print('Active in {}\n Member Count : {}'.format(guild.name,guild.member_count))
"""

#Müzik komutları

@client.command()
async def play(ctx, url : str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'clear' command")
        return

    voiceChannel = ctx.author.voice.channel
    
    if ctx.guild.voice_client in  client.voice_clients:
      pass
    else:
      await voiceChannel.connect()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            song_name = file
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))
    await ctx.send(">>> **Now playing **:musical_note:\n"+str(song_name)[:-16])


@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        await ctx.send("Paused ⏸️")
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")


@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        await ctx.send("Resuming ⏯️")
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")


@client.command()
async def clear(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()


        
#Shutdown

@client.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send("See you UwU")
    await ctx.bot.logout()


keep_alive()
client.run('...') # Put your own discord token here

