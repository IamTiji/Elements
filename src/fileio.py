import numpy as np

def save(grid, dest):
    with open(dest, 'wb') as fp:
        fp.write(len(grid).to_bytes(1, byteorder='little'))
        fp.write(len(grid[0]).to_bytes(1, byteorder='little'))

        for x in grid:
            for y in x:
                fp.write(y.to_bytes(1, byteorder='little'))
        fp.close()

def load(src):
    with open(src, 'rb') as fp:
        height = fp.read(1)
        width = fp.read(1)

        array=np.zeros((int(height), int(width)), dtype=np.uint8)

        for y in range(int(height)):
            for x in range(int(width)):
                array[y][x] = fp.read(1)
        
        fp.close()
    return array
