import sys
import threading
import gi
import json
import requests
#from nfc import Rfid
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib

import http.client
import time
from timeit  import Timer
from timer_handler import newTimer

class CourseManager(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_default_size(800, 800)
        self.user = None
        self.uid = None
        self.table = None
        self.conn = http.client.HTTPConnection("localhost", 8080)
        self.entry = None

        # Configurar la interfaz gráfica
        self.box = Gtk.VBox(spacing=6)
        self.label = Gtk.Label()
        self.label.set_text("Acerca la tarjeta")
        self.box.pack_start(self.label, True, True, 0)
        self.add(self.box)
        self.show_all()

        self.input_thread = threading.Thread(target=self.read_user_input)
        self.input_thread.daemon = True
        self.input_thread.start()

        self.create_entry("Introduce lo que quieras ver:")
        
    def get(self, url):
        try:
            self.conn.request("GET", url)
            response = self.conn.getresponse()
            if response.status == 200:
                json_arr = response.read().decode('utf-8')  
                return json.loads(json_arr) #retornem l'objecte json
        finally:
            self.conn.close()
        
    def login(self):
        self.uid = input()
        data = self.get("/CriticalDesignPBE/back/index.php/students?uid={}".format(self.uid))
        if data:
            self.user = data[0]['userName']
            GLib.idle_add(self.update_label, "Welcome: " + self.user)
            
            
            
    def update_label(self, text):
        self.label.set_text(text) 
        self.show_all()

    def read_user_input(self):
        while True:
            self.login()

    def create_entry(self, text):
        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text(text)
        self.entry.connect("activate", lambda entry: self.consultaThread(entry = self.entry))
        self.box.pack_start(self.entry, True, True, 0)

    def consultaThread(self, entry):  #creem un thread per consultar el server de forma concurrent
        text = entry.get_text()
        thread1 = threading.Thread(target= self.consultarServer, args=(text, ))  #li passem el que esta escrit i el uid
        thread1.start()
        
    def consultarServer(self, text):
        self.table = text
        if self.table == 'logout':
            self.logout()
        else:
            self.aux = self.table.split("?") #mirem primera part de la query per saber si és marks i enviar uid
            if (self.aux[0]=="marks" and self.uid):
                if(len(self.aux)==1):
                    self.table = self.table + "?uid=" + self.uid
            data = self.get("/CriticalDesignPBE/back/index.php/{}".format(self.table))
            print(data)

win = CourseManager()
win.connect("destroy", Gtk.main_quit)
Gtk.main()
