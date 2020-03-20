from shutil import copy2 as copy
from ftplib import FTP
from sys import exc_info
import threading
import os

serverAddress = "buttons.go.ro"
serverPort = 21
username = "Silvia"
password = ""

class FTPThread (threading.Thread):
    def __init__(self, threadID, dirListLocal):
        self.threadID = threadID
        self.dirListLocal = dirListLocal
        threading.Thread.__init__(self)
    def run(self):
        connectionThr = FTP()
        connectionThr.connect(serverAddress,serverPort)
        connectionThr.login(username,password)
        print("Process " + str(self.threadID) + " online. Proceeding.")
        for dir in self.dirListLocal:
            connectionThr.cwd(str(dir))
            connectionThr.retrbinary("RETR contents.pak", open(str(dir) + ".pak", "wb").write)
            connectionThr.cwd("..")
        print("Process " + str(self.threadID) + " finished transferring.")
        connectionThr.close()

print("Cleaning up old mods")
files = os.listdir()
for file in files:
    if(file[:-4:-1] == "kap"):
        os.remove(file)
print("Done cleaning up")
print("Estabilishing FTP connection to " + serverAddress + ":" + str(serverPort))

try:
    connection = FTP()
    connection.connect(serverAddress,serverPort)
    connection.login(username,password)
    dirs = connection.nlst()
    assoc = dict()
    print("Connection succesful! Retrieving folders.")
    for dir in dirs:
        connection.cwd(dir)
        assoc[dir] = connection.size("contents.pak")
        connection.cwd("..")
    sortedAssoc = {k: v for k, v in sorted(assoc.items(), key=lambda item: item[1], reverse = True)}
    dirList1 = []
    dirList2 = []
    ct=1
    for key in sortedAssoc.keys():
        if ct % 2 == 1:
            dirList1.append(key)
        else:
            dirList2.append(key)
        ct = ct+1
    connection.close()
    print("Folders retrieved! Starting file transfer.")
    thread1 = FTPThread(1,dirList1)
    thread2 = FTPThread(2,dirList2)
    thread1.start()
    thread2.start()
except:
    exc = exc_info()[0]
    print("Uh oh, something went wrong")
    print("Error: {}".format(exc))