import threading
from time import sleep

class TimerHandler():
    def __init__(self, time, callback):
        self.time = time
        self.callback = callback
        self.timer = None
        self.reset_timer()

    def reset_timer(self):
        if self.timer:
            try:
                self.timer.cancel()
            except Exception as e:
                print(f"Error al cancelar el temporizador: {e}")

        self.timer = threading.Timer(self.time, self.callback)
        self.timer.start()
