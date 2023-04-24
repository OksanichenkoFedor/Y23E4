import tkinter as tk
import config
import numpy as np
from count_plot_array import count_wave

class ChRB_panel(tk.Frame):
    def __init__(self, master, var, command):
        self.master = master
        super().__init__(master)

        self.ch_lb = tk.Label(self, text="Настройка умного курсора")
        self.ch_lb.grid(row=0, column=0, columnspan=2)
        self.print_U = tk.Radiobutton(self, text="Первый", value=0, variable=var, command=command)
        self.print_U.grid(row=1, column=0, sticky="W")

        self.print_I = tk.Radiobutton(self, text="Второй", value=1, variable=var, command=command)
        self.print_I.grid(row=1, column=1, sticky="W")


class Intence_panel(tk.Frame):
    def __init__(self, master):
        self.master = master
        super().__init__(master)

        self.IntenceVar = tk.StringVar()
        self.int_lb = tk.Label(self, text="Полная интенсивность: ")
        self.int_lb.grid(column=0, row=0, sticky="W")
        self.crdX_lb = tk.Label(self, textvariable=self.IntenceVar)  # , background="#777")
        self.crdX_lb.grid(column=1, row=0, sticky="W")


class VariablesForFunction(tk.Frame):
    def __init__(self, master):
        self.master = master
        super().__init__(master)
        self.addAmpl(0)
        self.addDelta(10)
        self.addSmesch(20)
        self.addAlpha(30)
        self.addL0(40)

    def addAmpl(self, curr_row):
        self.ampl_label = tk.Label(self, text="Амплитуда : ")
        self.ampl_var = tk.StringVar()
        self.ampl_status = tk.StringVar()
        self.ampl_statuscolor = tk.StringVar()
        self.l_ampl_status = tk.Label(self, textvariable=self.ampl_status, fg="green")
        self.ampl_Entry = tk.Entry(self, textvariable=self.ampl_var, justify='left')

        self.ampl_var.trace("w", lambda name, index, mode, Value=self.ampl_var, status=self.ampl_status,
                                        colr=self.l_ampl_status: self.ClBckAmplEntry(name, index,
                                                                                     mode, Value,
                                                                                     status, colr))
        self.ampl_var.set(config.E4_ampl_var)

        self.ampl_label.grid(column=0, row=curr_row, sticky="we")
        self.ampl_Entry.grid(column=1, row=curr_row, sticky="we")
        self.l_ampl_status.grid(column=0, columnspan=2, row=curr_row + 5, sticky="we")

    def ClBckAmplEntry(self, name, index, mode, Value, status, colr):
        curr_value = Value.get()
        try:
            curr_value = np.float32(curr_value)
            status.set("Корректное значение")
            colr.configure(fg="green")
            config.E4_ampl_var = curr_value
        except:
            status.set("Введите вещественное число")
            colr.configure(fg="red")
        self.master.updateplot(self.master.plot_field)

    def addDelta(self, curr_row):
        self.delta_label = tk.Label(self, text="Ширина щели(м) : ")
        self.delta_var = tk.StringVar()
        self.delta_status = tk.StringVar()
        self.delta_statuscolor = tk.StringVar()
        self.l_delta_status = tk.Label(self, textvariable=self.delta_status, fg="green")
        self.delta_Entry = tk.Entry(self, textvariable=self.delta_var, justify='left')

        self.delta_var.trace("w", lambda name, index, mode, Value=self.delta_var, status=self.delta_status,
                                         colr=self.l_delta_status: self.ClBckDeltaEntry(name, index,
                                                                                        mode, Value,
                                                                                        status, colr))
        self.delta_var.set(config.E4_delta_var)

        self.delta_label.grid(column=0, row=curr_row, sticky="we")
        self.delta_Entry.grid(column=1, row=curr_row, sticky="we")
        self.l_delta_status.grid(column=0, columnspan=2, row=curr_row + 5, sticky="we")

    def ClBckDeltaEntry(self, name, index, mode, Value, status, colr):
        curr_value = Value.get()
        try:
            curr_value = np.float32(curr_value)
            status.set("Корректное значение")
            colr.configure(fg="green")
            config.E4_delta_var = curr_value
        except:
            status.set("Введите вещественное число")
            colr.configure(fg="red")
        self.master.updateplot(self.master.plot_field)

    def addSmesch(self, curr_row):
        self.smesch_label = tk.Label(self, text="Смещение(м) : ")
        self.smesch_var = tk.StringVar()
        self.smesch_status = tk.StringVar()
        self.smesch_statuscolor = tk.StringVar()
        self.l_smesch_status = tk.Label(self, textvariable=self.smesch_status, fg="green")
        self.smesch_Entry = tk.Entry(self, textvariable=self.smesch_var, justify='left')

        self.smesch_var.trace("w", lambda name, index, mode, Value=self.smesch_var, status=self.smesch_status,
                                          colr=self.l_smesch_status: self.ClBckSmeschEntry(name, index,
                                                                                           mode, Value,
                                                                                           status, colr))
        self.smesch_var.set(config.E4_smesch_var)

        self.smesch_label.grid(column=0, row=curr_row, sticky="we")
        self.smesch_Entry.grid(column=1, row=curr_row, sticky="we")
        self.l_smesch_status.grid(column=0, columnspan=2, row=curr_row + 5, sticky="we")

    def ClBckSmeschEntry(self, name, index, mode, Value, status, colr):
        curr_value = Value.get()
        try:
            curr_value = np.float32(curr_value)
            status.set("Корректное значение")
            colr.configure(fg="green")
            config.E4_smesch_var = curr_value
        except:
            status.set("Введите вещественное число")
            colr.configure(fg="red")
        self.master.updateplot(self.master.plot_field)

    def addAlpha(self, curr_row):
        self.alpha_label = tk.Label(self, text="Альфа : ")
        self.alpha_var = tk.StringVar()
        self.alpha_status = tk.StringVar()
        self.alpha_statuscolor = tk.StringVar()
        self.l_alpha_status = tk.Label(self, textvariable=self.alpha_status, fg="green")
        self.alpha_Entry = tk.Entry(self, textvariable=self.alpha_var, justify='left')

        self.alpha_var.trace("w", lambda name, index, mode, Value=self.alpha_var, status=self.alpha_status,
                                         colr=self.l_alpha_status: self.ClBckAlphaEntry(name, index,
                                                                                        mode, Value,
                                                                                        status, colr))
        self.alpha_var.set(config.E4_alpha_var)

        self.alpha_label.grid(column=0, row=curr_row, sticky="we")
        self.alpha_Entry.grid(column=1, row=curr_row, sticky="we")
        self.l_alpha_status.grid(column=0, columnspan=2, row=curr_row + 5, sticky="we")

    def ClBckAlphaEntry(self, name, index, mode, Value, status, colr):
        curr_value = Value.get()
        try:
            curr_value = np.float32(curr_value)
            status.set("Корректное значение")
            colr.configure(fg="green")
            config.E4_alpha_var = curr_value
        except:
            status.set("Введите вещественное число")
            colr.configure(fg="red")
        self.master.updateplot(self.master.plot_field)

    def addL0(self, curr_row):
        self.l0_label = tk.Label(self, text="L0(м) : ")
        self.l0_var = tk.StringVar()
        self.l0_status = tk.StringVar()
        self.l0_statuscolor = tk.StringVar()
        self.l_l0_status = tk.Label(self, textvariable=self.l0_status, fg="green")
        self.l0_Entry = tk.Entry(self, textvariable=self.l0_var, justify='left')

        self.l0_var.trace("w", lambda name, index, mode, Value=self.l0_var, status=self.l0_status,
                                      colr=self.l_l0_status: self.ClBckL0Entry(name, index,
                                                                               mode, Value,
                                                                               status, colr))
        self.l0_var.set(config.E4_l0_var)

        self.l0_label.grid(column=0, row=curr_row, sticky="we")
        self.l0_Entry.grid(column=1, row=curr_row, sticky="we")
        self.l_l0_status.grid(column=0, columnspan=2, row=curr_row + 5, sticky="we")

    def ClBckL0Entry(self, name, index, mode, Value, status, colr):
        curr_value = Value.get()
        try:
            curr_value = np.float32(curr_value)
            status.set("Корректное значение")
            colr.configure(fg="green")
            config.E4_l0_var = curr_value
        except:
            status.set("Введите вещественное число")
            colr.configure(fg="red")
        self.master.updateplot(self.master.plot_field)

