from PIL import Image,ImageDraw,ImageFont
import pathlib,json,subprocess
p=pathlib.Path('C:/AI/Video-Recipe-Reproduction-20261108/Avatar-Specialist-20261109')
font='C:/Windows/Fonts/msyh.ttc'
def f(n):return ImageFont.truetype(font,n)
def txt(d,xy,s,n=28,color='#F6F8FC'):d.text(xy,s,font=f(n),fill=color)
def base(i,caption):
 im=Image.new('RGB',(1280,720),'#0B1526');d=ImageDraw.Draw(im)
 d.rectangle((0,0,1280,8),fill='#46D6C1')
 txt(d,(60,40),'\u628a\u5185\u5bb9\u8bb2\u6e05\u695a',42)
 txt(d,(915,55),'AI \u6570\u5b57\u4eba \u00b7 \u80fd\u529b\u6f14\u793a',19,'#92A9C7')
 d.line((60,117,1220,117),fill='#29394E',width=1)
 d.rounded_rectangle((46,632,1234,700),radius=16,fill='#17283F')
 # Sentence captions are timed to each generated speech segment.
 lines=[caption[j:j+32] for j in range(0,len(caption),32)]
 for k,line in enumerate(lines):txt(d,(640-int(d.textlength(line,font=f(24)))/2,639+k*29),line,24)
 txt(d,(60,599),'\u56fa\u5b9a\u4eba\u7269 / \u66f4\u6362\u8bb2\u89e3\u5185\u5bb9',20,'#92A9C7')
 txt(d,(1098,597),'0'+str(i+1)+' / 03',20,'#46D6C1')
 return im,d
parts=json.loads((p/'tts-run.json').read_text(encoding='utf-8'))['parts']
im,d=base(0,parts[0])
d.rounded_rectangle((54,168,458,572),radius=22,fill='#FFFFFF')
txt(d,(522,165),'\u4ece\u4e00\u6bb5\u6587\u6848\u5f00\u59cb',44)
txt(d,(522,240),'\u8ba9\u4e00\u4e2a\u56fa\u5b9a\u4eba\u7269\uff0c\u6301\u7eed\u4ecb\u7ecd\u4f60\u7684\u5185\u5bb9\u3002',25,'#ADC0D8')
for j,(a,b) in enumerate([('\u4eba\u50cf','\u540c\u4e00\u5f20\u9762\u5b54'),('\u58f0\u97f3','\u6e05\u6670\u666e\u901a\u8bdd'),('\u5185\u5bb9','\u6309\u6587\u6848\u8bb2\u89e3')]):
 x=522+j*232
 d.rounded_rectangle((x,333,x+212,478),radius=18,fill='#17283F')
 txt(d,(x+23,352),a,31,'#46D6C1');txt(d,(x+23,411),b,22)
txt(d,(522,527),'\u5934\u50cf\u53e3\u64ad + \u4ecb\u7ecd\u9875\u9762 + \u4e2d\u6587\u5b57\u5e55',25,'#ADC0D8')
im.save(p/'scene-0.png')
im,d=base(1,parts[1])
txt(d,(60,153),'\u4e09\u79cd\u5185\u5bb9\uff0c\u4e00\u8d77\u8bb2\u660e\u767d',40)
# Slide, image and interface representations are labelled examples.
cards=[('\u56fe\u7247\u4ecb\u7ecd','\u5c55\u793a\u4ea7\u54c1\u4e0e\u7279\u70b9'),('PPT \u8bb2\u89e3','\u63d0\u70bc\u4fe1\u606f\u4e0e\u91cd\u70b9'),('\u529f\u80fd\u753b\u9762','\u5c55\u793a\u64cd\u4f5c\u4e0e\u7ed3\u679c')]
for j,(a,b) in enumerate(cards):
 x=60+j*281
 d.rounded_rectangle((x,240,x+255,548),radius=19,fill='#F2F6FB')
 txt(d,(x+20,263),a,29,'#10253D')
 if j==0:
  d.rounded_rectangle((x+23,329,x+232,450),radius=12,fill='#CFECE6')
  d.ellipse((x+169,345,x+199,375),fill='#F5CF70')
  d.polygon([(x+35,433),(x+100,360),(x+151,416),(x+187,386),(x+220,433)],fill='#448C83')
 elif j==1:
  for k,w in enumerate([184,157,174]):
   d.rounded_rectangle((x+26,338+k*38,x+26+w,351+k*38),radius=6,fill=['#57BFAF','#A9BCCF','#A9BCCF'][k])
 else:
  d.rounded_rectangle((x+23,329,x+232,450),radius=10,fill='#DDE7F2')
  d.rectangle((x+23,329,x+232,356),fill='#B3C9DD')
  d.rounded_rectangle((x+45,380,x+116,424),radius=7,fill='#46B8A5')
  d.rounded_rectangle((x+135,380,x+212,392),radius=4,fill='#93AEC8')
  d.rounded_rectangle((x+135,408,x+196,420),radius=4,fill='#93AEC8')
 txt(d,(x+20,484),b,20,'#425B76')
d.rounded_rectangle((947,291,1213,557),radius=18,fill='white')
txt(d,(953,244),'\u8bb2\u89e3\u59cb\u7ec8\u5728\u573a',25,'#46D6C1')
txt(d,(60,564),'\u793a\u610f\u5185\u5bb9\u53ef\u66ff\u6362\u4e3a\u4f60\u7684\u56fe\u7247\u3001\u5e7b\u706f\u7247\u6216\u5b9e\u9645\u5f55\u5c4f\u3002',21,'#92A9C7')
im.save(p/'scene-1.png')
im,d=base(2,parts[2])
d.rounded_rectangle((54,168,458,572),radius=22,fill='#FFFFFF')
txt(d,(522,160),'\u6362\u5185\u5bb9\uff0c\u590d\u7528\u540c\u4e00\u4eba\u7269',39)
txt(d,(522,229),'\u56fa\u5b9a\u914d\u65b9\uff0c\u6309\u5185\u5bb9\u66ff\u6362\u3002',26,'#ADC0D8')
for j,(a,b) in enumerate([('01','\u4fee\u6539\u8bb2\u89e3\u6587\u6848'),('02','\u751f\u6210\u5bf9\u5e94\u914d\u97f3'),('03','\u53e3\u578b\u9a71\u52a8\u4e0e\u526a\u8f91')]):
 y=310+j*82
 d.rounded_rectangle((522,y,1209,y+64),radius=13,fill='#17283F')
 txt(d,(543,y+10),a,30,'#46D6C1');txt(d,(625,y+12),b,27)
txt(d,(522,570),'\u672c\u7247\u4e3a\u865a\u6784\u5f62\u8c61\u7684\u4e2d\u6587\u529f\u80fd\u6f14\u793a',18,'#92A9C7')
im.save(p/'scene-2.png')
# Decode sample counts, rather than using MP3 container padding, for scene timings.
ff='C:/Users/A/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-8.1.1-full_build/bin/ffmpeg.exe'
dur=[]
for i in range(3):
 r=subprocess.run([ff,'-v','error','-i',str(p/('speech-'+str(i)+'.mp3')),'-ac','1','-ar','16000','-f','s16le','-'],capture_output=True,check=True)
 dur.append(len(r.stdout)/32000)
(p/'scene-timing.json').write_text(json.dumps({'decoded_seconds':dur,'total_seconds':sum(dur),'avatar_placements':[[64,178,384],[955,299,250],[64,178,384]],'caption_type':'sentence level, derived from separately generated speech segments'},indent=2),encoding='utf-8')
print(json.dumps({'scenes':3,'timing':dur}),flush=True)
