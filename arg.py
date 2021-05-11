import argparse
parser = argparse.ArgumentParser()
parser.add_argument("mode", help="train | test")
mode = parser.parse_args().mode

img_format = ['png','jpg']
subject_cls = {'person':1,'face':7} 
if mode=="train":
    Hoi_cls ={'with':1,'without':0}
else:
    Hoi_cls = {'with':0,'without':1}

import_json = "./label_train.json"
# import_pic_path = 'Z:/02_dataset/qiuweiyu/to_fgm/csbank/'
import_pic_path = 'Z:\\gwf\\dataset\\wf'