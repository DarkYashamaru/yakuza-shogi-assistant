from PIL import Image
import numpy as np
import os

path = "D:/Repositories/yakuza-shogi-assistant/backend/templates"

content = os.listdir(path)

for line in content:
    img = Image.open(f"{path}/{line}")
    gray = img.convert("L")
    newName = line.replace("_color", "")
    gray.save(f"{path}/{newName}.png")

#print(content)