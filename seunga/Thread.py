import time
from threading import Thread 

def one():
    i=0
    while True:
        print(i,"\n")
        i += 1
        time.sleep(1)

def two():
    while True:
        print("function2")
        time.sleep(1)

if __name__ == '__main__':
    proc = Thread(target=one, args=())
    proc2 = Thread(target=two, args=())
    proc.start()
    proc2.start()
