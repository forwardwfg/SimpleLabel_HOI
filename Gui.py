import json
from tkinter.filedialog import askdirectory
import os 
import tkinter as tk
from tkinter import messagebox
from arg import * 
from PIL import Image, ImageTk
import numpy as np
from tkinter import messagebox
import pandas as pd

class GUI(object):
    def __init__(self,path):
        self.window = tk.Tk()
        self.window_right = tk.Frame(self.window)
        self.window_left = tk.Frame(self.window)
        self.male_var = tk.IntVar()
        self.female_var = tk.IntVar()
        self.child_var = tk.IntVar()
        self.young_var = tk.IntVar()
        self.mid_var = tk.IntVar()
        self.old_var = tk.IntVar()
        self.bag_var = tk.IntVar()
        self.mask_var = tk.IntVar()
        self.hat_var = tk.IntVar()
        self.luggage_var = tk.IntVar()
        self.pic_idx_dir = -1
        self.img = None
        self.label_img = None
        self.max_idx = len(os.listdir(path)) 
        self.img_name = None
        self.default_save_path = "./MultiLabel.json" 
        self.to_json = {}
        self.txt_show = None
        self.frm = None
        self.mark_path = "./mark.txt"
        

        self.varis = [self.male_var,self.female_var,self.child_var,self.young_var,self.mid_var,\
                self.old_var,self.bag_var,self.mask_var,self.hat_var,self.luggage_var]
    
    def win_right_GUI(self):
        l = tk.Label(self.window_right,text="please select labels for each picture",bg='green', \
            font=('Arial', 12), width=30, height=1) 
        l.pack()
        
        leng    = [len(i) for i in labels]
        max_len = max(leng)

        nll = ''
        for _ in labels:
            nll += ' ' 

        self.frm = tk.Frame(self.window_right)

        frm1 = tk.Frame(self.frm) 
        for v,i in zip(self.varis,labels):
            frm2 = tk.Frame(frm1)
            s = nll[:max_len-len(i)]+i #右对齐
            r = tk.Label(frm2,text=s)
            r.pack(side=tk.LEFT)
            r1   = tk.Radiobutton(frm2,text='1',variable=v,value=1,command=None)
            r0   = tk.Radiobutton(frm2,text='0',variable=v,value=0,command=None)
            r2   = tk.Radiobutton(frm2,text='NotSure',variable=v,value=2,command=None)
            r1.pack(side=tk.LEFT)
            r0.pack(side=tk.LEFT)
            r2.pack(side=tk.LEFT)
            frm2.pack()
        frm1.pack(side=tk.LEFT)
        self.frm.pack()

        b = tk.Button(self.window_right, text='certain', font=('Arial', 10), width=10, height=1, command=self.selection)
        b.pack()

        frm2 = tk.Frame(self.window_right)
        b = tk.Button(frm2, text='pre', font=('Arial', 10), width=10, height=1, command=lambda:self.show_pic(-1))
        b.pack(side=tk.LEFT)
        b = tk.Button(frm2, text='next', font=('Arial', 10), width=10, height=1, command=lambda:self.show_pic(1))
        b.pack(side=tk.LEFT)
        frm2.pack()

        c = tk.Button(self.window_right, text='to csv', font=('Arial', 10), width=10, height=1, command=self.save_csv)
        c.pack(pady=20)

        self.window_right.pack(side=tk.RIGHT)
 
 
    def start_gui(self):
        self.window.title("Simple Label(MultiLabel)")
        self.win_right_GUI()
        
        self.txt_show = tk.Text(self.window_left,height=4,width=50)
        self.txt_show.pack(side=tk.BOTTOM)
        txt_title = tk.Label(self.window_left,text="Your seclected labels shown in the following box")
        txt_title.pack(side=tk.BOTTOM)

        self.init_idx()        
        self.show_pic()
        self.window.mainloop()

    def selection(self):
        new_dict = {}

        for flag,value in zip(labels,self.varis):
            new_dict[flag] = value.get()
        # if img information exists in json,update them or add the information.
        if self.img_name in self.to_json:
            self.to_json[self.img_name].update(new_dict) 
        else:
            self.to_json[self.img_name] = new_dict
        
        print(self.to_json)
        self.show_txt()
        self.save_json()

    def messagebox_first(self):
        messagebox.showinfo(title='Warning', message="It's already the first picture!")

    def messagebox_last(self):
        messagebox.showinfo(title='Warning', message="It's already the last picture!")

    def messagebox_conver(self):
        messagebox.showinfo(title='ok', message="conver to csv file successfully!")


    def save_json(self):
        with open(self.default_save_path,'w') as f:
            json.dump(self.to_json,f)

        with open(self.mark_path,"w") as f:
            f.write(self.img_name)
    
    def img_process(self):
        height,width,_ = np.shape(self.img)
        max_l = max(height,width)
        
        if max_l> 500 and width>height:
            ft = 500/max_l
            self.img = self.img.resize((int(width*ft),int(height*ft)))
        
        if max_l>400 and height>width:
            ft = 400/max_l
            self.img = self.img.resize((int(width*ft),int(height*ft)))
    
    def init_idx(self):
        if os.path.exists(self.default_save_path) and os.path.exists(self.mark_path):
            with open(self.mark_path) as f:
                marked = f.readline()
                print("mark",marked)

            for idx,i in enumerate(os.listdir(img_path)):
                if i !=marked:
                    continue
                else:self.pic_idx_dir = idx-1

        
    def show_txt(self):
        if self.img_name in self.to_json:
            txt_to_show = [key for key,value in self.to_json[self.img_name].items() if int(value)==1]
            self.txt_show.delete(1.0, tk.END)
            self.txt_show.insert(tk.INSERT,txt_to_show)
        else:
            self.txt_show.delete(1.0, tk.END)#delete the first char to the last char in the txt box 
    
    def save_csv(self):
        df = pd.DataFrame(self.to_json).T
        df.to_csv('MultiLabel.csv')
        self.messagebox_conver()

    def show_pic(self,num=1):

        for v in self.varis: v.set(0)

        if self.pic_idx_dir+num<0:
            self.messagebox_first()
            return None 
        if self.pic_idx_dir+num>=self.max_idx:
            self.messagebox_last()
            return None
        
        self.pic_idx_dir += num

        print(self.pic_idx_dir)
        self.img_name = os.listdir(img_path)[self.pic_idx_dir]
        if self.img_name[-3:].lower() not in img_format:
            print(self.img_name)
            raise Exception("please input a image!")

        pic_path = os.path.join(img_path,self.img_name) 
        assert os.path.exists(pic_path),"path not found!"

        #show labels in json
        self.show_txt()

        self.img = Image.open(pic_path)# use PIL to process picture,or only .gif format can be shown.
        self.img_process()
        print(pic_path)
 
        self.img = ImageTk.PhotoImage(self.img)
        if self.label_img:
            self.label_img.destroy()
        self.label_img = tk.Label(self.window_left,image=self.img,width=500, height=400,background='grey')
        self.label_img.pack()
        self.window_left.pack(side=tk.LEFT)
        self.window.mainloop()


if __name__ == "__main__":
    gui = GUI(img_path)
    gui.start_gui()


