from uiutils import Display
import simulate
from tkinter import *
from tkinter import ttk
from time import time
import math
import numpy as np
import scipy.ndimage

class Ui:
    def __init__(self):
        self.root = Tk()

        self.tickrate = 20
        self.enabled = True
        self.recentsc = 0
        self.tickratem = 0
        self.ticktime = np.zeros(50)
        self.tickratelist = np.zeros(50)
        self.inspectenabled = False

        self.sim = simulate.Simulation()

        self.display = Display(self.root)
        self.display.pack(fill='both', expand=1)

        self.options = list(self.sim.NAME.values())
        self.options = [self.options[i] for i in range(1, len(self.options))]

        ttk.OptionMenu(self.root, StringVar(), self.options[0], *self.options, command=self.updatepen).pack(side=LEFT)
        ttk.Scale(self.root, from_=5, to=50, value=20, orient=HORIZONTAL,command=self.updatetickrate).pack(side=LEFT)
        self.tickdisplay = ttk.Button(self.root, command=self.openinspect)
        self.tickdisplay.pack(side=LEFT)
        self.toggle=ttk.Button(self.root, text='Freeze', command=self.togglesim)
        self.toggle.pack(side=LEFT)
        ttk.Button(self.root, text='Step', command=self.step).pack(side=LEFT)
        self.hover = ttk.Label(self.root, text='')
        self.hover.pack(side=LEFT)
        ttk.Button(self.root, text='Reset', command=self.sim.RESET).pack(side=RIGHT)
        
        self.display.after_idle(self.tick)
        self.display.bind_pen(0, self.sim.CHANGE)

        self.root.title('Pixel Earth')
        self.root.wm_iconphoto(True, PhotoImage(file='assets/icon.png'))
        self.root.mainloop()

    def updatepen(self, v):
        self.display.bind_pen(list(self.sim.IDS.values()).index(self.sim.IDS[self.options.index(v)]), self.sim.CHANGE)

    def togglesim(self):
        if self.enabled:
            self.enabled = False
            self.toggle['text'] = 'Unfreeze'
            self.display.after_cancel(self.after)
            return
        self.enabled = True
        self.toggle['text'] = 'Freeze'
        self.after = self.display.after_idle(self.tick)

    def updatetickrate(self, v):
        self.tickrate = math.floor(float(v))

    def updateinspect(self):
        self.inspectcanvas1.delete("all")
        self.inspectcanvas2.delete("all")

        highest = max(np.max(self.tickratelist),1)
        lowest = np.min(self.tickratelist)
        for i in range(len(self.tickratelist)-1):
            self.inspectcanvas1.create_line(0,10,500,10, fill='gray70')
            self.inspectcanvas1.create_text(5,10,text=str(round(highest, 1))+'tps', fill='gray70', anchor=NW)
            self.inspectcanvas1.create_line(0,55,500,55, fill='gray70')
            self.inspectcanvas1.create_text(5,55,text=str(round((highest+lowest)/2,1))+'tps', fill='gray70', anchor=NW)

            self.inspectcanvas1.create_line(i * (500 / len(self.tickratelist)), 100-((self.tickratelist[i]-lowest)*(90/(highest-lowest))),  
                                            (i+1) * (500 / len(self.tickratelist)), 100-((self.tickratelist[i+1]-lowest)*(90/(highest-lowest))),
                                              fill='black')

        highest = max(np.max(self.ticktime),1)
        lowest = np.min(self.ticktime)
        for i in range(len(self.ticktime)-1):
            self.inspectcanvas2.create_line(0,10,500,10, fill='gray70')
            self.inspectcanvas2.create_text(5,10,text=str(round(highest, 1))+'ms', fill='gray70', anchor=NW)
            self.inspectcanvas2.create_line(0,55,500,55, fill='gray70')
            self.inspectcanvas2.create_text(5,55,text=str(round((highest+lowest)/2,1))+'ms', fill='gray70', anchor=NW)

            self.inspectcanvas2.create_line(i * (500 / len(self.ticktime)), 100-((self.ticktime[i]-lowest)*(90/(highest-lowest))),  
                                            (i+1) * (500 / len(self.ticktime)), 100-((self.ticktime[i+1]-lowest)*(90/(highest-lowest))),
                                              fill='black')
        
        self.inspectlabel['text'] = ('Tickrate: '+str(self.tickrate)+' / '+str(self.tickratem)+
                                     '     Max: '+str(round(np.max(self.tickratelist),1))+
                                     '     Min: '+str(round(np.min(self.tickratelist),1))+
                                     '     Avg: '+str(round(np.mean(self.tickratelist),1))
                                     +'\nTicktime: '+str(round(self.ticktime[-1],1))+'ms')

    def closeinspect(self):
        self.inspectenabled = False
        self.inspectwindow.destroy()

    def openinspect(self):
        if self.inspectenabled:
            self.inspectwindow.focus_set()
            return
        
        self.inspectenabled = True

        self.inspectwindow = Toplevel(self.root)
        self.inspectwindow.title('Inspect')
        self.inspectwindow.geometry('500x300')
        self.inspectwindow.resizable(0, 0)
        self.inspectwindow.protocol('WM_DELETE_WINDOW', self.closeinspect)

        ttk.Label(self.inspectwindow, text='Tickrate:', justify=LEFT).pack(fill=X)
        self.inspectcanvas1 = Canvas(self.inspectwindow, width=500, height=100)
        self.inspectcanvas1.pack()
        ttk.Label(self.inspectwindow, text='Ticktime:', justify=LEFT).pack(fill=X)
        self.inspectcanvas2 = Canvas(self.inspectwindow, width=500, height=100)
        self.inspectcanvas2.pack()

        self.inspectlabel = ttk.Label(self.inspectwindow, justify=LEFT)
        self.inspectlabel.pack(fill=X)
        self.updateinspect()
    
    def tick(self):
        if self.recentsc < math.floor(time()):
            self.recentsc = math.floor(time())
            scipy.ndimage.shift(self.tickratelist, -1, self.tickratelist, cval=self.tickratem)
            if self.inspectenabled:
                self.updateinspect()
            self.tickdisplay['text'] = str(self.tickrate)+' / '+str(self.tickratem)
            self.tickratem = 0

        self.tickratem += 1
        starttime = time()
        self.sim.TICK()
        self.display.render(self.sim.grid, simulate.Simulation.COLOR)
        self.hoverinfo()
        ticktime = max(1, math.floor(1000/self.tickrate-((time()-starttime)*1000)))
        scipy.ndimage.shift(self.ticktime, -1, self.ticktime, cval=ticktime)
        self.after = self.display.after(ticktime, self.tick)

    def hoverinfo(self):
        try:
            x,y = self.display.get_mouse()
            x,y = x/self.display.blockwidth, y/self.display.blockheight
            x,y = math.floor(x), math.floor(y)
            self.hover['text'] = self.sim.NAME[self.sim.grid[y][x]] + '    ' + str(self.sim.temp[y][x]) + '°C'
        except IndexError:
            pass

    def step(self):
        self.sim.TICK()
        self.display.render(self.sim.grid, simulate.Simulation.COLOR)
        self.hoverinfo()

if __name__ == '__main__':
    Ui()