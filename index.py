import time
import psutil
from tkinter import *
from tkinter import messagebox
import os
import threading
import sys
from hurry.filesize import size

class Client:
    def __init__(self):
        self.root = Tk()
        self.root.title("Bandwidth Monitor")
        self.root.geometry("560x320")
        try:
            self.root.iconbitmap(os.getcwd() + '/assets/icon.ico')
        except:
            messagebox.showerror("Icon not found.")
        self.running = True
        self.root.protocol("WM_DELETE_WINDOW", self.destroyed)
        self.bandwidth_text = StringVar()
        self.bandwidth_text.set("Current bandwidth: 0B/s")
        self.state_text = StringVar()
        self.state_text.set("Data used this session: 0B")
        self.data_used = 0
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
        self.state_label = Label(self.root, textvariable=self.state_text, height="1", anchor='w')
        self.the_label.config(font=("Arial", 26))
        self.bandwidth_label.config(font=("Arial", 20))
        self.state_label.config(font=("Arial", 20))

    def pack(self):
        self.the_label.pack(fill='x')
        self.bandwidth_label.pack(fill='both', padx="20", pady="20")
        self.state_label.pack(fill='both', padx="20", pady="20")

    def thread(self):
        old_value = 0    
        while self.running:
            new_value = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
            self.data_used += new_value - old_value
            if old_value:
                self.send_stat(new_value - old_value)
            old_value = new_value
            time.sleep(1)

    def send_stat(self, value):
        self.bandwidth_text.set("Current bandwidth: " + size(value) + "/s")
        self.state_text.set("Data used this session: " + size(self.data_used))
        

client = Client()