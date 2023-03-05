import pyautogui
import keyboard
import time
import tkinter as tk
import threading

class ClickerGUI:
    def __init__(self, master):
        self.master = master
        master.title("自动点击器")

        self.label1 = tk.Label(master, text="点击间隔（秒）：")
        self.label1.grid(row=0, column=0, padx=5, pady=5)

        self.entry1 = tk.Entry(master, width=10)
        self.entry1.grid(row=0, column=1, padx=5, pady=5)
        self.entry1.insert(0, "1.5")

        self.button1 = tk.Button(master, text="开始点击", command=self.start_clicker)
        self.button1.grid(row=1, column=0, padx=5, pady=5)

        self.button2 = tk.Button(master, text="停止点击", command=self.stop_clicker)
        self.button2.grid(row=1, column=1, padx=5, pady=5)

        self.status_label = tk.Label(master, text="等待命令")
        self.status_label.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        keyboard.add_hotkey('F2', self.start_clicker)
        keyboard.add_hotkey('F3', self.stop_clicker, suppress=True)

    def start_clicker(self, event=None):
        if not self.validate_input():
            return

        global is_running, click_interval
        click_interval = float(self.entry1.get())
        if not is_running.is_set():
            is_running.set()
            self.status_label.config(text="点击中...")
            threading.Thread(target=self.clicker_thread).start()
        else:
            self.status_label.config(text="点击中...")

    def stop_clicker(self, event=None):
        global is_running
        is_running.clear()
        self.status_label.config(text="已停止")

    def clicker_thread(self):
        while is_running.is_set():
            pyautogui.click()
            time.sleep(click_interval)

    def validate_input(self):
        try:
            click_interval = float(self.entry1.get())
            if click_interval <= 0:
                raise ValueError
        except ValueError:
            self.status_label.config(text="错误：请输入大于零的数字")
            return False
        return True

if __name__ == "__main__":
    is_running = threading.Event()
    is_running.clear()
    root = tk.Tk()
    my_gui = ClickerGUI(root)
    root.mainloop()

    keyboard.unhook_all()
