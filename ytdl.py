import yt_dlp
import os.path
import requests
def downloadvideo(url,name):

    ydl_opts = {
        'outtmpl': name,
        # ℹ️ See help(yt_dlp.
        # postprocessor) for a list of available Postprocessors and their arguments
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegCopyStream',
        }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download(url)
        print(error_code)
        if os.path.isfile(name+".webm"):
            print("webm") 
            os.system(f"ffmpeg -i {name}.webm -c copy -y {name}.mkv")
            os.remove(name+".webm")
        else:
            try:
                os.system(f"ffmpeg -i {name}.mp4 -c copy -y {name}.mkv")
                os.remove(name+".mp4")
            except:
                print("failed to download video")
                pass
def downloadfromurl(url,name):
    response = requests.get(url)
    filesize=requests.get(url, stream=True).headers['Content-length']
    if int(filesize)>500000000:
        print("too big!!!!")
        return "too big!!!!"   
        
    open(name, "wb").write(response.content)