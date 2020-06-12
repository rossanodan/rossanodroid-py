import os
import random
import discord
import requests

from discord.ext import commands
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv

from Brain import Brain

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = commands.Bot(command_prefix="!")


@client.event
async def on_ready():
    activity = discord.Game(name="with humans")
    status = discord.Status.online
    guild = discord.utils.get(client.guilds, name=GUILD)
    channel = discord.utils.get(guild.channels, name="general")
    wave = ":wave:"
    await client.change_presence(activity=activity, status=status)
    await channel.send(f'Hello, there {wave}')


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )


@client.command(name='analyze')
async def on_message(context):
    # manage if context.message.attachments is empty
    image_url = context.message.attachments[0].url
    # improve image format detection
    image_format_jpg = image_url[-3:]
    image_format_jpeg = image_url[-4:]
    if image_format_jpg.lower() == 'jpg' or image_format_jpeg.lower() == 'jpeg':
        try:
            brain = Brain()
            results = brain.analyze_image(image_url)[0]
            message = discord.Embed(
                title="Let's have a look..")
            for statistic in results:
                name = statistic[1]
                value = f'{round(statistic[2] * 100, 2)} %'
                message.add_field(name=name, value=value, inline=False)
            message.set_image(url=image_url)
            message.colour = 0x00ff00
            await context.message.channel.send(embed=message)
        except:
            error = discord.Embed(
                title="Ops.. Something went wrong", description="I'm sorry, something went wrong. Please, try again.")
            error.colour = 0xff0000
            await context.message.channel.send(embed=error)
            raise discord.DiscordException
    else:
        invalid_format = discord.Embed(
            title="Invalid format", description="I'm sorry, this format is not supported. Please, try again with a .jpg or .jpeg!")
        invalid_format.colour = 0xff0000
        await context.message.channel.send(embed=invalid_format)

client.run(TOKEN)
