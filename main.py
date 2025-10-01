import tkinter as tk
from tkinter import filedialog, messagebox
import serial
import threading

class ChannelLoaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Channel Loader v1.0")
        self.serial_conn = None

        self.port_label = tk.Label(root, text="COM Port:")
        self.port_label.pack()
        self.port_entry = tk.Entry(root)
        self.port_entry.pack()

        self.baud_label = tk.Label(root, text="Baud Rate:")
        self.baud_label.pack()
        self.baud_entry = tk.Entry(root)
        self.baud_entry.insert(0, "9600")
        self.baud_entry.pack()

        self.connect_btn = tk.Button(root, text="Connect", command=self.connect_serial)
        self.connect_btn.pack()

        self.upload_btn = tk.Button(root, text="Upload File", command=self.upload_file, state=tk.DISABLED)
        self.upload_btn.pack()

        self.download_btn = tk.Button(root, text="Download File", command=self.download_file, state=tk.DISABLED)
        self.download_btn.pack()

    def connect_serial(self):
        port = self.port_entry.get()
        baud = self.baud_entry.get()
        try:
            self.serial_conn = serial.Serial(port, baudrate=int(baud), timeout=1)
            messagebox.showinfo("Success", f"Connected to {port} at {baud} baud")
            self.upload_btn.config(state=tk.NORMAL)
            self.download_btn.config(state=tk.NORMAL)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def upload_file(self):
        file_path = filedialog.askopenfilename()
        if not file_path or not self.serial_conn:
            return
        threading.Thread(target=self._send_file, args=(file_path,)).start()

    def _send_file(self, file_path):
        try:
            with open(file_path, "rb") as f:
                data = f.read()
                self.serial_conn.write(data)
            messagebox.showinfo("Success", "File uploaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def download_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".bin")
        if not file_path or not self.serial_conn:
            return
        threading.Thread(target=self._receive_file, args=(file_path,)).start()

    def _receive_file(self, file_path):
        try:
            data = self.serial_conn.read(1024)
            with open(file_path, "wb") as f:
                f.write(data)
            messagebox.showinfo("Success", "File downloaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = ChannelLoaderApp(root)
    root.mainloop()
