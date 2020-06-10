#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext
from views import *

# 主窗口;

window = Tk()
monty = ttk.LabelFrame(window)
window.title("front_end_test")
window.resizable(width=False, height=False)  # 窗口大小不可改变
window.geometry("800x600+650+100")

# 顶级菜单,显示在窗口最上方
menubar = Menu(window)

# fmenu可理解为菜单容器,用于add菜单项

fmenu1 = Menu(window, tearoff=False)  # tearoff=True 表示这个菜单可以被拖拽出来
fmenu1.add_separator()  # 分割线
fmenu1.add_command(label='dvbs_11_dynamic_range_awng_max_level',  command=lambda: dvbs_11_dynamic_range_awng_max_level(window, monty))
fmenu1.add_separator()  # 分割线
fmenu1.add_command(label='dvbs_11_dynamic_range_awng_min_level', command=lambda: dvbs_11_dynamic_range_awng_min_level(window, monty))
fmenu1.add_separator()  # 分割线
fmenu1.add_command(label='dvbs_12_symbol_rate_step')
fmenu1.add_separator()  # 分割线
fmenu1.add_command(label='dvbs_15_symbol_err_rate')
fmenu1.add_separator()  # 分割线
fmenu1.add_command(label='dvbs_16_signal_acquisition_frequency_range')
fmenu1.add_separator()  # 分割线
fmenu1.add_command(label='dvbs_17_signal_tracking_frequency_range')


fmenu2 = Menu(window)
fmenu2.add_separator()  # 分割线
fmenu2.add_command(label='dvbs2_18_dynamic_range_awng_max_level')
fmenu2.add_separator()  # 分割线
fmenu2.add_command(label='dvbs2_18_dynamic_range_awng_min_level')
fmenu2.add_separator()  # 分割线
fmenu2.add_command(label='dvbs2_19_symbol_rate_step')
fmenu2.add_separator()  # 分割线
fmenu2.add_command(label='dvbs2_22_phase_distortion_test')
fmenu2.add_separator()  # 分割线
fmenu2.add_command(label='dvbs2_23_amplitude_distortion_test')
fmenu2.add_separator()  # 分割线
fmenu2.add_command(label='dvbs2_24_symbol_err_rate')
fmenu2.add_separator()  # 分割线
fmenu2.add_command(label='dvbs2_25_signal_acquisition_frequency_range')
fmenu2.add_separator()  # 分割线
fmenu2.add_command(label='dvbs2_26_signal_tracking_frequency_range')



fmenu3 = Menu(window)
fmenu3.add_separator()
fmenu3.add_command(label='菜单3-1')
fmenu3.add_separator()
fmenu3.add_command(label='菜单3-2')

fmenu4 = Menu(window)  # 创建了第四个菜单容器,add四个菜单容器,实现多级子菜单
fmenu4_1 = Menu(window)
fmenu4_1.add_command(label='菜单4-子菜单1-1')
fmenu4_1.add_command(label='菜单4-子菜单1-2')
fmenu4_2 = Menu(window)
fmenu4_2.add_command(label='菜单4-子菜单2-1')
fmenu4_2.add_command(label='菜单4-子菜单2-2')
fmenu4_3 = Menu(window)
fmenu4_3.add_command(label='菜单4-子菜单3-1')
fmenu4_3.add_command(label='菜单4-子菜单3-2')
fmenu4_4 = Menu(window)
fmenu4_4.add_command(label='菜单4-子菜单4-1')
fmenu4_4.add_command(label='菜单4-子菜单4-2')

# 将fmenu4_1,fmenu4_2,fmenu4_3,fmenu4_4四个菜单容器加入fmenu4菜单容器中

fmenu4.add_cascade(label='菜单4-子菜单1', menu=fmenu4_1)
fmenu4.add_cascade(label='菜单4-子菜单2', menu=fmenu4_2)
fmenu4.add_cascade(label='菜单4-子菜单3', menu=fmenu4_3)
fmenu4.add_cascade(label='菜单4-子菜单4', menu=fmenu4_4)

# 将“fmenu1、fmenu2、fmenu3、fmenu4”四个菜单容器加入顶级菜单中,并设置该菜单容器的label

menubar.add_cascade(label='DVB-S', menu=fmenu1)
menubar.add_cascade(label='DVB-S2', menu=fmenu2)
menubar.add_cascade(label='DVB-T', menu=fmenu3)
menubar.add_cascade(label='DVB-T2', menu=fmenu4)

window['menu'] = menubar  # 设置窗口的菜单为menubar

window.mainloop()
