import time
import psutil
from tkinter import *
import threading
import sys
from hurry.filesize import size

class Client:
    def __init__(self):
        self.root = Tk()
        self.root.title("Bandwidth Monitor")
        self.root.geometry("500x200")
        self.running = True
        self.root.protocol("WM_DELETE_WINDOW", self.destroyed)
        self.bandwidth_text = StringVar()
        self.bandwidth_text.set("Bandwidth: 0B/s")
        self.initialize_attributes()
        self.thread = threading.Thread(target=self.thread)
        self.thread.start()
        self.pack()
        self.root.mainloop()

    def destroyed(self):
        self.running = False
        self.root.quit()

    def initialize_attributes(self):
        self.the_label = Label(self.root, text="Bandwidth Monitor", bg="#3e3e3e", fg="#fff", height="3")
        self.bandwidth_label = Label(self.root, textvariable=self.bandwidth_text, height="1", anchor='w')
        # self.state_label = Label(self.root, text="State: Good", height="1", anchor='w')
        self.the_label.config(font=("Arial", 26))
        self.bandwidth_label.config(font=("Arial", 20))
        #self.state_label.config(font=("Courier", 20))
    
    def pack(self):
        self.the_label.pack(fill='x')
        self.bandwidth_label.pack(fill='both', padx="20", pady="20")
        #self.state_label.pack(fill='both', padx="20")

    def thread(self):
        old_value = 0    
        while self.running:
            new_value = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
            if old_value:
                self.send_stat(new_value - old_value)
            old_value = new_value
            time.sleep(1)

    def send_stat(self, value):
        self.bandwidth_text.set("Bandwidth: " + size(value) + "/s")
        

client = Client()