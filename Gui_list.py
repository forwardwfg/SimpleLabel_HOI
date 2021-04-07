from tkinter.filedialog import askdirectory
import tkinter as tk
from tkinter import messagebox
from arg import * 
from tkinter import ttk

class GUI(object):
    def __init__(self):
        self.bbox_nums = 36
        self.window = tk.Tk()
        self.sub_var = tk.StringVar()
        self.relation_var = tk.StringVar()
        self.relation_var_w  =tk.StringVar()  
        self.pair_sub_var = tk.StringVar() 
        self.pair_obj_var = tk.StringVar() 

    def start_gui(self,q):
        self.window.title("Simple Label")
        # self.window.geometry('500x200')
        
        #每个bbox选择一个对象
        l = tk.Label(self.window,text="please select a subject for each bbox",bg='green', \
            font=('Arial', 12), width=40, height=1) 
        l.pack()
        for sub_key,sub_value in subject_cls.items():        
            r1 = tk.Radiobutton(self.window, text=str(sub_value)+":"+sub_key, variable=self.sub_var, \
                value=sub_value, command=None)
            r1.pack()
        b = tk.Button(self.window, text='certain', font=('Arial', 10), width=10, height=1, command=lambda:self.annotation(q))
        b.pack()

        #选择为<人-物>
        frm2_3 = tk.Frame(self.window)
        frm2 = tk.Frame(frm2_3)
        l = tk.Label(self.window,text="please select a <person,object> pair",bg='green', font=('Arial', 12), width=40, height=1) 
        l.pack()
        #l_pr = tk.label()
        # for i in range(self.bbox_nums):
        #     c2 = tk.Radiobutton(frm2, text = "bbox "+str(i), variable = self.pair_sub_var,value=i, command=None)
        #     c2.pack()
        l = tk.Label(frm2,text="select a subject bbx num", font=('Arial', 12), width=40, height=1) 
        l.pack()
        num_choice = ttk.Combobox(frm2, width=12, textvariable=self.pair_sub_var)
        num_choice['values']= tuple(range(self.bbox_nums))
        num_choice.pack()
        frm2.pack()

        frm3 = tk.Frame(frm2_3)
        # for i in range(self.bbox_nums):
        #     c2 = tk.Radiobutton(frm3, text = "bbox "+str(i), variable = self.pair_obj_var,value=i, command=None)
        #     c2.pack()
        # frm3.pack(side=tk.LEFT)
        l = tk.Label(frm3,text="select a obj bbx num", font=('Arial', 12), width=40, height=1) 
        l.pack()
        num_choice = ttk.Combobox(frm3, width=12, textvariable=self.pair_obj_var)
        num_choice['values']= tuple(range(self.bbox_nums))
        num_choice.pack()
        frm3.pack()
        frm2_3.pack()

        #选择的<人-物>关系
        frm4 = tk.Frame(self.window)
        l = tk.Label(self.window,text="please select a relation for the pair",\
                bg='green', font=('Arial', 12), width=40, height=1) 
        l.pack()
        for hoi_key,hoi_value in Hoi_cls.items():     
            r1 = tk.Radiobutton(frm4, text=str(hoi_value)+":"+hoi_key, variable=self.relation_var, \
                value=hoi_value, command=None)
            r1.pack()
        frm4.pack()
        if mode=="train":
            frm_t = tk.Frame(self.window)
            l_t = tk.Label(self.window,text="please select a object relation",\
                    bg='green', font=('Arial', 10), width=35, height=1) 
            l_t.pack()
            for hoi_key,hoi_value in Hoi_cls_What.items():     
                r1 = tk.Radiobutton(frm_t, text=str(hoi_value)+":"+hoi_key, variable=self.relation_var_w, \
                    value=hoi_value, command=None)
                r1.pack()
            frm_t.pack()


        b = tk.Button(self.window, text='certain', font=('Arial', 10), width=10, height=1, command=lambda:self.hoi_annotation(q))
        b.pack()

        self.window.mainloop()

    def hoi_annotation(self,q):
        # draw error!
        pair_sub_var = self.pair_sub_var.get()
        pair_obj_var = self.pair_obj_var.get()
        relation_var = self.relation_var.get()

        if mode=="train":
            relation_var_w = self.relation_var_w.get()

        all_dict = q.get()

        if mode=="test":
            hoi_dict = {"subject_id":int(pair_sub_var),"object_id":int(pair_obj_var),"category_id":int(relation_var)}
        else:
            hoi_dict = {"subject_id":int(pair_sub_var),"object_id":int(pair_obj_var),"category_id":int(relation_var),\
                        "hoi_category_id":int(relation_var_w)}

        if hoi_dict not in all_dict[-1]["hoi_annotations"]:
            all_dict[-1]["hoi_annotations"].append(hoi_dict)
        q.put(all_dict)
        print("after add a hoi:\n",all_dict[-2:])

        for i in all_dict[-1]["annotations"]:
            if i["category_id"]==-1:
                self.bbx_category_warning()
                all_dict = q.get()
                all_dict[-1]["hoi_annotations"].pop()
                q.put(all_dict)
                print("after warning:\n",all_dict[-1])
                break

    def annotation(self,q):
        category_id = self.sub_var.get()
        all_dict = q.get()

        s_x,s_y,e_x,e_y = all_dict[-1]["annotations"][-1]["bbox"]
        all_dict[-1]["annotations"][-1].update({"category_id":int(category_id)})
        q.put(all_dict)
        print("after adding a bbox:\n",all_dict[-2:])

    def bbx_category_warning(self):
        messagebox.showinfo(title='Warning', message='Error!\nforgotten bbox category\nplease draw again!')   

    def my_bbox_nums(self): #TODO: 如果发现之前定义的边框数量不够用，则可以自己定义一个
        pass

if __name__ == "__main__":
    q = []
    G = GUI()
    G.start_gui(q)
