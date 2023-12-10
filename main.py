import sys
import threading
import gi
import json
#from nfc import Rfid
import urllib.request
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib
from TimerHandler import TimerHandler

class CourseManager: 

    def __init__(self):
        self.user = None
        self.uid = None
        self.user_lock = threading.Lock()
        self.timer_handler = TimerHandler(10, self.logout)
        self.login()
        while(self.user is not None):
            self.consultarServer()

    def login(self):
        print ("Entra el teu uid: ")    #7399A831, 1099031C
        self.uid = input()
        url = "http://localhost:8080/CriticalDesignPBE/back/index.php/students?uid={}".format(self.uid)
        request = urllib.request.Request(url)
        try:
            with urllib.request.urlopen(request) as response:
            # Read the response data
                json_array = response.read().decode('utf-8')
                data = json.loads(json_array)
                with self.user_lock:
                    self.user = data[0]['userName']
            print('sessió iniciada: ' + self.user)
        except urllib.error.URLError as e:
            print(f"Error al realizar la solicitud: {e}")
        timer_thread = threading.Thread(target=self.timer_handler.reset_timer)
        timer_thread.start()
        
    def logout(self):
        with self.user_lock:
            self.user = None
            self.uid = None
        self.login()

    def consultarServer(self):
        print("Introduzca lo que quiera ver: ")
        self.table = input()
        if self.table:
            self.timer_handler.reset_timer()
            if self.table == 'logout':
                self.logout()
            elif self.uid is not None:
                url = "http://localhost:8080/CriticalDesignPBE/back/index.php/{}?uid={}".format(self.table, self.uid)
                request = urllib.request.Request(url)
                with urllib.request.urlopen(request) as response:
                    json_array = response.read().decode('utf-8')
                    print(json_array);

course = CourseManager();
Gtk.main()
