import math
import cv2
import numpy as np

def runway_center(corners):
    pts=np.array([corners['TL'],corners['TR'],corners['BL'],corners['BR']],dtype=float)
    return tuple(np.mean(pts,axis=0))

def centerline(corners):
    tl,tr=np.array(corners['TL'],float),np.array(corners['TR'],float)
    bl,br=np.array(corners['BL'],float),np.array(corners['BR'],float)
    return tuple((tl+tr)/2),tuple((bl+br)/2)

def orientation_angle(corners):
    top,bottom=centerline(corners)
    return math.degrees(math.atan2(bottom[1]-top[1],bottom[0]-top[0]))

def angular_deviation(corners, reference_angle=90.0):
    diff=abs(orientation_angle(corners)-reference_angle)%180
    return float(min(diff,180-diff))

def lateral_deviation(corners,image_width):
    cx=runway_center(corners)[0]; ic=image_width/2
    px=abs(cx-ic); return float(px),float(px/max(ic,1))

def alignment_status(lateral_norm,angular_deg,lateral_good=.15,lateral_minor=.30,angular_good=5,angular_minor=10):
    if lateral_norm<=lateral_good and angular_deg<=angular_good:return 'GOOD'
    if lateral_norm<=lateral_minor and angular_deg<=angular_minor:return 'MINOR DEVIATION'
    return 'MISALIGNED'

def landing_zone_assessment(corners,image_width,image_height):
    top,bottom=centerline(corners)
    p1=np.array(top)+.35*(np.array(bottom)-np.array(top))
    p2=np.array(top)+.65*(np.array(bottom)-np.array(top))
    return {'type':'central_runway_zone','top_center':tuple(p1),'bottom_center':tuple(p2),'description':'Project-defined central runway landing-assessment zone'}

def extract_bbox(detection):
    if hasattr(detection,'boxes'):
        boxes=detection.boxes
        if boxes is None or len(boxes)==0:return None
        a=boxes.xyxy.cpu().numpy()[0]; return tuple(map(int,a[:4]))
    if hasattr(detection,'xyxy'):
        a=detection.xyxy.cpu().numpy()[0]; return tuple(map(int,a[:4]))
    if isinstance(detection,dict):
        a=detection.get('bbox',detection.get('box'))
        if a is not None:return tuple(map(int,a[:4]))
    a=np.asarray(detection).reshape(-1)
    if len(a)>=4:return tuple(map(int,a[:4]))
    raise ValueError('Could not extract runway bounding box.')

def _line_x_at_y(line,y):
    x1,y1,x2,y2=map(float,line)
    if abs(y2-y1)<1e-8:return None
    return x1+(y-y1)*(x2-x1)/(y2-y1)

def extract_corners_from_hough(roi,canny_low=50,canny_high=150,hough_threshold=40,min_line_length=40,max_line_gap=30):
    gray=cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
    edges=cv2.Canny(cv2.GaussianBlur(gray,(5,5),0),canny_low,canny_high)
    lines=cv2.HoughLinesP(edges,1,np.pi/180,threshold=hough_threshold,minLineLength=min_line_length,maxLineGap=max_line_gap)
    if lines is None:return None,edges,None
    c=[]; h,w=roi.shape[:2]
    for item in lines:
        x1,y1,x2,y2=item[0]; dx=x2-x1;dy=y2-y1; length=math.hypot(dx,dy)
        if length<min_line_length:continue
        angle=math.degrees(math.atan2(dy,dx))
        if abs(angle)<15 or abs(angle)>165:continue
        c.append((length,(x1,y1,x2,y2)))
    c.sort(reverse=True,key=lambda z:z[0])
    chosen=None
    for i in range(min(len(c),30)):
        for j in range(i+1,min(len(c),30)):
            l1,l2=c[i][1],c[j][1]; m1=(l1[0]+l1[2])/2;m2=(l2[0]+l2[2])/2
            if abs(m1-m2)<.15*w:continue
            if (m1<w/2 and m2>w/2) or (m2<w/2 and m1>w/2):chosen=(l1,l2);break
        if chosen:break
    if chosen is None:return None,edges,lines
    l1,l2=chosen
    if (l1[0]+l1[2])/2>(l2[0]+l2[2])/2:l1,l2=l2,l1
    vals=[_line_x_at_y(l1,0),_line_x_at_y(l1,h-1),_line_x_at_y(l2,0),_line_x_at_y(l2,h-1)]
    if any(v is None for v in vals):return None,edges,lines
    lt,lb,rt,rb=vals
    if lt>=rt or lb>=rb:return None,edges,lines
    return {'TL':(lt,0),'TR':(rt,0),'BL':(lb,h-1),'BR':(rb,h-1)},edges,lines

def bbox_corners_fallback(bbox):
    x1,y1,x2,y2=bbox
    return {'TL':(x1,y1),'TR':(x2,y1),'BL':(x1,y2),'BR':(x2,y2)}

def analyze_alignment(image,runway_detection,use_hough=True,reference_angle=90.0):
    if image is None:raise ValueError('image is None')
    h,w=image.shape[:2]; bbox=extract_bbox(runway_detection)
    if bbox is None:return {'alignment_status':'NO RUNWAY DETECTED','annotated_image':image.copy()}
    x1,y1,x2,y2=bbox; x1=max(0,min(x1,w-1));y1=max(0,min(y1,h-1));x2=max(0,min(x2,w-1));y2=max(0,min(y2,h-1))
    roi=image[y1:y2,x1:x2].copy()
    corners_roi=edges=lines=None
    if use_hough: corners_roi,edges,lines=extract_corners_from_hough(roi)
    if corners_roi is not None:
        corners={k:(v[0]+x1,v[1]+y1) for k,v in corners_roi.items()}; source='YOLO bbox + Canny/Hough'
    else:
        corners=bbox_corners_fallback((x1,y1,x2,y2)); source='YOLO bbox fallback'
    center=runway_center(corners); top,bottom=centerline(corners); angle=orientation_angle(corners)
    ang=angular_deviation(corners,reference_angle); lat_px,lat_norm=lateral_deviation(corners,w)
    lz=landing_zone_assessment(corners,w,h); status=alignment_status(lat_norm,ang)
    out=image.copy(); cv2.rectangle(out,(x1,y1),(x2,y2),(0,255,0),2)
    for name,p in corners.items():
        px,py=map(int,p);cv2.circle(out,(px,py),6,(0,0,255),-1);cv2.putText(out,name,(px+8,py-8),cv2.FONT_HERSHEY_SIMPLEX,.6,(0,0,255),2)
    cv2.line(out,tuple(map(int,top)),tuple(map(int,bottom)),(255,0,0),3); cv2.line(out,(w//2,0),(w//2,h),(255,255,0),2);cv2.circle(out,tuple(map(int,center)),8,(255,0,255),-1)
    cv2.line(out,tuple(map(int,lz['top_center'])),tuple(map(int,lz['bottom_center'])),(0,165,255),5)
    cv2.putText(out,f'Lateral deviation: {lat_norm*100:.1f}%',(20,35),cv2.FONT_HERSHEY_SIMPLEX,.75,(255,255,255),2)
    cv2.putText(out,f'Angular deviation: {ang:.1f} deg',(20,65),cv2.FONT_HERSHEY_SIMPLEX,.75,(255,255,255),2)
    cv2.putText(out,f'Alignment: {status}',(20,95),cv2.FONT_HERSHEY_SIMPLEX,.8,(255,255,255),2)
    return {'lateral_deviation':lat_px,'lateral_deviation_normalized':lat_norm,'angular_deviation':ang,'alignment_status':status,'landing_zone':lz,'runway_corners':corners,'runway_center':center,'centerline':{'top':top,'bottom':bottom},'runway_orientation':angle,'detection_bbox':(x1,y1,x2,y2),'geometry_source':source,'annotated_image':out,'edges':edges,'hough_lines':lines}

def analyze_ground_truth_alignment(image,corners):
    h,w=image.shape[:2]; center=runway_center(corners);top,bottom=centerline(corners);angle=orientation_angle(corners);ang=angular_deviation(corners);lat_px,lat_norm=lateral_deviation(corners,w);lz=landing_zone_assessment(corners,w,h);status=alignment_status(lat_norm,ang)
    out=image.copy()
    for name,p in corners.items():
        px,py=map(int,p);cv2.circle(out,(px,py),6,(0,0,255),-1);cv2.putText(out,name,(px+8,py-8),cv2.FONT_HERSHEY_SIMPLEX,.6,(0,0,255),2)
    cv2.line(out,tuple(map(int,top)),tuple(map(int,bottom)),(255,0,0),3);cv2.line(out,(w//2,0),(w//2,h),(255,255,0),2);cv2.circle(out,tuple(map(int,center)),8,(255,0,255),-1)
    cv2.putText(out,f'Lateral deviation: {lat_norm*100:.1f}%',(20,35),cv2.FONT_HERSHEY_SIMPLEX,.75,(255,255,255),2);cv2.putText(out,f'Angular deviation: {ang:.1f} deg',(20,65),cv2.FONT_HERSHEY_SIMPLEX,.75,(255,255,255),2);cv2.putText(out,f'Alignment: {status}',(20,95),cv2.FONT_HERSHEY_SIMPLEX,.8,(255,255,255),2)
    return {'lateral_deviation':lat_px,'lateral_deviation_normalized':lat_norm,'angular_deviation':ang,'alignment_status':status,'landing_zone':lz,'runway_corners':corners,'runway_center':center,'centerline':{'top':top,'bottom':bottom},'runway_orientation':angle,'geometry_source':'LARD_V2 ground truth','annotated_image':out}
