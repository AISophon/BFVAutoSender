import tkinter as tk
import tkinter.messagebox
from pynput.keyboard import Controller, Key
import threading
import ctypes
import time

keyboard = Controller()
stop_event = threading.Event()
window_title = "Battlefield™ V"
hwnd = ctypes.windll.user32.FindWindowW(None, window_title)


def display_messagebox():
    tk.messagebox.showinfo(title="未找到战地5", message="战地5程序未找到，请重试")


def press_enter():
    keyboard.press(Key.enter)
    time.sleep(0.1)
    keyboard.release(Key.enter)
    time.sleep(0.2)


def send_keyboard_messages(range_time, range_rest, messages):
    for _ in range(range_time):
        for message in messages:
            if stop_event.is_set():  # 检查是否请求停止
                return
            press_enter()
            keyboard.type(message)
            press_enter()
        time.sleep(range_rest)


class App:
    def __init__(self, master):
        self.master = master
        master.title("战地5公告机")
        master.geometry("618x420")
        master.resizable(False, False)

        self.messages = {
            "welcome": "welcome to tqm's server. the server is under bfv mini robot control.",
            "text": "ban 2a, ban shotgun. if someone breaks the rule, i will kick them.",
            "join": "you can join our qq group: 619982307 for more information and communication.",
        }

        # 验证输入框内容
        vcmd = (master.register(self.validate_input), "%P")

        self.create_widgets(vcmd)
        self.is_sending = False

    def create_widgets(self, vcmd):
        tk.Label(
            self.master,
            text="欢迎使用战地5公告机！如有问题请加QQ群：619982307",
            anchor="w",
            padx=15,
        ).pack(fill=tk.X)

        self.entry_range_time = self.create_entry("发送次数：", "10", vcmd)
        self.entry_range_rest = self.create_entry("间隔秒数：", "120", vcmd)

        tk.Label(
            self.master,
            text="注意：由于战地5限制，字符数限制80，必须全部为小写字母，不得使用中文字符",
            anchor="w",
            padx=15,
        ).pack(fill=tk.X)

        self.entry_welcome = self.create_entry(
            "欢迎内容：", self.messages["welcome"], vcmd
        )
        self.entry_text = self.create_entry("正文内容：", self.messages["text"], vcmd)
        self.entry_join = self.create_entry("加群内容：", self.messages["join"], vcmd)

        tk.Label(
            self.master,
            text="注意：输入法需切换为英语，不能使用微软拼音",
            anchor="w",
            padx=15,
        ).pack(fill=tk.X)

        self.start_button = tk.Button(
            self.master, text="开始发送", command=self.start_sending
        )
        self.start_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.stop_button = tk.Button(
            self.master, text="停止发送", command=self.stop_sending, state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=10, pady=10)

    def create_entry(self, label_text, default_value, vcmd):
        tk.Label(self.master, text=label_text, anchor="w", padx=15).pack(fill=tk.X)
        entry = tk.Entry(self.master, width=80, validate="key", validatecommand=vcmd)
        entry.pack(pady=5, anchor="c", padx=15)
        entry.insert(0, default_value)
        return entry

    def validate_input(self, proposed):
        # 限制输入框最多输入80个字符
        return len(proposed) <= 80

    def start_sending(self):
        self.start_button.config(state=tk.DISABLED)  # 禁用开始按钮
        self.stop_button.config(state=tk.NORMAL)  # 启用停止按钮
        stop_event.clear()  # 清除停止事件

        global hwnd
        if hwnd:
            ctypes.windll.user32.SetForegroundWindow(hwnd)  # 激活窗口
            time.sleep(0.5)  # 等待窗口激活
            try:
                range_time = int(self.entry_range_time.get())
                range_rest = int(self.entry_range_rest.get())
            except ValueError:
                range_time, range_rest = 10, 120
            messages = [
                self.entry_welcome.get(),
                self.entry_text.get(),
                self.entry_join.get(),
            ]
            time.sleep(5)  # 延迟5秒后开始发送
            threading.Thread(
                target=send_keyboard_messages, args=(range_time, range_rest, messages)
            ).start()
        else:
            display_messagebox()
            self.stop_sending()

    def stop_sending(self):
        stop_event.set()  # 设置停止事件
        self.start_button.config(state=tk.NORMAL)  # 恢复开始按钮
        self.stop_button.config(state=tk.DISABLED)  # 禁用停止按钮


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
