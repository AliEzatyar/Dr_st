# opening the image and then creating a byte object of it in the ram, then do whatever...
# instead of a filepath or name, we can also pass a bytesIO object or file-like object
import os

from PIL import Image
from io import BytesIO
poto = open('Amisel_E__Amino_Rich.jpg',"rb")
x = BytesIO(poto.read())
# poto.close()
print(os.path.getsize("Amisel_E__Amino_Rich.jpg")//10)
Image.open(poto)