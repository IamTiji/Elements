import random
import numpy as np
import copy

WID = 30
HEI = 30

def INCLUDES(self, type, tag):
    if isinstance(tag, str):
        try:self.TAGS[type].index(tag)
        except:
            return self.NAME[type] == tag
        else:return True
    else:
        for t in tag:
            if INCLUDES(self, type, t):
                return True
        return False
        
class Simulation:
    def __init__(self):
        self.RESET()

    def RESET(self):
        grid = []
        grid.append([-1 for x in range(WID+2)])
        tmp = [(0, -1)[x==0 or x==WID+1] for x in range(WID+2)]
        for x in range(HEI):
            grid.append(tmp)
        grid.append([-1 for x in range(WID+2)])
        self.grid = np.array(grid)
        self.temp = np.full((WID+2,HEI+2), 1000)

    def TICK(self):
        order = [(x, y) for x in range(1,WID+1) for y in range(1,HEI+1)]
        random.shuffle(order)

        for o in order:
            self.grid[o[1]-1:o[1]+2,o[0]-1:o[0]+2] = self.IDS[self.grid[o[::-1]]](self.grid[o[1]-1:o[1]+2, o[0]-1:o[0]+2], self.temp[o[1], o[0]])
            
            self.temp[o[1]-1,o[0]] = (self.temp[o[1],o[0]] + self.temp[o[1]-1,o[0]])/2.005 
            self.temp[o[1]+1,o[0]] = (self.temp[o[1],o[0]] + self.temp[o[1]+1,o[0]])/2.005 
            self.temp[o[1],o[0]+1] = (self.temp[o[1],o[0]] + self.temp[o[1],o[0]+1])/2.005
            self.temp[o[1],o[0]-1] = (self.temp[o[1],o[0]] + self.temp[o[1],o[0]-1])/2.005

    def CHANGE(self,x,y,v):
        if x > 0 and y > 0 and x < WID+1 and y < HEI+1:
            self.grid[y][x] = v
            self.temp[y][x] = self.DEFAULTTEMP[v]

    def air(surround, temp):
        return surround

    def sand(surround, temp):
        out = copy.deepcopy(surround)
        if temp > 2000:
            out[1][1] = 9
            return out
            
        if INCLUDES(__class__, surround[2][1], ['empty','liquid','gas']):
            out[1][1] = surround[2][1]
            out[2][1] = 1
            return out
        if (INCLUDES(__class__, surround[2][0], ['empty','liquid','gas']) and 
            INCLUDES(__class__, surround[2][2], ['empty','liquid','gas']) and 
            INCLUDES(__class__, surround[1][0], ['empty','liquid','gas']) and 
            INCLUDES(__class__, surround[1][2], ['empty','liquid','gas'])):
            if random.random() < 0.5:
                out[1][0] = 1
                out[1][1] = surround[1][0]
            else:
                out[1][2] = 1
                out[1][1] = surround[1][2]
            return out
        if (INCLUDES(__class__, surround[2][0], ['empty','liquid','gas']) and 
            INCLUDES(__class__, surround[2][1], ['soild','Sand']) and 
            INCLUDES(__class__, surround[1][0], ['empty','liquid','gas'])):
            out[1][1] = surround[1][0]
            out[1][0] = 1
            return out
        if (INCLUDES(__class__, surround[2][2], ['empty','liquid','gas']) and 
            INCLUDES(__class__, surround[2][1], ['soild','Sand']) and 
            INCLUDES(__class__, surround[1][2], ['empty','liquid','gas'])):
            out[1][1] = surround[1][2]
            out[1][2] = 1
            return out
        else:
            return out
        
    def water(surround, temp):
        out = copy.deepcopy(surround)
        if temp > 100:
            out[1][1] = 3
            return out
        if temp < 0:
            out[1][1] = 6
            return out
        
        if INCLUDES(__class__, surround[2][1], ['empty','gas']):
            out[1][1] = surround[2][1]
            out[2][1] = 2
            return out
        if (INCLUDES(__class__, surround[1][0], ['empty','gas']) and 
            INCLUDES(__class__, surround[1][2], ['empty','gas'])):
            if random.random() < 0.5:
                out[1][0] = 2
                out[1][1] = surround[1][0]
            else:
                out[1][2] = 2
                out[1][1] = surround[1][2]
            return out
        if (INCLUDES(__class__, surround[1][0], ['empty','gas']) and 
            INCLUDES(__class__, surround[1][2], ['soild','dust','Water'])):
            out[1][1] = surround[1][0]
            out[1][0] = 2
            return out
        if (INCLUDES(__class__, surround[1][0], ['soild','dust','Water']) and 
            INCLUDES(__class__, surround[1][2], ['empty','gas'])):
            out[1][1] = surround[1][2]
            out[1][2] = 2
            return out
        else:
            return out
    
    def steam(surround, temp):
        out = copy.deepcopy(surround)
        if temp < 95:
            out[1][1] = 2
            return out
        
        if not INCLUDES(__class__, surround[0][1], ['soild', 'Steam']):
            out[1][1] = surround[0][1]
            out[0][1] = 3
            return out
        if (not INCLUDES(__class__, surround[1][0], ['soild', 'Steam']) and 
            not INCLUDES(__class__, surround[1][2], ['soild', 'Steam'])):
            if random.random() < 0.5:
                out[1][0] = 3
                out[1][1] = surround[1][0]
            else:
                out[1][2] = 3
                out[1][1] = surround[1][2]
            return out
        if (not INCLUDES(__class__, surround[1][0], ['soild', 'Steam']) and 
            INCLUDES(__class__, surround[1][2], ['soild', 'Steam'])):
            out[1][1] = surround[1][0]
            out[1][0] = 3
            return out
        if (INCLUDES(__class__, surround[1][0], ['soild', 'Steam']) and 
            not INCLUDES(__class__, surround[1][2], ['soild', 'Steam'])):
            out[1][1] = surround[1][2]
            out[1][2] = 3
            return out
        else:
            return out
        
    def stone(surround, temp):
        if temp > 1000:
            out = copy.deepcopy(surround)
            out[1][1] = 10
            return out
        return surround
    
    def acid(surround, temp):
        out = copy.deepcopy(surround)
        
        out[0][1] = surround[0][1] if INCLUDES(__class__, surround[0][1], ['Border', 'acid']) else 0
        out[1][0] = surround[1][0] if INCLUDES(__class__, surround[1][0], ['Border', 'acid']) else 0
        out[1][2] = surround[1][2] if INCLUDES(__class__, surround[1][2], ['Border', 'acid']) else 0
        out[2][1] = surround[2][1] if INCLUDES(__class__, surround[2][1], ['Border', 'acid']) else 0

        if INCLUDES(__class__, surround[2][1], ['empty']):
            out[1][1] = 0
            out[2][1] = 5
            return out
        if (INCLUDES(__class__, surround[1][0], ['empty']) and 
            INCLUDES(__class__, surround[1][2], ['empty'])):
            out[1][1] = 0
            if random.random() < 0.5:
                out[1][0] = 5
            else:
                out[1][2] = 5
            return out
        if (INCLUDES(__class__, surround[1][0], ['empty']) and 
            INCLUDES(__class__, surround[1][2], ['Border', 'acid'])):
            out[1][1] = 0
            out[1][0] = 5
            return out
        if (INCLUDES(__class__, surround[1][0], ['Border', 'acid']) and 
            INCLUDES(__class__, surround[1][2], ['empty'])):
            out[1][1] = 0
            out[1][2] = 5
            return out
        else:
            return out
    
    def ice(surround, temp):
        if temp > 5:
            out = copy.deepcopy(surround)
            out[1][1] = 2
            return out
        
        return surround
    
    def infispread(surround, temp):
        out = copy.deepcopy(surround)
        out[0][1] = 7 if INCLUDES(__class__, surround[0][1], 'empty') else surround[0][1]
        out[1][0] = 7 if INCLUDES(__class__, surround[1][0], 'empty') else surround[1][0]
        out[1][2] = 7 if INCLUDES(__class__, surround[1][2], 'empty') else surround[1][2]
        out[2][1] = 7 if INCLUDES(__class__, surround[2][1], 'empty') else surround[2][1]
        return out
    
    def virus(surround, temp):
        out = copy.deepcopy(surround)
        out[0][1] = surround[0][1] if INCLUDES(__class__, surround[0][1], ['Border', 'empty']) else 8
        out[1][0] = surround[1][0] if INCLUDES(__class__, surround[1][0], ['Border', 'empty']) else 8
        out[1][2] = surround[1][2] if INCLUDES(__class__, surround[1][2], ['Border', 'empty']) else 8
        out[2][1] = surround[2][1] if INCLUDES(__class__, surround[2][1], ['Border', 'empty']) else 8
        return out

    def glass(surround, temp):
        return surround
    
    def lava(surround, temp):
        out = copy.deepcopy(surround)
        if temp < 1600:
            out[1][1] = 4
            return out
        
        if INCLUDES(__class__, surround[2][1], ['empty','gas']):
            out[1][1] = surround[2][1]
            out[2][1] = 10
            return out
        if (INCLUDES(__class__, surround[1][0], ['empty','gas']) and 
            INCLUDES(__class__, surround[1][2], ['empty','gas'])):
            if random.random() < 0.5:
                out[1][0] = 10
                out[1][1] = surround[1][0]
            else:
                out[1][2] = 10
                out[1][1] = surround[1][2]
            return out
        if (INCLUDES(__class__, surround[1][0], ['empty','gas']) and 
            INCLUDES(__class__, surround[1][2], ['soild','dust','Lava'])):
            out[1][1] = surround[1][0]
            out[1][0] = 10
            return out
        if (INCLUDES(__class__, surround[1][0], ['soild','dust','Lava']) and 
            INCLUDES(__class__, surround[1][2], ['empty','gas'])):
            out[1][1] = surround[1][2]
            out[1][2] = 10
            return out
        else:
            return out
        
    IDS = {0: air, 1: sand, 2: water, 3: steam, 4: stone, 5: acid, 6: ice, 7: infispread, 8: virus, 9: glass, 10: lava}
    COLOR = {-1: "#555555", 0: "#000000", 1: "#ffd200", 2: "#0052ff", 3: "#a2a2a2", 4: "#828282", 5: "#a2ff22", 6: "#00ffff", 7: "#a200ff", 8: "#df00ff", 9: "#55ffff", 10: "#ff0000"}
    TAGS = {-1: ['soild'], 0: ['empty'], 1: ['dust'], 2: ['liquid'], 3: ['gas'], 4: ['soild'], 5: ['liquid','acid'], 6: ['soild'], 7: ['soild'], 8: ['soild'], 9: ['soild'], 10: ['liquid']}
    NAME = {-1: 'Border', 0: 'Air', 1: 'Sand', 2: 'Water', 3: 'Steam', 4: 'Stone', 5: 'Acid', 6: 'Ice', 7: 'Infispread', 8: 'Virus', 9: 'Glass', 10: 'Lava'}
    DEFAULTTEMP = {0: 30, 1: 30, 2: 30, 3: 120, 4: 30, 5: 30, 6: -1000, 7: 30, 8: 30, 9: 30, 10: 20000}