import math
import sys
import tkinter
import os
from threading import Thread

from playsound import playsound

PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
TIMER_SPEED = 1000


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    # try:
    #     base_path = sys._MEIPASS
    # except Exception:
    #     base_path = os.path.abspath(".")
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def format_count(seconds):
    minutes = str(math.floor(seconds / 60)).zfill(2)
    seconds = str(seconds % 60).zfill(2)
    return f"{minutes}:{seconds}"


def play_gong():
    path = resource_path('gong.wav')
    print("Gong Path: " + path)
    playsound(path)


class Pomodoro:
    def __init__(self):
        self.start_pressed = False
        self.reps = 0
        self.checks = ""
        window = tkinter.Tk()
        window.title("Pomodoro")
        window.config(padx=100, pady=50, bg=YELLOW)
        self.active_fun = None
        self.text_title = tkinter.Label(text="Press Start!", font=("Arial", 45, "bold"), bg=YELLOW, fg=GREEN)
        window.columnconfigure(1, minsize=350)

        self.text_title.grid(column=1, row=0)

        canvas = tkinter.Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)

        tomato_image = tkinter.PhotoImage(file=resource_path("tomato.png"))
        canvas.create_image(100, 112, image=tomato_image)
        timer_text = canvas.create_text(100, 130, text="25:00", fill="white", font=(FONT_NAME, 25, "bold"))
        canvas.grid(column=1, row=1)
        self.timer_text = timer_text
        self.window = window
        self.canvas = canvas
        self.tomato_count = 0

        start_button = tkinter.Button(text="Start", command=self.start_button, highlightthickness=0)
        start_button.grid(column=0, row=2)

        reset_button = tkinter.Button(text="Reset", command=self.reset, highlightthickness=0)
        reset_button.grid(column=2, row=2)

        self.check_text = tkinter.Label(text="", font=("Arial", 45, "bold"), bg=YELLOW, fg=GREEN, highlightthickness=0)
        self.check_text.grid(column=1, row=3)

        window.mainloop()
        pass

    def trigger_gong(self):
        self.window.attributes('-topmost', 1)
        self.window.attributes('-topmost', 0)
        music_thread = Thread(target=play_gong)
        music_thread.start()

    def start_button(self):
        if self.start_pressed:
            return
        self.start()

    def start(self):
        self.start_pressed = True
        self.trigger_gong()
        self.reps += 1

        if self.reps % 8 == 0:
            self.text_title.config(text="Long Break", bg=YELLOW, fg=RED)
            count = LONG_BREAK_MIN * 60
            self.canvas.itemconfig(self.timer_text, text=format_count(count))
            self.active_fun = self.window.after(TIMER_SPEED, self.count_down, count - 1)
        elif self.reps % 2 == 0:
            self.text_title.config(text="Short Break", bg=YELLOW, fg=PINK, highlightthickness=0)
            count = SHORT_BREAK_MIN * 60
            self.canvas.itemconfig(self.timer_text, text=format_count(count))
            self.active_fun = self.window.after(TIMER_SPEED, self.count_down, count - 1)
        else:
            self.text_title.config(text="Work", bg=YELLOW, fg=GREEN)
            count = WORK_MIN * 60
            self.canvas.itemconfig(self.timer_text, text=format_count(count))
            self.active_fun = self.window.after(TIMER_SPEED, self.count_down, count - 1)

    def reset(self):
        self.start_pressed = False
        self.reps = 0
        if self.active_fun is not None:
            self.canvas.after_cancel(self.active_fun)

        self.checks = ""
        self.check_text.config(text=self.checks)

        self.canvas.itemconfig(self.timer_text, text=format_count(1500))
        self.tomato_count = 0

    def count_down(self, count):
        if count > 0:
            self.canvas.itemconfig(self.timer_text, text=format_count(count))
            self.active_fun = self.window.after(TIMER_SPEED, self.count_down, count - 1)
        else:
            self.start()
            if self.reps % 8 == 0:
                self.checks = ""
                self.check_text.config(text=self.checks)
            elif self.reps % 2 == 0:
                self.checks += "✓"
                self.check_text.config(text=self.checks)

    def update_count(self):
        self.tomato_count = self.tomato_count + 1
