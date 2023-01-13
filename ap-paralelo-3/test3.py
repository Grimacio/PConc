from threading import Thread
import os
import time
r,w =os.pipe()
f = os.fdopen(r)
g = os.fdopen(w, 'w')

def t1():
    global g
    i=0
    while True:
        i+=1
        g.write(str(i)+"\n")
        time.sleep(1)

def t2():
    global f
    while True:
        s = f.readline()
        print(s)

thread1 = Thread(target=t1)
thread2= Thread(target=t2)
thread1.start()
thread2.start()
thread1.join()
thread2.join()