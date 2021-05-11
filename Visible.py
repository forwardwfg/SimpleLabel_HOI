import cv2
from arg import *
import os
import json

def visible(pic_json,img_name):
    file_name = img_name 
    pic_path = os.path.join(import_pic_path,file_name) 
    img = cv2.imread(pic_path)
    stack = [img.copy()]
    if not pic_json: return stack
    
    annotation =  pic_json["annotations"]
    for idx,bx in enumerate(annotation):
        s_x,s_y= bx["center"]
        R = bx['R']
        cv2.circle(img, (int(s_x),int(s_y)), int(R), (0,0,255), 4)
        cv2.putText(img,str(idx),(int(s_x-5),int(s_y)+5),cv2.FONT_HERSHEY_SIMPLEX,fontScale=1, color=(255,0,0),thickness=2)
        stack.append(img.copy())
    return stack



        

        
