from pathlib import Path
import cv2,numpy as np,json,av
from PIL import Image,ImageDraw
R=Path('C:/AI/TenYears-Animatic-20261030/R9');D=R/'PHONE'
track=json.loads((D/'tracking-review.json').read_text(encoding='utf-8'))
cap=cv2.VideoCapture(str(R/'P/native.mp4'));rows=[];fs=[];i=0
while True:
 ok,f=cap.read()
 if not ok:break
 fs.append(f)
 mask=cv2.inRange(f,np.array([150,150,150],np.uint8),np.array([255,255,255],np.uint8))
 roi=np.zeros((320,384),np.uint8);cv2.rectangle(roi,(165,30),(308,235),255,-1);mask=cv2.bitwise_and(mask,roi)
 cs,_=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE);cand=[]
 for c in cs:
  ar=cv2.contourArea(c);hu=cv2.convexHull(c);p=cv2.approxPolyDP(hu,cv2.arcLength(hu,True)*.025,True)
  if ar>3500 and len(p)==4:cand.append((ar,p[:,0,:].astype(np.float32)))
 if cand:
  q=max(cand,key=lambda x:x[0])[1];target=np.array(track['rows'][i]['screen_quad_native'])
  best=min(float(np.sqrt(np.mean(np.sum((target-np.roll(q,j,axis=0))**2,axis=1)))) for j in range(4))
  rows.append({'frame':i,'independent_white_glass_corner_rmse_px':best,'detected_quad':q.tolist()})
 else:rows.append({'frame':i,'independent_white_glass_corner_rmse_px':None})
 i+=1
n=[r['independent_white_glass_corner_rmse_px'] for r in rows if r['independent_white_glass_corner_rmse_px'] is not None]
report={'frames':len(rows),'independently_detected':len(n),'max_corner_rmse_px':max(n) if n else None,'median_corner_rmse_px':float(np.median(n)) if n else None,'rows':rows}
(D/'independent-border-check.json').write_text(json.dumps(report,indent=2))
raw=[f.to_image() for f in av.open(str(R/'P/native.mp4')).decode(video=0)];fixed=[f.to_image() for f in av.open(str(R/'P/screen-fixed.mp4')).decode(video=0)]
sheet=Image.new('RGB',(1536,680),'white');dr=ImageDraw.Draw(sheet)
for j,k in enumerate([0,12,24,38]):
 for row,arr in enumerate([raw,fixed]):
  x=j*384;y=row*340;sheet.paste(arr[k],(x,y+20));dr.text((x+4,y+3),('RAW' if row==0 else 'FIXED')+' f'+str(k),fill='black')
sheet.save(D/'raw-vs-fixed.jpg',quality=94)
print(json.dumps({k:v for k,v in report.items() if k!='rows'}),flush=True)
