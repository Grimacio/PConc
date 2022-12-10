from threading import Thread
from PIL import Image

def resize(imagem, dimensoes):
    copy= Image.open(imagem)
    copy=copy.resize(dimensoes)
    return copy

def watermark(imagem):
    watermark= Image.open("watermark.png")
    imagem=Image.open(imagem)
    # image watermark
    size = (250, 50)
    crop_image = watermark.copy()
    
    # add watermark
    copied_image = imagem.copy()
    copied_image.paste(crop_image, size)
    return copied_image

lista=[]
new=[]

f= open("nomes.txt", "r")

with f as texto:
    for line in texto:
        lista+=[line.replace("\n", "")]

watermark(lista[0]).show()
'''imagem=Image.open(lista[0])
imagem.thumbnail((150,150))
imagem.save(lista[0].split(".")[0]+ ".thumbnail", "JPEG")'''
