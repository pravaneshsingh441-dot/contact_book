import tkinter as tk
print('starting')
try:
    root = tk.Tk()
    print('created root')
    root.withdraw()
    print('withdrawn')
except Exception as e:
    print('exception', e)
print('done')
