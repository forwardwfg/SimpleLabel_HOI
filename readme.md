# Simple_label 使用说明

## 一.环境
* python37
* tkinter

## 二.标注步骤
* 1.在图中绘制一个边框
* 2.在界面<pealse select a subject for each bbox>中给选择边框对象,并确定  
* 3.继续在图中绘制一个边框  
* 4.重复2  
* 5.绘制两个及其以上边框请根据实际情况添加它们的关系  
    * 5.1 在 pealse select <person,object> pair 选项中选择对应的bbx,序号对应图像所示的数字  
    * 5.2 在 pealse select a relation for the pair 选项中选择关系  
    * 5.3 在 pealse select a object of the relation 选项中选择关系的对象  

## 三.其他操作
* 1.按下z键,撤回上一步操作
* 2.按下b键，撤回上一站图片


## 四.错误提示
* 所有给两个边框对象选择关系的时候，如果有错误提示，则为最后两次所绘制的边框中有一个忘记选择对象了，这时候需要按下z键撤回至没有选择类别的边框，并重新选择

## 五.其他
* label_train.json 标记数据
* last_visited.txt 记录最后访问的图片
* skip.txt 记录了没有标注的图片名字



