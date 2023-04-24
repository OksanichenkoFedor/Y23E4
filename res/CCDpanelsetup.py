# Copyright (c) 2019 Esben Rossel
 # All rights reserved.
 #
 # Author: Esben Rossel <esbenrossel@gmail.com>
 #
 # Redistribution and use in source and binary forms, with or without
 # modification, are permitted provided that the following conditions
 # are met:
 # 1. Redistributions of source code must retain the above copyright
 #    notice, this list of conditions and the following disclaimer.
 # 2. Redistributions in binary form must reproduce the above copyright
 #    notice, this list of conditions and the following disclaimer in the
 #    documentation and/or other materials provided with the distribution.
 #
 # THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
 # ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 # IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 # ARE DISCLAIMED.  IN NO EVENT SHALL AUTHOR OR CONTRIBUTORS BE LIABLE
 # FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 # DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
 # OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 # HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 # LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
 # OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 # SUCH DAMAGE.

#python imports
from cgitb import text
from tkinter import ttk
import numpy as np
import serial

#application imports
import config
from CCDhelp import *
import CCDserial
import CCDfiles
from count_plot_array import *
from additional_panels import *

class buildpanel(tk.Frame):
  def __init__(self, master, CCDplot, SerQueue):
    CCDplot.master = self
    #geometry-rows for packing the grid
    device_row = 10
    shicg_row = 20
    prak_row = 30
    self.add_func_row = 40
    avg_row = 80
    collect_row = 90
    divide_row = 55
    choose_which_curse_row = 65
    self.choose_which_curse_row = 65
    pon_row = 70
    save_row = 100
    update_row = 100
    self.coord_row = 110
    progress_var = tk.IntVar()
    
    tk.Frame.__init__(self, master=None)

    self.plot_field = CCDplot
    #Create all widgets and space between them
    self.devicefields(device_row)
    #insert vertical space
    self.grid_rowconfigure(device_row+3, minsize=30)
    self.CCDparamfields(shicg_row)
    self.grid_rowconfigure(shicg_row+4, minsize=30)
    self.add_fun_params_fields(self.add_func_row)
    self.grid_rowconfigure(pon_row-2, minsize=30)
    self.plot_or_not_rbutton(pon_row)
    #self.grid_rowconfigure(avg_row - 2, minsize=30)
    self.avgfields(avg_row)
	#insert vertical space
    self.grid_rowconfigure(avg_row+2, minsize=30)
    self.collectfields(collect_row, SerQueue, progress_var)

    #self.divide_plot_buttons(divide_row)
    # vertical space
    self.grid_rowconfigure(collect_row+2, minsize=30)
    #self.plotmodefields(plotmode_row, CCDplot)
    #self.cursor_button(plotmode_row)

    # vertical space
    self.grid_rowconfigure(choose_which_curse_row + 2, minsize=30)
    self.saveopenfields(save_row, CCDplot)
    self.updateplotfields(update_row, CCDplot)
    # vertical space
    self.grid_rowconfigure(update_row + 2, minsize=30)
    #self.coordfield(self.coord_row)

    #self.sumintence(self.coord_row)

    self.updateplot(self.plot_field)
    config.already_started = True


  def devicefields(self, device_row):
    #device setup - variables, widgets and traces associated with the device entrybox
    #variables
    self.device_address = tk.StringVar()
    self.device_status = tk.StringVar()
    self.device_statuscolor = tk.StringVar()
    #widgets
    self.ldevice = tk.Label(self, text="Используемый порт:")
    self.ldevice.grid(column=0, row=device_row)
    self.edevice = tk.Entry(self, textvariable=self.device_address, justify='left')
    self.edevice.grid(column=1, row=device_row)   
    self.ldevicestatus = tk.Label(self, textvariable=self.device_status, fg="green")
    #setup trace to check if the device exists
    self.device_address.trace("w", lambda name, index, mode, Device=self.device_address, status=self.device_status, colr=self.ldevicestatus: self.DEVcallback(name, index, mode, Device, status, colr))
    self.device_address.set(config.port)
    self.ldevicestatus.grid(columnspan=2, row=device_row+1)
    #help button

  def avgfields(self, avg_row):
    # setup AVG entry
    self.lAVG = tk.Label(self, text="Усреднение:")
    self.lAVG.grid(column=0, row=avg_row)
    self.AVGscale = tk.Scale(self, orient='horizontal', from_=1, to=40)
    self.AVGscale.configure(command=self.AVGcallback)
    self.AVGscale.grid(column=1, row=avg_row, sticky="we")
    # help button
    self.bhavg = tk.Button(self, text="?", command=lambda helpfor=2: helpme(helpfor))
    #self.bhavg.grid(row=avg_row, column=3)

  def add_fun_params_fields(self, curr_row):
      self.for_fun_par = VariablesForFunction(self)
      self.for_fun_par.grid(row=curr_row,column=0,columnspan=2)

  def plot_or_not_rbutton(self, curr_row):
      self.plotmode_frame = tk.Frame(self)
      self.plotmode_frame.grid(row=curr_row, columnspan=3)
      self.pon_var = tk.IntVar()
      self.pon_chkb = tk.Checkbutton(self.plotmode_frame, text="Построить теоретическую зависимость",
                                    variable=self.pon_var, offvalue=0, onvalue=1)  # , state=tk.ACTIVE)
      if config.is_plotting:
          self.pon_chkb.select()
      else:
          self.pon_chkb.deselect()
      self.pon_chkb.grid(row=0, column=0, sticky="W")

      self.pon_var.trace("w", lambda name, index,
                                        mode, pon=self.pon_var : self.PONcallback(name, index, mode, pon))


  def PONcallback(self,name, index, mode, pl_or_np):
      config.is_plotting = pl_or_np.get()
      self.updateplot(self.plot_field)
	
  def CCDparamfields(self, shicg_row):
    #CCD parameters - variables, widgets and traces associated with setting ICG and SH for the CCD
    self.SHvalue = tk.StringVar()
    self.SHvalue.set(str(config.SHperiod))
    self.ICGvalue = tk.StringVar()
    self.ICGvalue.set(str(config.ICGperiod))
    self.tint = tk.StringVar()
    self.tint.set("Integration time is 0.1 ms")
    self.ICGSHstatus = tk.StringVar()
    self.ICGSHstatus.set("Корректная чувствительность.")
    self.ICGSHstatuscolor = tk.StringVar()
    #pulse timing tip
    self.ltipSHICG = tk.Label(self, text="ICG = n·SH")
    #self.ltipSHICG.grid(columnspan=2, row=shicg_row-1)
	#setup SH-entry
    self.lSH = tk.Label(self, text="Чувствительность:")
    self.lSH.grid(column=0, row=shicg_row)
    self.eSH = tk.Entry(self, textvariable=self.SHvalue, justify='right')
    self.eSH.grid(column=1, row=shicg_row)
    #setup ICG-entry
    self.lICG = tk.Label(self, text="ICG-period:")
    #self.lICG.grid(column=0, row=shicg_row+1)
    self.eICG = tk.Entry(self, textvariable=self.ICGvalue, justify='right')
    #self.eICG.grid(column=1, row=shicg_row+1)
    #setup ICGSH-status label
    self.lICGSH = tk.Label(self, textvariable=self.ICGSHstatus, fg="green")
    self.lICGSH.grid(columnspan=2, row=shicg_row+2)
    #integration time label
    self.ltint = tk.Label(self, textvariable=self.tint)
    #self.ltint.grid(columnspan=2, row=shicg_row+3)
    #setup traces to update tx-data
    self.SHvalue.trace("w", lambda name, index, mode, status=self.ICGSHstatus, tint=self.tint, colr=self.lICGSH, SH=self.SHvalue, ICG=self.ICGvalue: self.ICGSHcallback(name, index, mode, status, tint, colr, SH, ICG))
    self.ICGvalue.trace("w", lambda name, index, mode, status=self.ICGSHstatus, tint=self.tint, colr=self.lICGSH, SH=self.SHvalue, ICG=self.ICGvalue: self.ICGSHcallback(name, index, mode, status, tint, colr, SH, ICG))

  def SPCparamfields1(self, shicg_row):
      # CCD parameters - variables, widgets and traces associated with setting ICG and SH for the CCD
      self.start_value = tk.StringVar()
      self.start_value.set(str(config.start))
      self.end_value = tk.StringVar()
      self.end_value.set(str(config.end))
      self.l_start_value = tk.StringVar()
      self.l_start_value.set(str(config.light_start))
      self.l_end_value = tk.StringVar()
      self.l_end_value.set(str(config.light_end))
      self.SPECstatus = tk.StringVar()
      self.SPECstatus.set("Корректные параметры.")
      self.SPECstatuscolor = tk.StringVar()
      # pulse timing tip
      self.ltipSPEC = tk.Label(self, text="Настройки спектра")
      self.ltipSPEC.grid(columnspan=2, row=shicg_row - 1)
      # setup "start"
      self.lST = tk.Label(self, text="Левый пиксель: ")
      self.lST.grid(column=0, row=shicg_row)
      self.eST = tk.Entry(self, textvariable=self.start_value, justify='right')
      self.eST.grid(column=1, row=shicg_row)
      # setup "end"
      self.lEND = tk.Label(self, text="Правый пиксель:")
      self.lEND.grid(column=0, row=shicg_row + 1)
      self.eEND = tk.Entry(self, textvariable=self.end_value, justify='right')
      self.eEND.grid(column=1, row=shicg_row + 1)
      # setup "light start"
      self.lLST = tk.Label(self, text="Левая длина волны:")
      self.lLST.grid(column=0, row=shicg_row + 2)
      self.eLST = tk.Entry(self, textvariable=self.l_start_value, justify='right')
      self.eLST.grid(column=1, row=shicg_row + 2)
      # setup "end"
      self.lLEND = tk.Label(self, text="Правая длина волны:")
      self.lLEND.grid(column=0, row=shicg_row + 3)
      self.eLEND = tk.Entry(self, textvariable=self.l_end_value, justify='right')
      self.eLEND.grid(column=1, row=shicg_row + 3)
      # setup ICGSH-status label
      self.lISPEC = tk.Label(self, textvariable=self.SPECstatus, fg="green")
      self.lISPEC.grid(columnspan=2, row=shicg_row + 4)
      # setup traces to update tx-data
      self.start_value.trace("w", lambda name, index, mode, status=self.SPECstatus, colr=self.lISPEC,
                                     start_l=self.start_value, end_l=self.end_value, light_start_l=self.l_start_value,
                                     light_end_l=self.l_end_value: self.SpectrCB(name, index, mode, status,
                                                                                       colr, start_l, end_l,
                                                                                       light_start_l, light_end_l))
      self.end_value.trace("w", lambda name, index, mode, status=self.SPECstatus, colr=self.lISPEC,
                                         start_l=self.start_value, end_l=self.end_value,
                                         light_start_l=self.l_start_value,
                                         light_end_l=self.l_end_value: self.SpectrCB(name, index, mode, status,
                                                                                     colr, start_l, end_l,
                                                                                     light_start_l, light_end_l))
      self.l_start_value.trace("w", lambda name, index, mode, status=self.SPECstatus, colr=self.lISPEC,
                                         start_l=self.start_value, end_l=self.end_value,
                                         light_start_l=self.l_start_value,
                                         light_end_l=self.l_end_value: self.SpectrCB(name, index, mode, status,
                                                                                     colr, start_l, end_l,
                                                                                     light_start_l, light_end_l))
      self.l_end_value.trace("w", lambda name, index, mode, status=self.SPECstatus, colr=self.lISPEC,
                                       start_l=self.start_value, end_l=self.end_value,
                                       light_start_l=self.l_start_value,
                                       light_end_l=self.l_end_value: self.SpectrCB(name, index, mode, status,
                                                                                   colr, start_l, end_l,
                                                                                   light_start_l, light_end_l))

  def SPCparamfields(self, shicg_row):
      self.SPCpf = SPC_panel(self)
      self.SPCpf.grid(row=shicg_row, column=0, columnspan=3)

  def collectmodefields(self, continuous_row):
    #setup continuous vs one-shot
    self.collectmode_frame = tk.Frame(self)
    self.collectmode_frame.grid(row=continuous_row, columnspan=3)
    self.CONTvar = tk.IntVar()
    self.rcontinuous = tk.Radiobutton(self.collectmode_frame, text="Непрерывный поток", variable=self.CONTvar, value=1, command=lambda CONTvar=self.CONTvar: self.modeset(CONTvar))
    self.rcontinuous.grid(row=0, column=2, sticky="W")
    self.roneshot = tk.Radiobutton(self.collectmode_frame, text="Единичное измерение", variable=self.CONTvar, value=0, command=lambda CONTvar=self.CONTvar: self.modeset(CONTvar))
    self.roneshot.grid(row=0, column=1, sticky="W")
	#help button
    self.bhcollectmode = tk.Button(self, text="?", command=lambda helpfor=6: helpme(helpfor))
    self.bhcollectmode.grid(row=continuous_row, column=3)


  def collectfields(self, collect_row, SerQueue, progress_var):
    #setup collect and stop buttons
    self.progress = ttk.Progressbar(self, orient="horizontal",  maximum=10,  mode="determinate",  var=progress_var)
    self.bcollect = tk.Button(self, width=14, text="Получить данные", command=lambda panel=self, SerQueue=SerQueue, progress_var=progress_var: CCDserial.rxtx(panel, SerQueue, progress_var))
    self.bcollect.event_generate('<ButtonPress>', when='tail')
    self.bcollect.grid(row=collect_row, columnspan=2, sticky="EW", padx=5)
    self.CollNum = tk.IntVar()
    self.rfirstcoll= tk.Radiobutton(self, text="Первый", variable=self.CollNum, value=0,
                                      command=lambda CollNum=self.CollNum: self.collect_modeset(CollNum))
    #self.rfirstcoll.grid(row=collect_row, column=2, sticky="W")
    self.rsecondcoll = tk.Radiobutton(self, text="Второй", variable=self.CollNum, value=1,
                                   command=lambda CollNum=self.CollNum: self.collect_modeset(CollNum))
    #self.rsecondcoll.grid(row=collect_row, column=2, sticky="W")
    self.progress.grid(row=collect_row+1, columnspan=2, sticky="EW", padx=5)

  def divide_plot_buttons(self, curr_row):
      self.one_d_two = tk.Button(self, width=14, text="Поделить первый график на второй", command=self.COMM_one_d_two)
      self.one_d_two.grid(row=curr_row, column=0, columnspan=3, sticky="EW", padx=5)

      self.two_d_one = tk.Button(self, width=14, text="Поделить второй график на первый", command=self.COMM_two_d_one)
      self.two_d_one.grid(row=curr_row+1, column=0, columnspan=3,sticky="EW", padx=5)
      if config.drawed_first == 1 and config.drawed_second == 1:
          self.one_d_two.config(state=tk.NORMAL)
          self.two_d_one.config(state=tk.NORMAL)
      else:
          self.one_d_two.config(state=tk.DISABLED)
          self.two_d_one.config(state=tk.DISABLED)
 
  def plotmodefields(self, plotmode_row, CCDplot):
	#setup plot mode checkbuttons
    self.plotmode_frame = tk.Frame(self)
    self.plotmode_frame.grid(row=plotmode_row, columnspan=3)
    self.balance_var = tk.IntVar()
    self.rawplot_var = tk.IntVar()
    self.spectr_var = tk.IntVar()
    self.cinvert = tk.Checkbutton(self.plotmode_frame, text="Plot raw data", variable=self.rawplot_var, offvalue=1, onvalue=0)#, state=tk.ACTIVE)
    self.cinvert.deselect()
    #self.cinvert.grid(row=0, column=1, sticky="W")
    self.cbalance = tk.Checkbutton(self.plotmode_frame, text="Balance output", variable=self.balance_var, offvalue=0, onvalue=1)#, state=tk.ACTIVE)
    self.cbalance.select()
    #self.cbalance.grid(row=0, column=2, sticky="W")
    self.cspectr = tk.Checkbutton(self.plotmode_frame, text="Построить зависимость от длин волн", variable=self.spectr_var, offvalue=0,onvalue=1)  # , state=tk.ACTIVE)
    self.cspectr.deselect()
    self.cspectr.grid(row=0, column=0, sticky="W")
    self.grid_rowconfigure(plotmode_row+2, minsize=50)
    #setup traces
    self.rawplot_var.trace("w", lambda name, index, mode, invert=self.rawplot_var, plot=CCDplot: self.RAWcallback(name, index, mode, invert, plot))
    self.balance_var.trace("w", lambda name, index, mode, balance=self.balance_var, plot=CCDplot: self.BALcallback(name, index, mode, balance, plot))
    self.spectr_var.trace("w", lambda name, index, mode, spec=self.spectr_var, plot=CCDplot: self.SPCcallback(name, index, mode, spec, plot))

  def cursor_button(self, curr_row):
      self.bc_text = tk.StringVar()
      if config.is_clever_cursor == 0:
          self.bc_text.set("Включить умный курсор")
      else:
          self.bc_text.set("Выключить умный курсор")
      self.bcursor = tk.Button(self, width=20, textvariable=self.bc_text, command = self.change_cursor_rb)
      self.bcursor.grid(column = 1, row = curr_row + 2)

  def prak_rbutton(self, curr_row):
      self.ch_prak_var = tk.IntVar()
      if config.second_prak:
          self.ch_prak_var.set(1)
      else:
          self.ch_prak_var.set(0)

      self.l_ch_prak = tk.Label(self, text="Выполняемый эксперимент:")
      self.l_ch_prak.grid(row=curr_row, column=0, sticky="W")

      self.rb_first_prak = tk.Radiobutton(self, text="E3", variable=self.ch_prak_var, value=0,
                                       command=lambda ch_prak_var=self.ch_prak_var: self.choose_prak(ch_prak_var))
      self.rb_first_prak.grid(row=curr_row, column=1, sticky="W")
      self.rb_second_prak = tk.Radiobutton(self, text="E4", variable=self.ch_prak_var, value=1,
                                        command=lambda ch_prak_var=self.ch_prak_var: self.choose_prak(ch_prak_var))
      self.rb_second_prak.grid(row=curr_row, column=2, sticky="W")

  def choose_r_b(self, ch_row):
    # setup plot mode checkbuttons
    self.cursor_var = tk.IntVar()
    self.ch_r_b = ChRB_panel(self, self.cursor_var, self.ch_cursor)
    self.ch_r_b.grid(row = ch_row, column = 0, columnspan = 3)

  def crb_forget(self):
      self.ch_r_b.grid_forget()

  def sumintence(self, curr_row):
      self.int_pan = Intence_panel(self)
      self.int_pan.grid(row=curr_row, column=0, columnspan=2)

  def sumintence_forget(self):

      self.int_pan.destroy()
      #try:
      #    self.int_lb.grid_forget()
      #except:
      #    pass
      #self.int_lb["text"]="\t\t\t"


  def updateplotfields(self, update_row, CCDplot):
    self.bupdate = tk.Button(self, text="Update plot", command=lambda CCDplot=CCDplot: self.updateplot(CCDplot))
    #setup an event on the invisible update-plot button with a callback this thread can invoke in the mainloop
    self.bupdate.event_generate('<ButtonPress>', when='tail')

    #commented out, it's needed to inject an event into the tk.mainloop for updating the plot from the 'checkfordata' thread
    #self.bupdate.grid(row=update_row, columnspan=3, sticky="EW", padx=5)

  ### Callbacks for traces, buttons, etc ###
  def callback(self):
    self.bopen.config(state=tk.DISABLED)
    return()

  def COMM_one_d_two(self):
      co_one_two()
      self.plot_field.update_plot()

  def COMM_two_d_one(self):
      co_two_one()
      self.plot_field.update_plot()


  def choose_prak(self,is_second_prak):
      if is_second_prak.get():
          config.second_prak = True
          self.change_for_second_prak()
          self.updateplot(self.plot_field)
      else:
          config.second_prak = False
          self.change_for_first_prak()
          self.updateplot(self.plot_field)


  def change_for_second_prak(self):
      if config.objects_for_prak_created:
        self.sumintence_forget()
        self.boundsfields_forget()
        print("Меняем на вовчарин прак")
      self.update()

  def change_for_first_prak(self):
      config.objects_for_prak_created = True
      self.sumintence(self.coord_row)
      self.boundsfields(self.bds_row)
      print("Меняем на мой прак")
      self.update()


  def ICGSHcallback(self, name, index, mode, status, tint, colr, SH, ICG):
    try:
        config.SHperiod = np.uint32(int(float(SH.get())*2.0))
        config.ICGperiod = np.uint32(int(ICG.get()))
    except:
        pass
    self.print_tint = tk.StringVar()
    

    if (config.SHperiod < 1):
      config.SHperiod = 1
    if (config.ICGperiod < 1):
      config.ICGperiod = 1


    if ((config.ICGperiod % config.SHperiod) or (config.SHperiod < 20) or (config.ICGperiod < 14776)):
        if (config.SHperiod < 20):
            status.set("Слишком маленькая чувствительность!")
        else:
            status.set("Чувствительность должна быть делителем 50000!")
        colr.configure(fg="red")
        self.print_tint.set("invalid")
    else:
        status.set("Корректная чувствительность.")
        colr.configure(fg="green")
        if (config.SHperiod < 20000000):
            self.print_tint.set(str(config.SHperiod / 2000) + " ms")
        elif (config.SHperiod <= 1200000000):
            self.print_tint.set(str(config.SHperiod / 2000000) + " s")
        elif (config.SHperiod > 1200000000):
            self.print_tint.set(str(round(config.SHperiod / 120000000, 2)) + " min")


    #tint.set("Integration time is " + + " ms")
    tint.set("Integration time is " + self.print_tint.get())

  def SpectrCB(self, name, index, mode, status, colr, start_l, end_l, light_start_l, light_end_l):
      self.print_tint = tk.StringVar()
      try:
          start = np.uint32(int(start_l.get()))
          end = np.uint32(int(end_l.get()))
          light_start = np.uint32(int(light_start_l.get()))
          light_end = np.uint32(int(light_end_l.get()))

          if (start >= 0) and (end <= config.num_pixels) and (start < end) and (light_start > 0) and (
                  light_start < light_end):
              status.set("Корректные параметры.")
              colr.configure(fg="green")
              config.start = start
              config.end = end
              config.light_start = light_start
              config.light_end = light_end
          else:
              status.set("Недопустимые параметры.")
              colr.configure(fg="red")
              self.print_tint.set("invalid")
      except:
          status.set("Недопустимые параметры.")
          colr.configure(fg="red")
          self.print_tint.set("invalid")

  def modeset(self, CONTvar):
    config.AVGn[0]=CONTvar.get()

  def collect_modeset(self, var):
    config.number_collecting=var.get()

  def save_modeset(self, var):
    config.number_saving=var.get()

  def load_modeset(self, var):
    config.number_loading=var.get()

  def AVGcallback(self,AVGscale):
    config.AVGn[1] = np.uint8(self.AVGscale.get())

  def BDScallbackLeft(self, BGSscale):
    #print(config.intence_x0)
    #print("Left")

    config.intence_x0 = np.uint32(self.bdsl_scale.get())
    self.bdsr_scale["from_"] = config.intence_x0
    if config.already_started_left==False:
        config.already_started_left = True
        self.updateplot(self.plot_field)
        config.already_started_left = False

  def BDScallbackRight(self, BGSscale):
    #print(self.bdsr_scale.get())
    #print("Right")

    config.intence_x1 = np.uint32(self.bdsr_scale.get())
    self.bdsl_scale["to"]=config.intence_x1
    if config.already_started_right == False:
        config.already_started_right = True
        self.updateplot(self.plot_field)
        config.already_started_right = False

  def BDScallbackBot(self, BGSscale):

      config.bottom_bound = np.uint32(self.bds_bot_scale.get())
      self.bds_bot_value.set(config.bottom_bound)
      if config.already_started_bot == False:
          config.already_started_bot = True
          self.updateplot(self.plot_field)
          config.already_started_bot = False


  def BDScallbackBotEntry(self, name, index, mode, Value, status, colr):
    curr_value = Value.get()
    try:
        curr_value = np.uint32(curr_value)
        if curr_value<=config.max_bottom_bound and curr_value>=0:
            status.set("Корректное значение")
            colr.configure(fg="green")
            config.bottom_bound = curr_value
            self.bds_bot_scale.set(curr_value)
        else:
            status.set("Введено число выходящее за границы")
            colr.configure(fg="red")

    except:
        status.set("Введите целое число")
        colr.configure(fg="red")


    #try:
    #    ser = serial.Serial(config.port, config.baudrate, timeout=1)
    #    status.set("Порт активен")
    #    ser.close()
    #    colr.configure(fg="green")
    #except serial.SerialException:
    #    status.set("Порт неактивен")
    #    colr.configure(fg="red")

  def RAWcallback(self, name, index, mode, invert, CCDplot):
    config.datainvert = invert.get()
    if (config.datainvert == 0):
        self.cbalance.config(state=tk.DISABLED)
    else:
        self.cbalance.config(state=tk.NORMAL)
    self.updateplot(CCDplot)

  def SPCcallback(self, name, index, mode, invert, CCDplot):
    config.is_make_spec = invert.get()
    self.updateplot(CCDplot)

  def BALcallback(self, name, index, mode, balanced, CCDplot):
    config.balanced = balanced.get()
    self.updateplot(CCDplot)

  def DEVcallback(self, name, index, mode, Device, status, colr):
    config.port = Device.get()
    try:
        ser = serial.Serial(config.port, config.baudrate, timeout=1)
        status.set("Порт активен")
        ser.close()
        colr.configure(fg="green")
    except serial.SerialException:
        status.set("Порт неактивен")
        colr.configure(fg="red")


  def ch_cursor(self):
    config.curr_checking = self.cursor_var.get()

  def updateplot(self, CCDplot):

    CCDplot.update_plot(self)

  def update_coords(self, curr_checking, curr_ind):
      self.X_var.set("X: " + str(config.data[curr_checking][0][curr_ind]))
      self.crdX_lb["bg"] = "#777"
      self.Y_var.set("Y: " + str(config.data[curr_checking][1][curr_ind]))
      self.crdY_lb["bg"] = "#777"
      self.update()

  def update_intence(self, value):
      self.int_pan.IntenceVar.set(value)
      self.update()

  def saveopenfields(self, save_row, CCDplot):
        # setup save/open buttons

        self.bsave = tk.Button(self, text="Сохранить", width=14, state=tk.DISABLED,
                               command=lambda self=self: CCDfiles.savefile(self))
        self.bsave.grid(row=save_row, column=0, columnspan=2, sticky="EW")
        self.SaveNum = tk.IntVar()
        #self.rfirstsave = tk.Radiobutton(self, text="Первый", variable=self.SaveNum, value=0,
        #                                  command=lambda SaveNum=self.SaveNum: self.save_modeset(SaveNum))
        #self.rfirstsave.grid(row=save_row, column=1, sticky="W")
        #self.rsecondsave = tk.Radiobutton(self, text="Второй", variable=self.SaveNum, value=1,
        #                               command=lambda SaveNum=self.SaveNum: self.save_modeset(SaveNum))
        #self.rsecondsave.grid(row=save_row, column=2, sticky="W")

        self.bopen = tk.Button(self, text="Открыть", width=14,
                               command=lambda self=self, CCDplot=CCDplot: CCDfiles.openfile(self, CCDplot))
        self.bopen.grid(row=save_row+1, column=0, columnspan =2, sticky="EW")
        self.LoadNum = tk.IntVar()
        #self.rfirstload = tk.Radiobutton(self, text="Первый", variable=self.LoadNum, value=0,
        #                                 command=lambda LoadNum=self.LoadNum: self.load_modeset(LoadNum))
        #self.rfirstload.grid(row=save_row+1, column=1, sticky="W")
        #self.rsecondload = tk.Radiobutton(self, text="Второй", variable=self.LoadNum, value=1,
        #                                  command=lambda LoadNum=self.LoadNum: self.load_modeset(LoadNum))
        #self.rsecondload.grid(row=save_row+1, column=2, sticky="W")

        # help button




