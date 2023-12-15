import sys
import threading
import gi
import json
#from nfc import Rfid
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib
import http.client
import time
from timeit  import Timer
from timer_handler import newTimer

class Temporizador:

    def __init__(self):
        self.x = 10 #nombre de segons
        th = threading.Thread(target = self.count)
        th.start()
    
    def count(self):
        x=10
        while(True):
            x=x-1
            time.sleep(1)
            if x == 0:
                self.logout()


class CourseManager: 

    def __init__(self):
        self.user = None
        self.uid = None
        self.table = None
        self.conn = http.client.HTTPConnection("localhost", 8080)
        self.login()
        self.flag = False
        

    def count(self):
        x = 5
        while(True):
            x=x-1
            time.sleep(1)
            if x == 0 and self.flag==True:
                    self.logout()
            else:
                self.flag=False
            
    def get(self, url):
        try:
            self.conn.request("GET", url)
            response = self.conn.getresponse()
            if response.status == 200:
            # Read and print the content of the response
                json_arr = response.read().decode('utf-8')  
                return json.loads(json_arr) #retornem l'objecte json
        finally:
            self.conn.close()


    def login(self):
        print ("Entra el teu uid: ")    #D1FDE202, 938B506
        self.uid = input()
        data = self.get("/CriticalDesignPBE/back/index.php/students?uid={}".format(self.uid))
        if data:
            self.user = data[0]['userName']
            print(data)
            print(self.user)
            self.consultarServer()

    def logout(self):
        self.user = None
        self.uid = None
        if self.conn:
            self.conn.close()
        self.login()

    def consultarServer(self):
        
        while(True):
            
            print("Introdueix el que vols veure: ")
            th = threading.Thread(target = self.count())
            th.start()
            self.table = input()
            
            if self.table:
                if self.table == 'logout':
                    self.logout()
                else:
                    self.aux = self.table.split("?") #mirem primera part de la query per saber si és marks i enviar uid
                    if (self.aux[0]=="marks" and self.uid):
                        if(len(self.aux)==1):
                            self.table = self.table + "?uid=" + self.uid
                    data = self.get("/CriticalDesignPBE/back/index.php/{}".format(self.table))
                    print(data)
                self.flag = True
            
course = CourseManager()

Gtk.main()
