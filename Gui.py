from tkinter.filedialog import askdirectory
import tkinter as tk
from tkinter import messagebox
from arg import * 
import numpy as np


class GUI(object):
    def __init__(self):
        self.bbox_nums = 10
        self.window = tk.Tk()
        self.sub_var = tk.IntVar()
        self.pair_sub_var = tk.IntVar() 
        self.pair_obj_var = tk.IntVar() 

    def start_gui(self,q_json,q_idx):
        self.window.title("Simple Label")
        # self.window.geometry('500x200')
        
        #每个bbox选择一个对象
        # l = tk.Label(self.window,text="please select a subject for each bbox",bg='green', \
        #     font=('Arial', 12), width=40, height=1) 
        # l.pack()
        # for sub_key,sub_value in subject_cls.items():        
        #     r1 = tk.Radiobutton(self.window, text=str(sub_value)+":"+sub_key, variable=self.sub_var, \
        #         value=sub_value, command=None)
        #     r1.pack()
        # b = tk.Button(self.window, text='certain', font=('Arial', 10), width=10, height=1, command=lambda:self.annotation(q_json,q_idx))
        # b.pack()

        #选择为<人-物>
        frm2_3 = tk.Frame(self.window)
        frm2 = tk.Frame(frm2_3)
        l = tk.Label(self.window,text="please select a <person,object> pair",bg='green', font=('Arial', 12), width=40, height=1) 
        l.pack()
        #l_pr = tk.label()
        for i in range(self.bbox_nums):
            c2 = tk.Radiobutton(frm2, text = "bbox "+str(i), variable = self.pair_sub_var,value=i, command=None)
            c2.pack()
        frm2.pack(side=tk.LEFT)

        frm3 = tk.Frame(frm2_3)
        for i in range(self.bbox_nums):
            c2 = tk.Radiobutton(frm3, text = "bbox "+str(i), variable = self.pair_obj_var,value=i, command=None)
            c2.pack()
        frm3.pack(side=tk.LEFT)
        frm2_3.pack()

        #选择的<人-物>关系
        frm4 = tk.Frame(self.window)



        b = tk.Button(self.window, text='certain', font=('Arial', 10), width=10, height=1, command=lambda:self.hoi_annotation(q_json,q_idx))
        b.pack()

        self.window.mainloop()

    def hoi_annotation(self,q_json,q_idx):
        pair_sub_var = self.pair_sub_var.get()
        pair_obj_var = self.pair_obj_var.get()

        cur_dict = q_json.get()
      
        hoi_dict = {"subject_id":pair_sub_var,"object_id":pair_obj_var}


        id_in_json= q_idx.get()
        q_idx.put(id_in_json)

    


        if hoi_dict not in cur_dict[id_in_json]["hoi_annotations"]: #避免重复添加hoi_annotation信息

        
                cur_dict[id_in_json]["hoi_annotations"].append(hoi_dict)
                try:
                    vec = np.array(cur_dict[id_in_json]['annotations'][pair_obj_var]['center'])- \
                        np.array(cur_dict[id_in_json]['annotations'][pair_sub_var]['center'])

                    cur_dict[id_in_json]['annotations'][pair_sub_var]['vec'] = list(vec) 
                    cur_dict[id_in_json]['annotations'][pair_obj_var]['vec'] = list(vec*(-1))
                except:pass
                     


                print("after hoi added:\n",cur_dict[id_in_json])
            
                
      

        q_json.put(cur_dict)

    # def annotation(self,q_json,q_idx):
    #     category_id = self.sub_var.get()
    #     cur_dict = q_json.get()
        
    #     id_in_json = q_idx.get()
    #     q_idx.put(id_in_json)
    #     cur_dict[id_in_json]["annotations"][-1].update({"category_id":category_id})#更新最后那个的anno
    #     q_json.put(cur_dict)

    #     print("after bbx added:\n",cur_dict[id_in_json])

    def bbx_category_warning(self,Err):
        messagebox.showinfo(title='Warning', message="bbx below is Error!\n"+str(Err))   



