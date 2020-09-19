
r = 16
g = 0
b = 0
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
    print((r,g,b))
    