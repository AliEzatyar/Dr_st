from PIL import Image, ImageOps
import os
os.chdir("F:\\project\\foto\\")
def resize(in_path,out_path,size,qualtiy):
    with Image.open(in_path) as image:
        image  = ImageOps.exif_transpose(image)
        image = image.resize(size,Image.LANCZOS)
        image.save(out_path,optimize=True,quality=qualtiy)

#example
for foto in os.listdir():
    resize(foto,f"F:\\project\\media\\drugs\\{foto}",(500,700),100)