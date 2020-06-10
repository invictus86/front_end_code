#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk

root = tk.Tk()
lb = tk.Label(root, text='网址;')
lb.grid(row=0, column=0)
addr = tk.StringVar(value='https://www.pynote.net')
en = tk.Entry(root, textvariable=addr)
en.grid(row=0, column=1)
root.mainloop()
