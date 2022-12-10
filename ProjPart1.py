from threading import Thread
from PIL import Image

def resize():

    return

def watermark(imagem):
    watermark= Image.open("watermark.png")
    imagem=Image.open(imagem)
    # image watermark
    size = (500, 100)
    crop_image = watermark.copy()
    crop_image.thumbnail(size)
    
    # add watermark
    copied_image = imagem.copy()
    copied_image.paste(crop_image, (500, 200))
    copied_image.show()
    return copied_image

lista=[]
new=[]

f= open("nomes.txt", "r")

with f as texto:
    for line in texto:
        lista+=[line.replace("\n", "")]


watermark(lista[0])
