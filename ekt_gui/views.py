#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import scrolledtext


def add_symbol_rate(monty):
    frequency_min = StringVar(value='-50')
    name_entered = Entry(monty, width=4, textvariable=frequency_min)
    name_entered.grid(row=1, column=2)  # align left/West


def dvbs_11_dynamic_range_awng_min_level(window, monty):
    # global window, monty
    monty.destroy()
    # 创建一个容器,
    monty = ttk.LabelFrame(window, text="dvbs_11_dynamic_range_awng_min_level     Parameter setting item ")  # 创建一个容器，其父容器为window
    monty.grid(column=0, row=0, padx=4, pady=4)  # padx  pady   该容器外围需要留出的空余空间
    # aLabel = ttk.Label(monty, text="A Label")

    # level config
    a_label = ttk.Label(monty, text=" Level(dBm) : ")
    a_label.grid(row=1, column=0, padx=4, pady=4)

    a_label = ttk.Label(monty, text="Min_ini")
    a_label.grid(row=1, column=1, padx=4, pady=4)
    # Adding a Textbox Entry widget
    frequency_min = StringVar(value='-50')
    name_entered = Entry(monty, width=4, textvariable=frequency_min)
    name_entered.grid(row=1, column=2)  # align left/West

    a_label = ttk.Label(monty, text="    Max")
    a_label.grid(row=1, column=3, padx=4, pady=4)

    frequency_max = StringVar(value='-10')
    name_entered = Entry(monty, width=4, textvariable=frequency_max)
    name_entered.grid(row=1, column=4)

    a_label = ttk.Label(monty, text="    Level_1_step")
    a_label.grid(row=1, column=5, padx=4, pady=4)

    frequency_max = StringVar(value='10')
    name_entered = Entry(monty, width=3, textvariable=frequency_max)
    name_entered.grid(row=1, column=6)

    a_label = ttk.Label(monty, text="   Level_2_step")
    a_label.grid(row=1, column=7, padx=4, pady=4)

    frequency_max = StringVar(value='2')
    name_entered = Entry(monty, width=3, textvariable=frequency_max)
    name_entered.grid(row=1, column=8)

    a_label = ttk.Label(monty, text="  Level_3_step")
    a_label.grid(row=1, column=9, padx=4, pady=4)

    frequency_max = StringVar(value='0.5')
    name_entered = Entry(monty, width=3, textvariable=frequency_max)
    name_entered.grid(row=1, column=10)

    # frequency config
    a_label = ttk.Label(monty, text=" Frequency(KHz): ")
    a_label.grid(row=2, column=0, sticky=W, padx=4, pady=4)

    a_label = ttk.Label(monty, text="Min")
    a_label.grid(row=2, column=1, padx=4, pady=4)
    # Adding a Textbox Entry widget
    frequency_min = StringVar(value='950000')
    name_entered = Entry(monty, width=7, textvariable=frequency_min)
    name_entered.grid(row=2, column=2)  # align left/West

    a_label = ttk.Label(monty, text="    Max")
    a_label.grid(row=2, column=3, padx=4, pady=4)

    frequency_max = StringVar(value='2150000')
    name_entered = Entry(monty, width=8, textvariable=frequency_max)
    name_entered.grid(row=2, column=4)

    a_label = ttk.Label(monty, text="    Step")
    a_label.grid(row=2, column=5, padx=4, pady=4)

    frequency_max = StringVar(value='1000')
    name_entered = Entry(monty, width=6, textvariable=frequency_max)
    name_entered.grid(row=2, column=6)

    # constellation
    a_label = ttk.Label(monty, text="            Constellation:")
    a_label.grid(row=3, column=0, padx=4, pady=4, columnspan=2)

    chVarDis_QPSK = IntVar()
    check1 = Checkbutton(monty, text="QPSK", variable=chVarDis_QPSK)
    check1.select()
    check1.grid(row=4, column=0, sticky=E)

    chVarDis_8PSK = IntVar()
    check1 = Checkbutton(monty, text="8PSK", variable=chVarDis_8PSK)
    check1.select()
    check1.grid(row=4, column=3, sticky=E)

    chVarDis_QPSK_0_15 = IntVar()
    check1 = Checkbutton(monty, text="0.15  ", variable=chVarDis_QPSK_0_15)
    check1.select()
    check1.grid(row=5, column=0, sticky=E)

    chVarDis_QPSK_0_25 = IntVar()
    check1 = Checkbutton(monty, text="0.25  ", variable=chVarDis_QPSK_0_25)
    check1.select()
    check1.grid(row=6, column=0, sticky=E)

    chVarDis_QPSK_0_20 = IntVar()
    check1 = Checkbutton(monty, text="0.20 ", variable=chVarDis_QPSK_0_20)
    check1.select()
    check1.grid(row=5, column=1, sticky=W)

    chVarDis_QPSK_0_35 = IntVar()
    check1 = Checkbutton(monty, text="0.35 ", variable=chVarDis_QPSK_0_35)
    check1.select()
    check1.grid(row=6, column=1, sticky=W)

    chVarDis_8PSK_0_15 = IntVar()
    check1 = Checkbutton(monty, text="0.15 ", variable=chVarDis_8PSK_0_15)
    check1.select()
    check1.grid(row=5, column=3, sticky=E)

    chVarDis_8PSK_0_25 = IntVar()
    check1 = Checkbutton(monty, text="0.25 ", variable=chVarDis_8PSK_0_25)
    check1.select()
    check1.grid(row=6, column=3, sticky=E)

    chVarDis_8PSK_0_20 = IntVar()
    check1 = Checkbutton(monty, text="0.20 ", variable=chVarDis_8PSK_0_20)
    check1.select()
    check1.grid(row=5, column=4, sticky=W)

    chVarDis_8PSK_0_35 = IntVar()
    check1 = Checkbutton(monty, text="0.35 ", variable=chVarDis_8PSK_0_35)
    check1.select()
    check1.grid(row=6, column=4, sticky=W)

    a_label = ttk.Label(monty, text="Code Rate")
    a_label.grid(row=7, column=0, pady=8, columnspan=2, sticky=E)

    a_label = ttk.Label(monty, text=" Code Rate")
    a_label.grid(row=7, column=3, pady=8, columnspan=2)

    chVarDis_QPSK_coderate_1_2 = IntVar()
    check1 = Checkbutton(monty, text="1/2", variable=chVarDis_QPSK_coderate_1_2)
    check1.select()
    check1.grid(row=8, column=1, sticky=W)

    chVarDis_QPSK_coderate_3_5 = IntVar()
    check1 = Checkbutton(monty, text="3/5", variable=chVarDis_QPSK_coderate_3_5)
    check1.select()
    check1.grid(row=9, column=1, sticky=W)

    chVarDis_QPSK_coderate_2_3 = IntVar()
    check1 = Checkbutton(monty, text="2/3", variable=chVarDis_QPSK_coderate_2_3)
    check1.select()
    check1.grid(row=10, column=1, sticky=W)

    chVarDis_QPSK_coderate_3_4 = IntVar()
    check1 = Checkbutton(monty, text="3/4", variable=chVarDis_QPSK_coderate_3_4)
    check1.select()
    check1.grid(row=11, column=1, sticky=W)

    chVarDis_QPSK_coderate_4_5 = IntVar()
    check1 = Checkbutton(monty, text="4/5", variable=chVarDis_QPSK_coderate_4_5)
    check1.select()
    check1.grid(row=12, column=1, sticky=W)

    chVarDis_QPSK_coderate_5_6 = IntVar()
    check1 = Checkbutton(monty, text="5/6", variable=chVarDis_QPSK_coderate_5_6)
    check1.select()
    check1.grid(row=13, column=1, sticky=W)

    chVarDis_QPSK_coderate_6_7 = IntVar()
    check1 = Checkbutton(monty, text="6/7", variable=chVarDis_QPSK_coderate_6_7, state='disabled')
    check1.select()
    check1.grid(row=14, column=1, sticky=W)

    chVarDis_QPSK_coderate_7_8 = IntVar()
    check1 = Checkbutton(monty, text="7/8", variable=chVarDis_QPSK_coderate_7_8, state='disabled')
    check1.select()
    check1.grid(row=15, column=1, sticky=W)

    chVarDis_QPSK_coderate_8_9 = IntVar()
    check1 = Checkbutton(monty, text="8/9", variable=chVarDis_QPSK_coderate_8_9)
    check1.select()
    check1.grid(row=16, column=1, sticky=W)

    chVarDis_QPSK_coderate_9_10 = IntVar()
    check1 = Checkbutton(monty, text="9/10", variable=chVarDis_QPSK_coderate_9_10)
    check1.select()
    check1.grid(row=17, column=1, sticky=W)

    chVarDis_8PSK_coderate_1_2 = IntVar()
    check1 = Checkbutton(monty, text="1/2", variable=chVarDis_8PSK_coderate_1_2, state='disabled')
    check1.select()
    check1.grid(row=8, column=4, sticky=W)

    chVarDis_8PSK_coderate_3_5 = IntVar()
    check1 = Checkbutton(monty, text="3/5", variable=chVarDis_8PSK_coderate_3_5)
    check1.select()
    check1.grid(row=9, column=4, sticky=W)

    chVarDis_8PSK_coderate_2_3 = IntVar()
    check1 = Checkbutton(monty, text="2/3", variable=chVarDis_8PSK_coderate_2_3)
    check1.select()
    check1.grid(row=10, column=4, sticky=W)

    chVarDis_8PSK_coderate_3_4 = IntVar()
    check1 = Checkbutton(monty, text="3/4", variable=chVarDis_8PSK_coderate_3_4)
    check1.select()
    check1.grid(row=11, column=4, sticky=W)

    chVarDis_8PSK_coderate_4_5 = IntVar()
    check1 = Checkbutton(monty, text="4/5", variable=chVarDis_8PSK_coderate_4_5, state='disabled')
    check1.select()
    check1.grid(row=12, column=4, sticky=W)

    chVarDis_8PSK_coderate_5_6 = IntVar()
    check1 = Checkbutton(monty, text="5/6", variable=chVarDis_8PSK_coderate_5_6)
    check1.select()
    check1.grid(row=13, column=4, sticky=W)

    chVarDis_8PSK_coderate_6_7 = IntVar()
    check1 = Checkbutton(monty, text="6/7", variable=chVarDis_8PSK_coderate_6_7, state='disabled')
    check1.select()
    check1.grid(row=14, column=4, sticky=W)

    chVarDis_8PSK_coderate_7_8 = IntVar()
    check1 = Checkbutton(monty, text="7/8", variable=chVarDis_8PSK_coderate_7_8, state='disabled')
    check1.select()
    check1.grid(row=15, column=4, sticky=W)

    chVarDis_8PSK_coderate_8_9 = IntVar()
    check1 = Checkbutton(monty, text="8/9", variable=chVarDis_8PSK_coderate_8_9)
    check1.select()
    check1.grid(row=16, column=4, sticky=W)

    chVarDis_8PSK_coderate_9_10 = IntVar()
    check1 = Checkbutton(monty, text="9/10", variable=chVarDis_8PSK_coderate_9_10)
    check1.select()
    check1.grid(row=17, column=4, sticky=W)

    # a_label = Label(monty, text="AWGN:")
    # a_label.grid(row=5, column=6, pady=8, sticky=E)

    # radVar = IntVar()
    # # Next we are selecting a non-existing index value for radVar
    # radVar.set(0)
    # # 单选框
    # r1 = tk.Radiobutton(monty, text="On", value=0, variable=radVar, state=DISABLED)
    # r1.grid(row=5, column=7)
    #
    # r2 = tk.Radiobutton(monty, text="Off", value=1, variable=radVar, state=DISABLED)
    # r2.grid(row=5, column=8)

    a_label = Label(monty, text="Symbol Rate(KS/s):")
    a_label.grid(row=6, column=6, pady=8, sticky=E)

    symbol_rate_widget = Spinbox(monty, from_=1, to=10, width=3)
    symbol_rate_widget.grid(row=6, column=7)

    symbol_rate_1 = StringVar(value='50000')
    name_entered = Entry(monty, width=8, textvariable=symbol_rate_1)
    name_entered.grid(row=7, column=7,sticky=W)

    symbol_rate_1 = StringVar(value='10000')
    name_entered = Entry(monty, width=8, textvariable=symbol_rate_1)
    name_entered.grid(row=8, column=7, sticky=W)

    symbol_rate_1 = StringVar(value='27500')
    name_entered = Entry(monty, width=8, textvariable=symbol_rate_1)
    name_entered.grid(row=9, column=7, sticky=W)

    symbol_rate_1 = StringVar(value='45000')
    name_entered = Entry(monty, width=8, textvariable=symbol_rate_1)
    name_entered.grid(row=10, column=7, sticky=W)


    # chVarDis_QPSK = IntVar()
    # check1 = Checkbutton(monty, text="Code Rate", variable=chVarDis_QPSK)
    # check1.select()
    # check1.grid(row=7, column=0, sticky=E, pady=8)
    #
    # chVarDis_8PSK = IntVar()
    # check1 = Checkbutton(monty, text="Code Rate", variable=chVarDis_8PSK)
    # check1.select()
    # check1.grid(row=7, column=3, sticky=E, pady=8)

    # a_label = ttk.Label(monty, text=" QPSK")
    # a_label.grid(row=4, column=0, padx=4, pady=4)
    # # Adding a Textbox Entry widget
    # frequency_min = StringVar(value='8PSK')
    # name_entered = Entry(monty, width=7, textvariable=frequency_min)
    # name_entered.grid(row=4, column=2)  # align left/West

    # a_label = ttk.Label(monty, text="    Max")
    # a_label.grid(row=4, column=3, padx=4, pady=4)
    #
    # frequency_max = StringVar(value='2150000')
    # name_entered = Entry(monty, width=8, textvariable=frequency_max)
    # name_entered.grid(row=4, column=4)
    #
    # a_label = ttk.Label(monty, text="    Step")
    # a_label.grid(row=4, column=5, padx=4, pady=4)
    #
    # frequency_max = StringVar(value='1000')
    # name_entered = Entry(monty, width=6, textvariable=frequency_max)
    # name_entered.grid(row=4, column=6)

    # # Modified Button Click Function
    # def click_me():
    #     action.configure(text='Hello ' + name.get() + ' ' +
    #                           number_chosen.get())
    #
    # # Adding a Textbox Entry widget
    # name = StringVar()
    # name_entered = ttk.Entry(monty, width=12, textvariable=name)
    # name_entered.grid(column=0, row=1, sticky='W')  # align left/West
    #
    # # Adding a Button
    # action = ttk.Button(monty, text="Click Me!", command=click_me)
    # action.grid(column=2, row=1)
    #
    # # Creating three checkbuttons
    # ttk.Label(monty, text="Choose a number:").grid(column=1, row=0)
    # number = StringVar()
    # number_chosen = ttk.Combobox(monty, width=12, textvariable=number, state='readonly')
    # number_chosen['values'] = (1, 2, 4, 42, 100)
    # number_chosen.grid(column=1, row=1)
    # number_chosen.current(0)
    #
    # chVarDis = IntVar()
    # check1 = Checkbutton(monty, text="Disabled", variable=chVarDis, state='disabled')
    # check1.select()
    # check1.grid(column=0, row=4, sticky=W)
    #
    # chVarUn = IntVar()
    # check2 = Checkbutton(monty, text="UnChecked", variable=chVarUn)
    # check2.deselect()
    # check2.grid(column=1, row=4, sticky=W)
    #
    # chVarEn = IntVar()
    # check3 = Checkbutton(monty, text="Enabled", variable=chVarEn)
    # check3.deselect()
    # check3.grid(column=2, row=4, sticky=W)
    #
    # # GUI Callback function
    # def checkCallback(*ignoredArgs):
    #     # only enable one checkbutton
    #     if chVarUn.get():
    #         check3.configure(state='disabled')
    #     else:
    #         check3.configure(state='normal')
    #     if chVarEn.get():
    #         check2.configure(state='disabled')
    #     else:
    #         check2.configure(state='normal')
    #
    # # trace the state of the two checkbuttons
    # chVarUn.trace('w', lambda unused0, unused1, unused2: checkCallback())
    # chVarEn.trace('w', lambda unused0, unused1, unused2: checkCallback())
    #
    # # Using a scrolled Text control
    # scrol_w = 30
    # scrol_h = 3
    # scr = scrolledtext.ScrolledText(monty, width=scrol_w, height=scrol_h, wrap=WORD)
    # scr.grid(column=0, row=5, sticky='WE', columnspan=3)
    #
    # # First, we change our Radiobutton global variables into a list
    # colors = ["Blue", "Gold", "Red"]
    #
    # # We have also changed the callback function to be zero-based, using the list
    # # instead of module-level global variables
    # # Radiobutton Callback
    # def radCall():
    #     radSel = radVar.get()
    #     if radSel == 0:
    #         window.configure(background=colors[0])  # zero-based
    #     elif radSel == 1:
    #         window.configure(background=colors[1])  # using list
    #     elif radSel == 2:
    #         window.configure(background=colors[2])
    #
    # # create three Radiobuttons using one variable
    # radVar = IntVar()
    #
    # # Next we are selecting a non-existing index value for radVar
    # radVar.set(99)
    #
    # # Now we are creating all three Radiobutton widgets within one loop
    # for col in range(3):
    #     curRad = Radiobutton(monty, text=colors[col], variable=radVar,
    #                          value=col, command=radCall)
    #     curRad.grid(column=col, row=5, sticky=W)  # row=5 ... SURPRISE!
    #
    # # Create a container to hold labels
    # buttons_frame = ttk.LabelFrame(monty, text=' Labels in a Frame ')
    # buttons_frame.grid(column=0, row=7)

    def dvbs_11_dynamic_range_awng_max_level(window, monty):
        # global window, monty
        monty.destroy()
        # 创建一个容器,
        monty = ttk.LabelFrame(window, text=" Monty Python ")  # 创建一个容器，其父容器为win
        monty.grid(column=0, row=0, padx=10, pady=10)  # padx  pady   该容器外围需要留出的空余空间
        # aLabel = ttk.Label(monty, text="A Label")

        ttk.Label(monty, text="222").grid(column=1, row=0)  # 添加一个标签，并将其列设置为1，行设置为0
