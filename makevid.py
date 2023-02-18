from moviepy.editor import *
import random
import os
from PIL import Image
from pytube import YouTube

img_path = 'static/ss_imgs'

def resize_imgs():
    #rpath = 'static/ss_resized'
    paths = os.listdir(img_path)
    for i in range(len(paths)):
        b = Image.new('RGBA', (720, 1280), (255, 0, 0, 0))
        p = img_path+'/'+paths[i]
        basewidth = 620
        img = Image.open(p)
        wpercent = (basewidth/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((basewidth,hsize), Image.ANTIALIAS)
        y = 640 - hsize//2
        i1 = img.convert('RGBA')
        b.paste(i1,(50,y))
        b.save(p)

def make_aud_clip(path1,path2):
    clip = ImageClip(path1)
    audio_clip = AudioFileClip(path2)
    clip = clip.set_duration(audio_clip.duration)
    dur = audio_clip.duration
    clip = clip.set_audio(audio_clip)
    fps = 1/dur
    return clip,fps,dur

def durs_check(vidlist,durl):
    while len(vidlist)>2:
        if sum(durl)>58:
            del vidlist[-1]
            del durl[-1]
            durs_check(vidlist,durl)
        else:
            return vidlist,durl

def make_vidlist():
    #resize_imgs()
    respaths = [f'{img_path}/{i}' for i in os.listdir(img_path)]
    audpaths = [f'static/ss_audioes/{i}' for i in os.listdir('static/ss_audioes/')]
    if len(respaths)==len(audpaths):
        vidlist,fpsl,durl=[],[],[]
        for i in range(len(respaths)):
            vf = make_aud_clip(respaths[i],audpaths[i])
            vidlist.append(vf[0])
            fpsl.append(vf[1])
            durl.append(vf[2])
    if sum(durl)>60:
        #del vidlist[-1]
        #del durl[-1]
        durs_check(vidlist,durl)
    print(durl,sum(durl))
    return vidlist,durl

def back_vid(s,e):
    yt_url = "https://www.youtube.com/watch?v=n_Dv4JMiwK8"
    vid = YouTube(yt_url)
    stream_url = vid.streams.get_by_itag(308).url
    #print(vid.streams.all,vid.streams.get_highest_resolution)
    clip = VideoFileClip(stream_url).subclip(s,e)
    clip = clip.without_audio()
    print(clip.size)
    x1 = clip.w//2-360
    x2 = clip.w//2+360
    y1 = clip.h//2-640
    y2 = clip.h//2+640
    rc = clip.crop(x1=x1,x2=x2,y1=y1,y2=y2)
    #text_clip = ImageClip("static\wm.png").set_duration(rc.duration) itag 303 try 308
    #wm = CompositeVideoClip([rc,text_clip])
    return rc

def make_fin_video(query):
    vidlist,durl = make_vidlist()
    vcmp = concatenate_videoclips(vidlist)
    drs = sum(durl)
    r = random.randint(120,3600)
    rc = back_vid(r,r+drs)
    final = CompositeVideoClip([rc,vcmp.set_start(0).set_duration(drs)])
    if query in ["what","when","whom","which","why","how","is","was","will","has","have","had"]:
        final.write_videofile(f'static/output/auto.mp4')
    else:
        query = query.replace('%20','_')
        final.write_videofile(f'static/output/{query}.mp4')
    

'''if __name__ == '__main__':
    make_fin_video()'''