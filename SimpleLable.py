from multiprocessing import Process, Queue, Lock
import Draw
import Gui


def start_label():
    q_json = Queue()  #队列，用于存储json数据,自动带锁
    q_idx = Queue()   #队列，用于存储图片
    dw = Draw.draw()
    gui = Gui.GUI()
    p1 = Process(target=dw.start_draw,args=(q_json,q_idx))# 创建两个子进程
    p2 = Process(target=gui.start_gui,args=(q_json,q_idx))
    p1.daemon = True#设置守护进程
    p2.daemon = True
    p1.start()
    p2.run() #在linux上p2.start()可以执行，但是在window有问题，不知道为啥，所以改成了p2.run()就可以了
    p1.join() #阻塞父进程，让父进程等待p1进程结束父进程才结束，因为父进程在产生子进程后会异步执行
    p2.terminate()#若p1进程结束就杀死p2进程


if __name__ == "__main__":
    start_label()
 
   