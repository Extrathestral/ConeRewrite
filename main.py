import discord
import datetime
from discord.ext import commands
from ifunnyBad import iFunnyFilter
from io import BytesIO
import urllib as urllib2
import re
from dotenv import load_dotenv
from PIL import Image
import os
from ifunnyScrape import getIFunnyMediaLink
from asyncio import sleep
ifunnyURLRE = r"(^| )(http|https)://ifunny.co/\S*( |$)"
bot = commands.Bot(command_prefix='>')
codyExempt = False
load_dotenv()
token = os.getenv('token')
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    if message.author.id == 821021462604677140:
        messages = await message.channel.history(limit=2).flatten()
        lastMessage = messages[-1]
        if lastMessage.author.id == 250797109022818305 and codyExempt:
            return
        # messageTS = datetime.datetime.timestamp(message.created_at)*1000
        # lastMessageTS = datetime.datetime.timestamp(lastMessage.created_at)*1000
        # if messageTS < lastMessageTS+500 and "mcfuck!" not in lastMessage.content.lower():
        #     await message.channel.set_permissions(message.author, send_messages=False)
        #     await message.delete()
        #     await sleep(1)
        #     await message.channel.set_permissions(message.author, send_messages=True)

    attachments = message.attachments
    if len(attachments) != 0:
        pic_ext = ['.jpg','.png','.jpeg']
        filename = attachments[0].filename
        for ext in pic_ext:
            if filename.endswith(ext):
                newImage = None
                with BytesIO() as image_binary:
                    await attachments[0].save(image_binary)
                    image_binary.seek(0)
                    print(attachments[0].url)
                    im = Image.open(image_binary)
                    newImage = iFunnyFilter(im)
                if newImage != None:
                    await message.delete()
                    with BytesIO() as image_binary:
                        newImage.save(image_binary, 'PNG')
                        image_binary.seek(0)
                        await message.channel.send("Fixed, "+message.author.mention, file=discord.File(fp=image_binary, filename='fixed.png'))
    if re.match(ifunnyURLRE,message.content):
        link = re.fullmatch(ifunnyURLRE,message.content).string
        await message.delete()
        await message.channel.send("Fixed, "+message.author.mention+"\n"+getIFunnyMediaLink(link))
    if message.author.bot:
        return
    await bot.process_commands(message)

@bot.command()
async def tinyPPShortManGodExempt(message, boolValue):
    global codyExempt
    if not boolValue:
        await message.channel.send(f"Value is {codyExempt}")
        return
    try:
        codyExempt = bool(boolValue)
        await message.channel.send(f"k, value is now {codyExempt}")
    except:
        await message.channel.send("Invalid Input")

@bot.command()
async def say(message, *text):
    if message.author.id != 181824790078685184:
        await message.channel.send("no.")
        return
    if text:
        await message.channel.send(" ".join(text))


bot.run(token)
