from threading import Barrier, Thread
from time import ctime, sleep
import requests

num_runners = 3
finish_line = Barrier(num_runners)
runners = []
filename = "try.txt"


def api():
    url = "https://digimon-api.herokuapp.com/api/digimon"
    response = requests.get(url)
    html=response.json()
    string = "Name: "
    for i in range(len(html)):
        hasil = html[i]["name"]
        data = str(hasil)
        ent = "\n"+str(i)+". "
        string = string+ent+data
        runners.append(data)
    createfile(string)


def createfile(isi):
    f = open(filename, "w")
    f.write(str(isi))
    f.close()
        
        
def runner():
    api()
    sleep(2)
    finish_line.wait()
    name = runners.pop()
    sleep(2)
    print('%s reached the barrier at: %s \n' % (name, ctime()))
    finish_line.wait()


def main():
    threads = []
    print('START RACE!!!!')
    for i in range(num_runners):
        threads.append(Thread(target=runner))
        threads[-1].start()
    for thread in threads:
        thread.join()
    print('Race over!')
    return True



