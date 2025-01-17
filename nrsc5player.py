#!/usr/bin/env python3
# NRSC5 Player 
# Copyright (c) 2022 Jason Yu

import tkinter as tk
from tkinter import ttk
from PIL import ImageTk,Image 
import nrsc5service
import configparser
import io
import os
import sys
from collections import defaultdict


class NRSC5Player:

    def __init__(self, root):

        self.root = root

 
        #root.configure(bg='red')

        self.style = ttk.Style(self.root)
        #self.style.theme_use("clam")

        self.config = configparser.ConfigParser()
        if hasattr(sys, 'frozen'):
            basedir = os.path.dirname(sys.executable)
        else:
            basedir = sys.path[0]
        self.configpath = os.path.join(basedir, "config.ini")
        self.configwindow = None

        self.windowtitle = ("NRSC5 Player")

        self.info = {}
        self.info['title'] = "title"
        self.info['artist'] = "artist"
        self.info['program'] = "program"
        self.info['station'] = "station"
        self.info['slogan'] = "slogan"
        self.status = None

        root.title("NRSC5")
        self.root.resizable(width=True, height=True)

        self.defaultimage = Image.new('RGB', (200, 500), color='gray')

        self.infosection = ttk.Frame(self.root)  #, width=640, height=200)

        self.albumartlabel = ttk.Label(self.infosection,
                                       image=ImageTk.PhotoImage(
                                           self.defaultimage))
      
        self.infotext = ttk.Frame(self.infosection)
        self.infotext.pack(fill='both', expand=True)
        self.infolabel = {}
        self.infolabel['title'] = ttk.Label(self.infotext,
                                            text=self.info['title'],
                                            font=("-size 14"))
                                            
        self.infolabel['title'].pack()

        self.infolabel['artist'] = ttk.Label(self.infotext,
                                             text=self.info['artist'],
                                             font=("-size 11"))
        self.infolabel['artist'].pack()

        #self.infolabel['program'] = ttk.Label(self.infotext,
                                              #text=self.info['program'],
                                              #font=("-size 11"))
        #self.infolabel['program'].pack()

        #self.infolabel['station'] = ttk.Label(self.infotext,
                                              #text=self.info['station'],
                                              #font=("-size 11"))
        #self.infolabel['station'].pack()
        #self.infolabel['slogan'] = ttk.Label(self.infotext,
                                             #text=self.info['slogan'],
                                             #font=("-size 11"))
        #self.infolabel['slogan'].pack()

        #self.infosection.rowconfigure(0, weight=1)
        #self.infosection.rowconfigure(1, weight=0)
        #self.infosection.rowconfigure(2, weight=0)
        #self.programbar.grid_columnconfigure(0, weight=1)
        #self.programbar.grid_columnconfigure(3, weight=1)
        
        self.albumartlabel.pack()
        self.infotext.pack() 
       

        self.infosection.pack()

        self.parent_frame = ttk.Frame(self.infosection)

        self.freqbar = ttk.Frame(self.parent_frame)


        freqs = [[94.1, 98.1, 102.1], [104.5, 101.1, 102.9]]
        for row, freq_row in enumerate(freqs):
            for col, freq in enumerate(freq_row):
                button = ttk.Button(self.freqbar, text=str(freq), command=lambda f=freq:
        self.change_frequency(f), width=7)
                button.grid(row=row+1, column=col+1, sticky="ew") 

        self.freqbar.pack() 
        
        self.programbar = ttk.Frame(self.parent_frame)
        self.programbtn = {}

        for x in range(4):
            self.programbtn[x] = ttk.Button(
                 self.programbar, command=lambda y=x: self.setprogram(y),width=5,)
            
                   
        for i in range(4):
             self.programbar.columnconfigure(i+1, weight=1)

        self.programbar.pack(anchor="center")

        self.parent_frame.pack(expand=True)


        self.controlsection = ttk.Frame(self.infosection)

        self.tunerbar = ttk.Frame(self.controlsection)
        ttk.Label(self.tunerbar, text="Frequency:").pack(side="left",
                                                         fill="x",
                                                         padx=(0, 2))
        self.freqvar = tk.DoubleVar(master=self.tunerbar, value=87.5)
        freqentry = ttk.Spinbox(self.tunerbar,
                                textvariable=self.freqvar,
                                from_=87.5,
                                to=107.9,
                                increment=0.2,
                                 wrap=False,
                                width=7)
        freqentry.pack(side="left", fill="x", padx=(0, 2), pady=(5, 5))
        freqentry.bind('<Return>', self.freqreturn)
        self.tunerbar.pack(side="top", fill="x") 


       
        self.buttonbar = ttk.Frame(self.controlsection)
        ttk.Button(self.buttonbar, text="Play", width=6,
                   command=self.play).grid(row=0, column=0)
        ttk.Button(self.buttonbar, text="Stop", width=6,
                   command=self.stop).grid(row=0, column=1)
        self.buttonbar.pack(side="top", fill="x")

        ttk.Button(self.buttonbar,
                   text="Conf",
                   width=6,
                   command=self.openconfigwindow).grid(row=0, column=2)



        self.buttonbar.pack(side="top", fill="x")
        self.buttonbar.grid_columnconfigure(0, weight=1)
        self.buttonbar.grid_columnconfigure(1, weight=1)
       
        self.volumesection = ttk.Frame(self.controlsection)
        self.volumevar = tk.IntVar()
        self.volumevar.set(100)
        self.volumeslider = ttk.Scale(self.volumesection,
                                      from_=0,
                                      to=100,
                                      orient='horizontal',
                                      variable=self.volumevar,
                                      command=self.setvolume)
        self.volumeslider.pack(side="right")
        self.volumelabel = ttk.Label(self.volumesection,
                                     text=self.volumevar.get(),
                                     width=3)
        self.volumelabel.pack(side="top", fill="x", pady=(0, 0))
        self.volumesection.pack(side="left", fill="x", expand=True)

        self.infosection.pack(side="top", fill="x")

        self.controlsection.pack()

        self.infosection.columnconfigure(1, weight=1)
        self.infosection.columnconfigure(1, weight=1)
        self.infosection.rowconfigure(0, weight=1)
        self.infosection.rowconfigure(1, weight=0)
        self.infosection.rowconfigure(2, weight=0)


        self.popup_menu = tk.Menu(self.root, tearoff=0)
        self.popup_menu.add_command(label="Configuration",
                                    command=self.openconfigwindow)

        self.theme_menu = tk.Menu(self.root, tearoff=0)
        self.popup_menu.add_cascade(label="Theme", menu=self.theme_menu)
        self.themevar = tk.StringVar()
        self.themevar.set(self.style.theme_use())
        for theme_name in self.style.theme_names():
            self.theme_menu.add_radiobutton(label=theme_name,
                                            command=self.settheme,
                                            variable=self.themevar)

        self.trafficmenuitem = self.popup_menu.add_command(
            label="Traffic Map",
            command=self.opentrafficwindow,
            state="disabled")

        self.popup_menu.add_command(label="Exit", command=self.onclose)

        self.infosection.bind("<Button-3>", self.popup)
        for child in self.infosection.winfo_children():
            child.bind("<Button-3>", self.popup)
        for child in self.infotext.winfo_children():
            child.bind("<Button-3>", self.popup)

        self.programvar = tk.IntVar()
        self.hostvar = tk.StringVar()
        self.devicevar = tk.IntVar()
        self.cachevar = tk.BooleanVar()



        self.statusbar = ttk.Frame(self.root)
        self.statuslabel = ttk.Label(self.statusbar,
                                     text="Disconnected",
                                     relief=tk.SUNKEN,
                                     anchor=tk.W)
        self.statuslabel.pack(fill="both", expand=True)
        #self.statusbar.grid(row=0, column=1, sticky='E')
        self.statusbar.pack(anchor="e") 

        self.root.protocol("WM_DELETE_WINDOW", self.onclose)

        self.service = nrsc5service.NRSC5service()
        self.service.ui = self

        self.trafficimage = defaultdict(dict)
        self.trafficimageparts = defaultdict(dict)
        self.trafficwindow = None

        self.loadconfig()
        #self.resetdisplay()

        self.root.update()
        xscreen = self.root.winfo_screenwidth() / 2
        yscreen = self.root.winfo_screenheight() / 2.5
        xwindow = self.root.winfo_reqwidth() / 2
        ywindow = self.root.winfo_reqheight() / 2
        xpos = int(xscreen - xwindow)
        ypos = int(yscreen - ywindow)
        self.root.geometry(f"+{xpos}+{ypos}")

    def popup(self, event):
        try:
            self.popup_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.popup_menu.grab_release()

    def opentrafficwindow(self):
        if self.trafficwindow is not None:
            return
        self.trafficwindow = tk.Toplevel(self.root)
        self.trafficwindow.resizable(0, 0)
        self.trafficwindow.title("Traffic - " + self.windowtitle)
        trafficframe = ttk.Frame(self.trafficwindow)
        trafficframe.pack()

        self.newimg = ImageTk.PhotoImage(
            Image.new('RGB', (200, 200), color=(194, 187, 96)))
        for row in range(3):
            for col in range(3):
                self.trafficimage[row][col] = tk.Label(trafficframe,
                                                       borderwidth=0,
                                                       image=self.newimg)
                self.trafficimage[row][col].grid(column=col,
                                                 row=row,
                                                 padx=0,
                                                 pady=0)

        self.trafficwindow.protocol("WM_DELETE_WINDOW",
                                    self.ontrafficwindowclose)
        self.updatetrafficimage()

    def ontrafficwindowclose(self):
        if self.trafficwindow:
            self.trafficwindow.destroy()
        self.trafficwindow = None

    def settrafficimagepart(self, data, row, col):
        img = Image.open(io.BytesIO(data))
        self.trafficimageparts[row][col] = ImageTk.PhotoImage(img)
        self.popup_menu.entryconfig("Traffic Map", state="normal")
        self.updatetrafficimage()

    def updatetrafficimage(self):
        if self.trafficwindow is not None:
            for row in range(3):
                for col in range(3):
                    try:
                        self.trafficimage[row][col].configure(
                            image=self.trafficimageparts[row][col])
                    except:
                        continue

    def openconfigwindow(self):
        if self.configwindow is not None:
            return
        self.configwindow = tk.Toplevel(self.root)
        self.configwindow.resizable(0, 0)
        self.configwindow.title("Configuration")

        configframe = ttk.Frame(self.configwindow, borderwidth=10)
        configframe.pack()

        hostvarlabel = ttk.Label(configframe, text="rtl_tcp Host:")
        hostvarlabel.grid(column=0, row=0, padx=2, pady=2, sticky=tk.E)
        hostvarentry = ttk.Entry(configframe, textvariable=self.hostvar)
        hostvarentry.grid(column=1, row=0, pady=2, sticky=tk.W)

        devicevarlabel = ttk.Label(configframe, text="Device Index:")
        devicevarlabel.grid(column=0, row=1, padx=2, sticky=tk.E)
        devicevarentry = ttk.Entry(configframe, textvariable=self.devicevar)
        devicevarentry.grid(column=1, row=1, pady=2, sticky=tk.W)

        cachevarlabel = ttk.Label(configframe, text="Cache Logos:")
        cachevarlabel.grid(column=0, row=2, padx=2, sticky=tk.E)
        cachevarbutton = ttk.Checkbutton(configframe,
                                         text="Enable",
                                         variable=self.cachevar,
                                         onvalue=True,
                                         offvalue=False)
        cachevarbutton.grid(column=1, row=2, pady=2, sticky=tk.W)

        savebutton = ttk.Button(configframe,
                                text="Save",
                                command=self.saveconfigwindow)
        savebutton.grid(columnspan=2, column=0, row=4)

        self.configwindow.protocol("WM_DELETE_WINDOW",
                                   self.onconfigwindowclose)
        self.configwindow.update()

        xoffset = self.root.winfo_x() + (self.root.winfo_width() / 2)
        yoffset = self.root.winfo_y() + (self.root.winfo_height() / 2)
        xconfig = self.configwindow.winfo_width() / 2
        yconfig = self.configwindow.winfo_height() / 2
        xpos = int(xoffset - xconfig)
        ypos = int(yoffset - yconfig)
        self.configwindow.geometry(f"+{xpos}+{ypos}")
        self.configwindow.focus()





    def change_frequency(self, new_frequency):
        self.freqvar.set(new_frequency)
        self.play()

    def saveconfigwindow(self):
        self.saveconfig()
        self.onconfigwindowclose()

    def onconfigwindowclose(self):
        if self.configwindow:
            self.configwindow.destroy()
        self.configwindow = None

    def settheme(self):
        try:
            if self.themevar.get():
                self.style.theme_use(self.themevar.get())
            else:
                self.themevar.set(self.style.theme_use())
        finally:
            return

    def freqreturn(self, event):
        self.play()

    def updatewindowtitle(self):
        titleparts = []
        if self.service != None:
            if self.info['artist'] != None:
                titleparts.append(self.info['artist'])
            if self.info['title'] != None:
                titleparts.append(self.info['title'])
            if len(titleparts) < 1 and self.info['program'] != None:
                titleparts.append(self.info['program'])
            if len(titleparts) < 1 and self.info['station'] != None:
                titleparts.append(self.info['station'])
                if self.info['slogan'] != None:
                    titleparts.append(self.info['slogan'])
        titleparts.append(self.windowtitle)
        self.root.title(" - ".join(titleparts))

    def updateinfo(self):
        for id in self.infolabel:
            self.infolabel[id].config(text=self.info[id])
            self.infolabel[id].config(wraplength=self.infotext.winfo_width())
            self.infolabel[id].update_idletasks()
        self.updatewindowtitle()

    def settitle(self, input):
        self.info['title'] = input
        self.updateinfo()

    def setartist(self, input):
        self.info['artist'] = input
        self.updateinfo()

    def setprogramname(self, input):
        self.info['program'] = input
        self.updateinfo()

    def setstationname(self, input):
        self.info['station'] = input
        self.updateinfo()

    def setslogan(self, input):
        self.info['slogan'] = input
        self.updateinfo()

    def setalbumart(self, img):
        wwidth = self.albumartlabel.winfo_width() - 4
        wheight = self.albumartlabel.winfo_height() - 4
        dim = max(wwidth, wheight, 200)
        self.albumart = ImageTk.PhotoImage(img.resize((dim, dim)))
        self.albumartlabel.configure(image=self.albumart)

    def setalbumartfile(self, newalbumart):
        img = Image.open(newalbumart)
        self.setalbumart(img)

    def setalbumartdata(self, imagedata):
        if imagedata is not None:
            img = Image.open(io.BytesIO(imagedata))
        else:
            img = self.defaultimage
        self.setalbumart(img)

    def setprogrambutton(self, id, name):
        maxlength = 13
        if name and len(name) > maxlength:
            name = name[:maxlength - 3] + "..."
        self.programbtn[id].config(state="normal", text=name)

    def resetdisplay(self):
        for id in self.info:
            self.info[id] = None
        for id in self.infolabel:
            self.infolabel[id].config(text="")  #todo?
        for id in self.programbtn:
            btntext = "HD", id + 1
            self.programbtn[id].config(state="disabled", text=btntext)
        self.updatewindowtitle()
        self.setalbumartdata(None)
        self.ontrafficwindowclose()
        self.popup_menu.entryconfig("Traffic Map", state="disabled")

    def setstatus(self, input, *args):
        self.status = input % args
        self.statuslabel.config(text=self.status)
        self.statuslabel.update_idletasks()

    def setprogram(self, prog):
        self.programvar.set(prog)
        self.service.setprogram(prog)

    def setvolume(self, event):
        self.volumelabel.configure(text=self.volumevar.get())
        if self.service:
            self.service.setvolume(self.volumevar.get() * 0.01)

    def loadconfig(self):
        self.config.read(self.configpath)
        if 'frequency' in self.config['DEFAULT']:
            self.freqvar.set(self.config['DEFAULT']['frequency'])
            self.service.setfrequency(self.freqvar.get())
        if 'program' in self.config['DEFAULT']:
            self.programvar.set(self.config['DEFAULT']['program'])
            self.service.program = self.programvar.get()
        if 'volume' in self.config['DEFAULT']:
            self.volumevar.set(self.config['DEFAULT']['volume'])
            self.setvolume(None)
        if 'host' in self.config['DEFAULT']:
            self.hostvar.set(self.config['DEFAULT']['host'])
        if 'cache' in self.config['DEFAULT']:
            self.cachevar.set(self.config['DEFAULT']['cache'])
        if 'theme' in self.config['DEFAULT']:
            self.themevar.set(self.config['DEFAULT']['theme'])
            self.settheme()

    def saveconfig(self):
        self.config['DEFAULT'] = {
            'frequency': self.freqvar.get(),
            'program': self.programvar.get(),
            'volume': self.volumevar.get(),
            'host': self.hostvar.get(),
            'device': self.devicevar.get(),
            'cache': self.cachevar.get(),
            'theme': self.themevar.get(),
        }
        with open(self.configpath, 'w') as configfile:
            self.config.write(configfile)

    def play(self):
        try:
            freqvar = self.freqvar.get()
        except Exception:
            self.setstatus("Invalid frequency")
            return
        changefreq = self.service.frequency != freqvar
        if changefreq or not self.service.playing:
            if self.service.playing:
                self.stop()
            if changefreq and self.service.frequency != 0:
                self.programvar.set(0)
                self.resetdisplay()
            self.service.setfrequency(freqvar)
            self.service.program = self.programvar.get()
            self.service.host = self.hostvar.get()
            self.service.cachelogos = self.cachevar.get()
            self.service.deviceid = self.devicevar.get()
            self.service.run()

    def stop(self):
        self.service.stop()
        #self.resetdisplay()
        #self.updatewindowtitle()

    def onclose(self):
        self.stop()
        self.saveconfig()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    #root.tk.call('tk', 'scaling', 1.0)
    NRSC5Player(root)
    root.mainloop()
