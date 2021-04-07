import cv2 
import os
import json
from arg import *
import numpy as np
from Visible import visible
class draw():
    def __init__(self):
        super().__init__()
        self.s_x = 0
        self.s_y = -1
        self.e_x = -1
        self.e_y = -1
        # self.dir_path = '/media/ubuntu_data2/gwf/pic/'
        # self.dir_path = 'Y:/02_dataset/qiuweiyu/to_fgm/csbank/'
        self.dir_path = '/home/gwf/图片'
        self.img_name = None
        self.img_new = None
        self.img_new_copy = None
        self.img_time = None
        self.after_mv = False
        self.drawed = False
        self.withdrawed_last = False
        self.stack = {}
        self.stack_name = []
        self.pic_idx_in_json = 0
        self.pic_idx_in_dir = 0
        

    def draw_rectangle(self,event,x,y,flags,q_json):
        
        self.img_new_copy = self.img_new.copy()
        if event==cv2.EVENT_LBUTTONDOWN:
            self.s_x,self.s_y=x,y
        elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
            self.after_mv = True
            cv2.rectangle(self.img_new_copy,(self.s_x,self.s_y),(x,y),(0,0,195),3) #还没确定终点之前都在之前的图上画，
            self.img_time = self.img_new_copy
          

        if self.after_mv and event==cv2.EVENT_LBUTTONUP:
            self.img_new = self.img_time
            self.e_x,self.e_y = x,y
            if q_json.empty():
                q_json.put({self.img_name:{"img_id":0,"hoi_annotations":[],"annotations":[]}})
                cur_dict = q_json.get()
            else:
                cur_dict = q_json.get()

                if self.img_name not in cur_dict.keys():
                    #如果json还没有对于的数据，那么字典初始化
                    if mode=="test":
                        cur_dict[self.img_name] = {"hoi_annotations":[],"annotations":[]}
                    else:
                        cur_dict[self.img_name] = {"img_id":len(cur_dict),"hoi_annotations":[],"annotations":[]}
          
            #边界处理
            height,weight,depth = self.img_new.shape
            if self.s_x < 0:
                self.s_x = 0
            if self.s_y < 0:
                self.s_y = 0 
            if self.s_x > weight:
                self.s_x = weight-1
            if self.s_y > height:
                self.s_y = height-1 
            #如果逆着画，终点坐标有可能小于0
            if self.e_x < 0:
                self.e_x = 0
            if self.e_y < 0:
                self.e_y = 0
            if self.e_x > weight:
                self.e_x = weight-1
            if self.e_y > height:
                self.e_y = height-1


              #如果是从右下角画到左上角,交换坐标
            if self.s_x>self.e_x and self.s_y>self.e_y:
                sx,sy,ex,ey = self.e_x,self.e_y,self.s_x,self.s_y
                self.s_x,self.s_y,self.e_x,self.e_y = sx,sy,ex,ey

            # 如果从左下角画到右上角
            if self.e_x>self.s_x and self.e_y<self.s_y:
                ex,ey = self.e_x,self.s_y
                sx,sy = self.s_x,self.e_y
                self.s_x,self.s_y,self.e_x,self.e_y = sx,sy,ex,ey
            
            # 如果从右上角画到左下角
            if self.e_x<self.s_x and self.e_y>self.s_y:
                ex,ey = self.s_x,self.e_y
                sx,sy = self.e_x,self.s_y
                self.s_x,self.s_y,self.e_x,self.e_y = sx,sy,ex,ey
            
            an_n = len(cur_dict[self.img_name]["annotations"])
            #每个边框写上它的id
            cv2.putText(self.img_time,str(an_n),(self.e_x-5,self.s_y+5),cv2.FONT_HERSHEY_SIMPLEX,fontScale=0.8, color=(255,0,0),thickness=2)
            pos = [self.s_x,self.s_y,self.e_x,self.e_y]
            category_id = -1
            #输入category_id
        
            bbox_dict = {"bbox":pos,"category_id":category_id}

            cur_dict[self.img_name]["annotations"].append(bbox_dict)
            q_json.put(cur_dict)
            # self.drawed = True
            self.after_mv = False
            self.stack[self.img_name].append(self.img_time)

      
    def start_draw(self,q_json,q_idx):
           
      
        with open(import_json,'r') as f:
            try:
                json_data = json.load(f)      
                q_json.put(json_data)         
            except:
            #     q_json.put({})
                json_data = {}
                pass


        imgs_dirs = os.listdir(import_pic_path)

        if os.path.exists('./last_visited.txt'): 
            with open('./last_visited.txt','r') as f:
                
                try:self.pic_idx_in_dir = int(f.read()[0]) 
                except:self.pic_idx_in_dir=0
                self.img_name = imgs_dirs[self.pic_idx_in_dir]
                print('last visited image is {}'.format(self.img_name))
            
        while self.pic_idx_in_dir < len(imgs_dirs):
        
            self.img_name = imgs_dirs[self.pic_idx_in_dir]
            self.drawed  = False
            self.withdrawed = False
            q_idx.put(self.img_name)

            #把改图的数据提取出来，然后就行绘制
            if self.img_name in json_data.keys():
                pic_json = json_data[self.img_name]
            else:
                pic_json = {}

            # self.img_name = pic_json["file_name"]
            stack = visible(pic_json,self.img_name)
            self.stack[self.img_name] = stack 
            self.img_new = stack[-1] #这图片把所有的框都画出来了

            if self.img_name not in self.stack_name:
                self.stack_name.append(self.img_name)
                

            if len(self.stack[self.img_name])>1:#说明图片被标注过,
                self.drawed = True

            self.img_time = self.img_new
            cv2.namedWindow(self.img_name,0)#没有namedwindow，不能画，为啥？
            cv2.resizeWindow(self.img_name,960,540)
            cv2.setMouseCallback(self.img_name,self.draw_rectangle,q_json)
            print("img_name:{} is processing".format(self.img_name))
            
            while(1):
                cv2.imshow(self.img_name,self.img_time) #不断显示实时图片
                k=cv2.waitKey(1)&0xFF
                if k == 27: # ESC键 切换图片
                    json_data = q_json.get()
                    q_json.put(json_data)
                    if self.img_name not in json_data.keys(): 
                        with open('./skip.txt','a') as f:   #记录没有标注过的图片
                            f.write(self.img_name) 
                            f.write('\r\n')

                    with open('./last_visited.txt','w') as f:
                        f.write(str(self.pic_idx_in_dir)+' '+self.img_name)#记录最后访问的图片

                    cv2.destroyAllWindows()
                    break
                
                if k == 122: #输入z,撤回绘制的边框
                    self.withdraw_operator(q_json,q_idx)
                
                if k == 98: #输入b,撤回到上一张
                    self.withdraw_last(q_json,q_idx)
        

            if not q_json.empty():
                data = q_json.get()
                with open('label_'+mode+'.json','w') as f:
                    json.dump(data,f)
                q_json.put(data)

            self.pic_idx_in_dir += 1
            q_idx.get()

        print("The End!")
    
    def withdraw_last(self,q_json,q_idx):

        self.withdrawed_last = True
        if len(self.stack_name)>=2:
            cur_dict  = q_json.get()

            cur_name = self.stack_name[-1]
            self.stack_name.pop()
            self.img_name = self.stack_name[-1]
            self.img_time = self.stack[self.img_name][-1]
            self.img_new = self.img_time

            cv2.destroyAllWindows()
            q_json.put(cur_dict)
            cv2.namedWindow(self.img_name,0)
            cv2.resizeWindow(self.img_name,960,540)
            cv2.setMouseCallback(self.img_name,self.draw_rectangle,q_json)
            self.pic_idx_in_dir -= 1
            

            q_idx.get()
            q_idx.put(self.img_name)

    def withdraw_operator(self,q_json,q_idx):
        
        # id_del = self.pic_idx_in_json 

        if len(self.stack[self.img_name])>1:
            self.stack[self.img_name].pop()
            self.img_time = self.stack[self.img_name][-1]
            self.img_new = self.img_time

            cur_dict  = q_json.get()

            if cur_dict[self.img_name]["annotations"]:
                cur_dict[self.img_name]["annotations"].pop()
                
            leng = len(cur_dict[self.img_name]["annotations"])
            if leng==0: 
                del cur_dict[self.img_name]
            else:
                
                hoi = cur_dict[self.img_name]["hoi_annotations"][::-1]
                for h in hoi:
                    sub_id = h["subject_id"]
                    obj_id = h["object_id"]
                    if sub_id not in range(leng) and obj_id not in range(leng):
                        cur_dict[self.img_name]["hoi_annotations"].pop() #如果subject_id和object_id对应的bbx不存在，则把该hoi删除

            q_json.put(cur_dict)

            try:
                print("after withdraw:\n",self.img_name,cur_dict[self.img_name])
            except:
                print("after withdraw:\n",self.img_name,[])
        