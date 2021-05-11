# -*- coding:utf-8 -*-  
import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
import os.path as osp
from random import shuffle
import sys
import time
import subprocess
import cv2
from collections import defaultdict,OrderedDict
import json

classes = ['person','bicycle','motorbike','car','bus','truck']
CURDIR = os.path.dirname(os.path.realpath(__file__)) 

def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

if __name__=='__main__':
    coco_dir="/media/ubuntu_data2/02_dataset/ppl/person_bike_motor/cimg_6"#可修改
    json_dir="/media/ubuntu_data2/02_dataset/ppl/person_bike_motor/cimg_6.json"

    coco_anndir=os.path.join(coco_dir,"annotation")
    json_data = OrderedDict()

    files=os.listdir(coco_anndir)#获取当前文件夹下所有的xml文件
    print("cur have {} sample".format(len(files)))
    #遍历文件
    for j,xmlfile in enumerate(files):
        if((j+1)%2000==0):
            # for index in range(len(classes)):
            #     print("cls==={},small_cnt={}".format(index,small_cnt[index]))
            print("files_num:{} current_file:{}".format(len(files),j))
        #获取car .xml全路径和.jpg全路径，并做判断
        xml_full_path=os.path.join(coco_anndir,xmlfile)
        # img_full_path=os.path.join(img_dir,xmlfile[:-4]+".jpg")
        print(xml_full_path)
        if not os.path.isfile(xml_full_path):
            print('{} is not file'.format(xml_full_path))
            continue

        img_attr = defaultdict(list)
        img_attr["img_id"] = j
        img_attr["hoi_annotations"] = []

        tree=ET.parse(xml_full_path)
        root = tree.getroot()
        # xml对应图片名
        imgname = root.find('filename').text
        #获取图片的width heigth
        size = root.find('size')
        imgW = int(size.find('width').text)
        imgH = int(size.find('height').text)

        #获取当前样本的object
        for obj in root.iter('object'):
            difficult = obj.find('difficult').text
            cls_name = obj.find('name').text
            if cls_name not in classes or int(difficult)==1:
                continue

            cls_id = classes.index(cls_name)#获取类名对应的索引
            xmlbox = obj.find('bndbox')
            b = [int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text), int(xmlbox.find('xmax').text), int(xmlbox.find('ymax').text)]
            # if (b[1] <= b[0]) or (b[3] <= b[2]):
            #     flag_bad = True
            #     break
            # if (b[0] < 0) or (b[2] < 0) or (b[1] > imgW) or (b[3] > imgH):
            #     flag_bad = True
            #     break
            sub_obj = OrderedDict()
            sub_obj["category_id"] = cls_id + 1 #weifa software start form 1
            sub_obj["bbox"] = b
            img_attr["annotations"].append(sub_obj)
        
        #print(img_attr)
        print(imgname)
        json_data[imgname] = img_attr
    
    print(json_data)
    json_str = json.dumps(json_data)
    with open(json_dir, 'w') as json_file:
        json_file.write(json_str)
    print("done!")
    
