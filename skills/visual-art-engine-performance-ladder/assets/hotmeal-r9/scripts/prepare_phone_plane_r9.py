from pathlib import Path
import cv2,numpy as np,json,base64
ROOT=Path('C:/AI/TenYears-Animatic-20261030');D=ROOT/'R9/PHONE';D.mkdir(exist_ok=True)
p=Path('C:/AI/MiniMax-H3/projects/H3-MINIMAL-20261015/input/HOTMEAL_R9_P_GUIDE.jpg')
im=cv2.imread(str(p));h,w=im.shape[:2]
mask=cv2.inRange(im,np.array([150,150,150],np.uint8),np.array([255,255,255],np.uint8))
roi=np.zeros((h,w),np.uint8);cv2.rectangle(roi,(int(w*.43),int(h*.1)),(int(w*.80),int(h*.75)),255,-1)
mask=cv2.bitwise_and(mask,roi);cs,_=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cand=[]
for c in cs:
 ar=cv2.contourArea(c);hull=cv2.convexHull(c);poly=cv2.approxPolyDP(hull,cv2.arcLength(hull,True)*.025,True)
 if ar>2000 and len(poly)==4:
  cand.append({'area':ar,'quad':poly[:,0,:].tolist(),'bounds':list(map(int,cv2.boundingRect(c)))})
cand.sort(key=lambda x:x['area'],reverse=True)
out=im.copy()
for j,c in enumerate(cand):
 q=np.array(c['quad']);cv2.polylines(out,[q],True,(0,0,255),2)
 for x,y in q:cv2.putText(out,str(x)+','+str(y),(int(x),int(y)),cv2.FONT_HERSHEY_SIMPLEX,.4,(0,0,255),1)
cv2.imwrite(str(D/'screen-source-detection.jpg'),out)
(D/'screen-source-candidates.json').write_text(json.dumps({'size':[w,h],'candidates':cand},indent=2))
print(json.dumps({'size':[w,h],'candidates':cand}),flush=True)
