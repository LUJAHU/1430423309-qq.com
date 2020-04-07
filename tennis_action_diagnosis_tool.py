import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import tkinter.font as tf
from main import ready, shot, swing,aftershot
from tkinter import messagebox

video_path = ''
stage = ''

def select_file():
    global video_path
    video_path = tk.filedialog.askopenfilename()  # askopenfilename 1次上传1个；askopenfilenames1次上传多个
    print(video_path)
    file.insert(0, video_path)

def submit():
    global stage
    stage = cmb.get()
    if stage == 'Ready':
        ready(video_path)
        messagebox.showinfo(title='Info！', message='Finish analyze！')
    elif stage == 'Swing':
        swing(video_path)
        messagebox.showinfo(title='Info！', message='Finish analyze！')
    elif stage == 'Stroke':
        shot(video_path)
        messagebox.showinfo(title='Info！', message='Finish analyze！')
    elif stage == 'After stroke':
        aftershot(video_path)
        messagebox.showinfo(title='Info！', message='Finish analyze！')


window = tk.Tk()
window.title('Tennis tool')
window.iconbitmap('icon.ico')

ft = tf.Font(family='TimeNewRoman', size=14)
tk.Label(window, text="select video").grid(row=0)
tk.Label(window, text="select stage").grid(row=1)

file = tk.Entry(window,width=22)
file.grid(row=0, column=1,pady=10)
tk.Button(text="Browse", width=10,command=select_file).grid(row=0,  column=2, pady=5)
cmb = ttk.Combobox(window)
cmb.grid(row=1, column=1)
cmb['value'] = ('Ready','Swing','Stroke','After stroke')


tk.Button(text="submit", width=10,command=submit).grid(row=2, columnspan=3, pady=5)  # columnspan=3 跨三列


window.mainloop()
