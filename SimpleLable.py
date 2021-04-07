from multiprocessing import Process, Queue, Lock
import Draw
import Gui


def start_label():
    q_json = Queue()
    q_idx = Queue()
    dw = Draw.draw()
    gui = Gui.GUI()
    p1 = Process(target=dw.start_draw,args=(q_json,q_idx))
    p2 = Process(target=gui.start_gui,args=(q_json,q_idx))
    p1.daemon = True
    p2.daemon = True
    p1.start()
    p2.run()
    p1.join()
    p2.terminate()


if __name__ == "__main__":
    start_label()
 
   