import copy
import json

def get_palette():
    r = 16
    g = 0
    b = 0
    palette = []
    for i in range(48):
        if g < 16 and b == 0:
            r = r - 1
            g = g + 1
        elif b < 16 and r == 0:
            g = g - 1
            b = b + 1
        else:
            b = b - 1
            r = r + 1
        palette.append((r,g,b))
    last = copy.copy(palette[len(palette)-1])
    del palette[len(palette)-1]
    palette.insert(0,last)
    return palette
palette = get_palette()
print(json.dumps(palette,indent=4))