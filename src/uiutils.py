from tkinter import *
import math

class Display(Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, background='black')
        self.x, self.y = 0, 0
        self.bind('<Motion>', self.set_mouse)
    
    def render(self, grid, colormap):
        self.delete("all")
        self.blockwidth = self.winfo_width() / len(grid[0])
        self.blockheight = self.winfo_height() / len(grid)
        
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                self.create_rectangle(self.blockwidth * x, self.blockheight * y, self.blockwidth * (x+1), self.blockheight * (y+1), fill=colormap[grid[y][x]])
    
    def bind_pen(self, penid, grid):
        self.unbind('<Button-1>')
        self.unbind('<B1-Motion>')
        self.bind('<Button-1>', lambda e: self._pen(e, penid, grid))
        self.bind('<B1-Motion>', lambda e: self._pen(e, penid, grid))

    def _pen(self, e, penid, grid):
        grid(math.floor(e.x/self.blockwidth), math.floor(e.y/self.blockheight), penid)

    def set_mouse(self, e):
        self.x, self.y = e.x, e.y

    def get_mouse(self):
        return self.x, self.y
