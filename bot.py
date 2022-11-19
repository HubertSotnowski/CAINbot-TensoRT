import nextcord as discord
from nextcord.ext import commands
import os
import cv2
import subprocess
import platform
from ytdl import *
import cv2
from pyupload.uploader import *

import shutil
ossystem=platform.system()
print(ossystem)
###
##
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
###
@bot.command()
async def interpolate(ctx, arg1="--model",arg2="cvp", arg3="x", arg4="x"):
    '''interpolate your video\n 
       !interpolate --ytdl [URL] 
       !interpolate --url [URL]
       !interpolate [ADD ATTACHMENT] 
        select model by adding --model (name)'''
    url,ytdl,model_name,ytdlurl=False,False,"cvp",None
    
    ################  ################
    if arg1=="--model":
        model_name=arg2
    if arg3=="--model":
        model_name=arg4
    ################
    if arg1=="--ytdl":
        ytdlurl=arg2
        ytdl=True
        embedurl=arg2
    if arg3=="--ytdl":
        ytdlurl=arg4
        ytdl=True
        embedurl=arg4
    ##############
    if arg1=="--wget":
        urlname=arg2
        url=True
        embedurl=arg2
    if arg3=="--wget":
        urlname=arg4
        url=True
        embedurl=arg4
    ##############
    if arg1=="--discord" or arg3=="--discord":
        ytdl=False
        url=False
    #create embed
    embedVar = discord.Embed(title="CAIN BOT SETTINGS", description="", color=0xcc0000)
    embedVar.add_field(name="Model ", value=model_name, inline=False)
    embedVar.add_field(name="URL ", value=embedurl, inline=False)
    settingsm = await ctx.channel.send(embed=embedVar)
    
    message =  await ctx.send(content=f"Downloading video 📥\n")
    #download video
    print("kys")
    if url==False and ytdl==False:
        urlname = ctx.message.attachments[0].url
        url=True
    
    if ytdl:
        downloadvideo(ytdlurl,"input")
    else:
        downloadfromurl(urlname,"input.mkv")
        os.system("ffmpeg -i input.mkv -c:a copy -vn -y audio.mkv")
    video = cv2.VideoCapture(f"input.mkv")
    width  = int(video.get(cv2.CAP_PROP_FRAME_WIDTH)) 
    fps = video.get(cv2.CAP_PROP_FPS)
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))  
    frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    #update embed
    embedVar.add_field(name="Resolution ", value=f"{width}x{height}")
    embedVar.add_field(name="FPS ", value=f"from {fps} to {fps*2}", inline=False)
    embedVar.add_field(name="Frames ", value=round(frames), inline=False)
    await settingsm.edit(embed=embedVar)
    print("kys")
    #limit video to 10800frames
    if frames>10800:
        return None
    #interpolate and convert
    if os.path.isfile(f"{width}x{height}x{model_name}.engine"):
        await message.edit(content=f"Interpolating ⌛\n")
        shutil.copy(f"{width}x{height}x{model_name}.engine", "cain.engine")  
        os.system(f"vspipe -c y4m cain.vpy - | ffmpeg -i pipe: -y  -c:v h264_nvenc -qp 20 -y output.mkv")
        os.remove("cain.engine")
    else:
        message.edit(content=f"Converting model ⌛\n")
        os.system(f"python convert.py --input {model_name}.pth --height {height} --width {width} --output {width}x{height}x{model_name}.engine")
        shutil.copy(f"{width}x{height}x{model_name}.engine", "cain.engine")  
        message.edit(content=f"Interpolating ⌛\n")
        os.system(f"vspipe -c y4m cain.vpy - | ffmpeg -i pipe: -y  -c:v h264_nvenc -qp 20 -y output.mkv")
        os.remove("cain.engine")
    if os.path.isfile("audio.mkv"):
        os.system("ffmpeg -i output.mkv -i audio.mkv -c:v copy -b:a 256k output-audio.mkv")
        
    await message.edit(content=f"Finished interpolation!✨\n")
    #upload
    uploader_class =  CatboxUploader
    if os.path.isfile("audio.mkv"):
        uploader_instance = uploader_class(f"output-audio.mkv")
    else:
        uploader_instance = uploader_class(f"output.mkv")
    catboxurl = uploader_instance.execute()
    await ctx.send( content=f"{ctx.author.mention} {catboxurl}")
    os.remove("output.mkv")
    try:
        os.remove("audio.mkv")
        os.remove("output-audio.mkv")
    except:
        pass
bot.run("MTAzNTY3MzAyNTQxNDE4OTA1Nw.GiJe_B.H2ibKHDzaXbFTRqUhiZ6f2skH46gkfq6G83yCg")
