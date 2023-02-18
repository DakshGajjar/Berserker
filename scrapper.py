from bs4 import BeautifulSoup as bs
import requests,pyttsx3,re,os,random
from PIL import Image,ImageDraw,ImageFont
from makevid import make_fin_video

def extr_post(query):
    ptext = []
    pdict = {}
    urllist = ['https://www.reddit.com/r/AskReddit','https://www.reddit.com/r/questions','https://www.reddit.com/r/Jokes/','https://www.reddit.com/r/AskWomen/','https://www.reddit.com/r/askscience/','https://www.reddit.com/r/AskScienceFiction/','https://www.reddit.com/r/AskAcademia/','https://www.reddit.com/r/AskHistorians/','https://www.reddit.com/r/NoStupidQuestions','https://www.reddit.com/r/UnethicalLifeProTips','https://www.reddit.com/r/AskMen/']
    for url in random.sample(urllist,5):
        page = requests.get(f'{url}/search/?q={query}')#&restrict_sr=1&sr_nsfw=0&sort=comments?scroll=2000
        html = page.content
        soup=bs(html,"html.parser")
        #print(soup.text)
        elements = soup.find_all(class_="Post")
        #print(elements)
        for ele in elements:
            text = ele.find("h3")
            ls = ele.find_all('a')
            link = 'https://www.reddit.com'+ls[-1].get('href')
            #links.append(links)
            cont = text.get_text()
            if 'Megathread' not in cont and len(cont)>10:
                ptext.append(cont)
                pdict[cont] = link
    return pdict,ptext
                #ptext.append(cont)

def extr_cmts(query):
    while True:
        pdict,ptext = extr_post(query)
        if len(ptext)>0:
            break
    #print(ptext)
    clist = []
    for i in ptext:
        cmts = []
        page = requests.get(pdict[i])
        html = page.content
        soup=bs(html,"html.parser")
        #head_div = soup.find(class_="Post")
        elements = soup.find_all(class_="Comment")
        for ele in elements:
            para = ele.find_all('p')
            cont = ''.join([i.text for i in para])
            if len(cont)>20 and len(cont)< 250:
                cmts.append(cont)
        if(len(cmts)>0):
            clist.append([i,cmts])
    return clist

def extr_links(str):
    if "https://" in str:
        url_pattern = r"(https?://[^\s]+)"
        urls = re.findall(url_pattern, str)
        for i in urls:
            nstr = str.replace(i,'')
        return nstr
    else:
        return str

def txt_to_speech(str,filename):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150) 
    engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')
    str = extr_links(str)
    engine.save_to_file(str,f'static/ss_audioes/{filename}.mp3')
    engine.runAndWait()

def make_para(text):
    text = extr_links(text)
    if len(text)>30:
        space = text[:30][::-1].index(' ')
        gentxt = text[:30-space]
        ntxt = text[30-space:]
        return gentxt + '\n' + make_para(ntxt)
    else:
        return text
        #text = text[:space]

def make_img(text,filename,fs):
    fintext = make_para(text)
    #nls = len([i for i,j in enumerate(fintext) if j=="\n"])
    img = Image.new('RGBA', (720, 1280), (63,63,63,0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("static\FiraSans-Bold.ttf",fs)
    text_width, text_height = draw.textsize(fintext, font=font)
    draw.rectangle((350-text_width//2,640-text_height//2,360+text_width//2,650+text_height//2),fill=(95,95,95,149))
    print(text_width,text_height)
    text_position = (360-(text_width//2),640-(text_height//2))
    draw.text(text_position, fintext, font=font, fill=(255, 255, 255, 255))
    img.save(f"static/ss_imgs/{filename}.png")
    #print(img.size,len(text))

def make_clist(query):
    while True:
        clist = extr_cmts(query)
        for i in clist:
            if len(i[1])<0:
                break
        break
    return clist

#clist = extr_cmts(query)
def final(query):
    while True:
        clist = make_clist(query)
        if len(clist)>0:
            break
    print(clist[:5]) if len(clist)>5 else print(clist)
    if len(clist)>0:
        ranp = random.sample(clist,1)[0]
        txt_to_speech(ranp[0],f'a-{query}')
        make_img(ranp[0],f'a-{query}',44)
        for j,k in enumerate(ranp[1][:8]):
            txt_to_speech(k,f'cmt{j}')
            make_img(k,f'cmt{j}',41)
    if len(os.listdir('static/ss_imgs'))>0 and len(os.listdir('static/ss_audioes'))>0:
        make_fin_video(query)