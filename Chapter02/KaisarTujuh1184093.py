from threading import Thread
import os
import requests
from queue import Queue

queue = Queue()
digi = []

apiurl='https://digimon-api.herokuapp.com/api/digimon'
response = requests.get(apiurl)
html=response.json()


class Kaisar(Thread):
    def __init__(self, name, thread_number):
        Thread.__init__(self)
        self.name = name
        self.thread_number = thread_number

    def digiapi(self):
        for i in range(len(html)):
            hasil = html[i]["name"]
            digi.append(hasil)
            queue.put(digi)
            print(str(i)+'. Digi %s Appended from queue by %s' % (hasil, self.name))
    
    def run(self):
        print("Start Queue!")
        self.digiapi()


class Abdan(Thread):
    def __init__(self, name, thread_number, filename):
        Thread.__init__(self)
        self.name = name
        self.thread_number = thread_number
        self.filename = os.path.join(os.path.dirname(__file__), filename)
        
    def fileresult(self):
        for x in range(len(html)):
            diginame = digi.pop()
            f = open(self.filename+".txt", "w")
            f.write(diginame)
            f.close()
            digiitem = queue.get()
            print(str(x)+'. Digi %d-th Popped from queue by %s' % (len(digiitem), self.name))
            queue.task_done()     
        print('Read File: '+self.filename+'.txt')
        x = open(self.filename+".txt", "r")
        print(x.read()+'\n')
        x.close()
           
    def run(self):
        self.fileresult()
        print("Finish Queue!")
