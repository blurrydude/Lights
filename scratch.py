# import copy
# import json

# def get_palette():
#     r = 16
#     g = 0
#     b = 0
#     palette = []
#     for i in range(48):
#         if g < 16 and b == 0:
#             r = r - 1
#             g = g + 1
#         elif b < 16 and r == 0:
#             g = g - 1
#             b = b + 1
#         else:
#             b = b - 1
#             r = r + 1
#         palette.append((r,g,b))
#     last = copy.copy(palette[len(palette)-1])
#     del palette[len(palette)-1]
#     palette.insert(0,last)
#     return palette
# palette = get_palette()
# print(json.dumps(palette,indent=4))
import subprocess

out = subprocess.Popen(['pip3','list'],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT)

stdout,stderr = out.communicate()
text = str(stdout)
text = text[2:len(text)-3]
while "  " in text:
    text = text.replace('  ',' ')
lines = text.split('\\n')
packages = {}
for line in lines:
    if "Package" in line or "---" in line:
        continue
    data = line.split(' ')
    packages[data[0]] = data[1]