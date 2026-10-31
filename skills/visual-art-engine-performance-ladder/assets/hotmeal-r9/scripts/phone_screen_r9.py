from pathlib import Path
import cv2,numpy as np,json,subprocess,hashlib,time
R=Path('C:/AI/TenYears-Animatic-20261030/R9');D=R/'PHONE'
raw=R/'P/native.mp4';guide=Path('C:/AI/MiniMax-H3/projects/H3-MINIMAL-20261015/input/HOTMEAL_R9_P_GUIDE.jpg')
assert raw.exists();D.mkdir(exist_ok=True)
full=cv2.imread(str(guide));base=cv2.resize(full,(384,320),interpolation=cv2.INTER_AREA)
q=np.array(json.loads((D/'screen-source-candidates.json').read_text())['candidates'][0]['quad'],np.float32)/2
mask=np.zeros((320,384),np.uint8);cv2.fillConvexPoly(mask,np.round(q).astype(np.int32),255)
mask=cv2.dilate(mask,np.ones((9,9),np.uint8))
sift=cv2.SIFT_create(nfeatures=1200,contrastThreshold=.018)
k0,d0=sift.detectAndCompute(cv2.cvtColor(base,cv2.COLOR_BGR2GRAY),mask)
assert d0 is not None and len(k0)>=15,'INSUFFICIENT_SOURCE_FEATURES'
cap=cv2.VideoCapture(str(raw));frames=[]
while True:
 ok,f=cap.read()
 if not ok:break
 frames.append(f)
cap.release();assert len(frames)==39
rows=[];hs=[];matcher=cv2.BFMatcher(cv2.NORM_L2)
for i,f in enumerate(frames):
 k1,d1=sift.detectAndCompute(cv2.cvtColor(f,cv2.COLOR_BGR2GRAY),cv2.dilate(mask,np.ones((21,21),np.uint8)))
 assert d1 is not None,('NO_TARGET_FEATURES',i)
 good=[a for a,b in matcher.knnMatch(d0,d1,k=2) if a.distance<.74*b.distance]
 assert len(good)>=10,('INSUFFICIENT_MATCHES',i,len(good))
 src=np.float32([k0[m.queryIdx].pt for m in good]);dst=np.float32([k1[m.trainIdx].pt for m in good])
 h,inside=cv2.findHomography(src,dst,cv2.RANSAC,1.5)
 assert h is not None and int(inside.sum())>=8,('HOMOGRAPHY_FAILED',i)
 fit=cv2.perspectiveTransform(src.reshape(-1,1,2),h).reshape(-1,2);errs=np.linalg.norm(fit-dst,axis=1)
 reproj=float(np.sqrt(np.mean(errs[inside[:,0].astype(bool)]**2)))
 assert reproj<1.2,('REPROJECTION_FAILED',i,reproj)
 target=cv2.perspectiveTransform(q.reshape(1,-1,2),h)[0]
 assert np.all(target[:,0]>0) and np.all(target[:,0]<384) and np.all(target[:,1]>0) and np.all(target[:,1]<320),('OFF_SCREEN',i)
 hs.append(h);rows.append({'frame':i,'matches':len(good),'inliers':int(inside.sum()),'inlier_rmse_native_px':reproj,'screen_quad_native':target.tolist(),'homography_base384_to_frame384':h.tolist()})
source_mask=np.zeros(full.shape[:2],np.uint8);cv2.fillConvexPoly(source_mask,np.round(q*2).astype(np.int32),255)
source_mask=cv2.erode(source_mask,np.ones((5,5),np.uint8))
output=R/'P/screen-fixed.mp4';temp=D/'screen-fixed-silent.mp4'
p=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s','384x320','-r','24','-i','pipe:0','-an','-c:v','libx264','-preset','fast','-crf','16','-pix_fmt','yuv420p','-movflags','+faststart',str(temp)],stdin=subprocess.PIPE)
for i,(f,h) in enumerate(zip(frames,hs)):
 transform=h@np.diag([.5,.5,1.]);patch=cv2.warpPerspective(full,transform,(384,320),flags=cv2.INTER_CUBIC)
 alpha=cv2.warpPerspective(source_mask,transform,(384,320),flags=cv2.INTER_LINEAR).astype(np.float32)/255
 out=np.round(f*(1-alpha[:,:,None])+patch*alpha[:,:,None]).clip(0,255).astype(np.uint8)
 if i in [0,12,24,38]:cv2.imwrite(str(D/f'fixed-frame-{i:03d}.jpg'),out)
 p.stdin.write(out.tobytes())
p.stdin.close();assert p.wait()==0
subprocess.run(['ffmpeg','-v','error','-y','-i',str(temp),'-i',str(raw),'-map','0:v:0','-map','1:a:0','-c','copy','-t',str(39/24),'-movflags','+faststart',str(output)],check=True)
corners=np.array([x['screen_quad_native'] for x in rows]);motion=float(np.linalg.norm(corners-corners[0],axis=2).max())
report={'method':'existing OpenCV SIFT + RANSAC planar homography, replace only inset screen glass with exact still reference; original phone body, hands and motion retained','frame_count':39,'source_guide_sha256':hashlib.sha256(guide.read_bytes()).hexdigest(),'all_tracks_passed':True,'max_reprojection_rmse_px':max(x['inlier_rmse_native_px'] for x in rows),'max_corner_displacement_native_px':motion,'interpolated_or_frozen_tracking_frames':0,'exact_screen_content':'static adult portrait and 老公，想你了。 from source guide','audio':'native P audio copied, not replaced','native_motion_artistic_approval':False,'rows':rows}
(D/'tracking-review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k!='rows'},ensure_ascii=True),flush=True)
