from pathlib import Path
import cv2
from PIL import Image,ImageDraw
R=Path('C:/AI/TenYears-Animatic-20261030');D=R/'R9/VIDEO_REVIEW'
for shot,ids in [('B_AV',[35,40,44,46,47,48,49,50,52,56,64,72]),('C',[0,24,48,72,96,120,144,174])]:
 cap=cv2.VideoCapture(str(R/f'R8/{shot}/native.mp4'));sheet=Image.new('RGB',(384*4,344*((len(ids)+3)//4)), 'white');dr=ImageDraw.Draw(sheet)
 for j,i in enumerate(ids):
  cap.set(1,i);ok,f=cap.read();assert ok
  x=j%4*384;y=j//4*344;sheet.paste(Image.fromarray(cv2.cvtColor(f,cv2.COLOR_BGR2RGB)),(x,y+24));dr.text((x+4,y+4),f'{shot} f{i} {i/24:.3f}s',fill='black')
 cap.release();sheet.save(D/f'{shot}-critical-frames.jpg')
print('READY')
