import argparse
parser = argparse.ArgumentParser()
parser.add_argument("mode", help="train | test")
mode = parser.parse_args().mode
# imprt = parser.parse_args().imprt

img_format = ['png','jpg']
subject_cls = {'person':1,'bicycle':2,'motorcycle':3,'car':4,'bus':5,'trunk':6,'face':7} 
if mode=="train":
    Hoi_cls ={'riding':1,'facing':2}
    Hoi_cls_What = {'bicycle':2,'motorcycle':3,'car':4,'bus':5,'trunk':6,'having':7,'no having':8}
else:
    Hoi_cls = {'riding non-motor vehicle':0,'others':1}


import_json = "./label_train.json"
# import_pic_path = 'Z:/02_dataset/qiuweiyu/to_fgm/csbank/'
import_pic_path = 'C:/Users/Administrator/Desktop/pigo_img'