import math 
from threading import Thread
from PIL import Image
from tkinter.filedialog import askdirectory
import os

def resize(imagem, new_width):
    try:
        copy= Image.open(imagem)
        try:
            dimensoes = (new_width,math.ceil(new_width *1.0/copy.size[0] * copy.size[1]))
            copy=copy.resize(dimensoes)
            return copy
        except Exception as e:
            print(e)
            return None
    except Exception as e:
        print(e)
        return None

def watermark(imagem, water):
    try:
        imagem=Image.open(imagem)
        try:
            # image watermark
            position=(0,0) 
            crop_image = resize(water, math.ceil(imagem.size[0]/3))
            
            # add watermark
            copied_image = imagem.copy()
            copied_image.paste(crop_image, position, crop_image)
            return copied_image
        except Exception as e:
            print(e)
            return None
    except Exception as e:
        print(e)
        return None

def thumbnail(ficheiro, tamanho):
    tamanho = math.ceil(tamanho)
    if tamanho < 1:
        print("dimensao thumbnail invalida")
        return None
    try:
        imagem=Image.open(ficheiro)
        try:
            width, height = imagem.size
            if(width > height):
                new_height = tamanho
                new_width = math.ceil(new_height *1.0/height * width)
            else:
                new_width = tamanho
                new_height = math.ceil(new_width *1.0/width * height)
            imagem.thumbnail((new_width,new_height))
            corte = (math.ceil(new_width/2-tamanho/2),math.ceil(new_height/2-tamanho/2),math.ceil(new_width/2+tamanho/2),math.ceil(new_height/2+tamanho/2))
            imagem = imagem.crop(corte)
            return imagem
        except Exception as e:
            print(e)
            return None
    except Exception as e:
        print(e)
        return None

def tWatermark():
    global listacopy
    global path
    global watermarkReady
    while len(listacopy)>0:
        imagem= listacopy.pop()

        watermark(path+"/"+imagem, "watermark.png").save(path+ "/watermark/"+imagem, "PNG")
        print("acabei 1")
        watermarkReady+=[path+"/watermark/"+imagem]
    return

def tResize():
    
    global lista
    global path
    global dimensoes
    for nome in lista:
        resize(path+"/watermark/"+nome, dimensoes).save(path +"/resized/"+ nome.split("/")[-1], "PNG")
    return
        

def tThumbnail():
    
    global tamanho

    global lista
    global path
    for nome in lista:
        thumbnail(path+"/watermark/"+nome, tamanho).save(path +"/thumbnail/"+ nome.split("/")[-1], "PNG")
    return
    
dimensoes= 500
tamanho = 50
watermarkReady=[]
print("Select Image Folder")
path = askdirectory(title='Select Folder')
print(path)
if not os.path.exists(path+"/watermark"):
    os.mkdir(path+"/watermark")
if not os.path.exists(path+"/resized"):
    os.mkdir(path+"/resized")
if not os.path.exists(path+"/thumbnail"):
    os.mkdir(path+"/thumbnail")

lista=[]

f= open("nomes.txt", "r")

with f as texto:
    for line in texto:
        lista+=[line.replace("\n", "")]

listacopy=lista.copy()

watermarkThread= Thread(target=tWatermark)
resizeThread= Thread(target=tResize)
thumbnailThread= Thread(target=tThumbnail)

watermarkThread.start()
watermarkThread.join()
resizeThread.start()
thumbnailThread.start()


resizeThread.join()
thumbnailThread.join()

print("done")