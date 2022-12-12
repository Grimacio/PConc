from threading import Thread
import math 
from PIL import Image
from tkinter import Tk
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


def threadFunc():
    global listacopy
    global path
    while len(listacopy)>0:
        imagem= listacopy.pop()
        dimensoes= 250
        tamanho= 50

        if not os.path.exists(path+"/watermark/"+imagem):
            print("watermark de "+imagem.split(".")[0]+": nao encontrado")
            watermark(path+"/"+imagem).save(path+ "/watermark/"+imagem, "PNG")
        else:
            print("watermark de "+imagem.split(".")[0]+": encontrado")
        
        if not os.path.exists(path+"/resized/"+imagem):
            print("resize de "+imagem.split(".")[0]+": nao encontrado")
            resize(path+ "/watermark/" +imagem, dimensoes).save(path +"/resized/"+ imagem, "PNG")
        else:
            print("resize de "+imagem.split(".")[0]+": encontrado")
        
        if not os.path.exists(path+"/thumbnail/"+imagem):
            print("resize de "+imagem.split(".")[0]+": nao encontrado")
            thumbnail(path+"/resized/" + imagem, tamanho).save(path + "/thumbnail/" +imagem, "PNG")
        else:
            print("resize de "+imagem.split(".")[0]+": encontrado")

    return


print("Select Image Folder")
path = askdirectory(title='Select Folder')
print(path)
if not os.path.exists(path+"/watermark"):
    os.mkdir(path+"/watermark")
if not os.path.exists(path+"/resized"):
    os.mkdir(path+"/resized")
if not os.path.exists(path+"/thumbnail"):
    os.mkdir(path+"/thumbnail")
numeroThreads=int(input("Number of Threads?:\n"))
lista=[]

f= open("nomes.txt", "r")

with f as texto:
    for line in texto:
        lista+=[line.replace("\n", "")]

listacopy=lista.copy()
listaThreads=[]
for i in range( numeroThreads):
    newThread = Thread(target=threadFunc)
    newThread.start()
    listaThreads+=[newThread]
for item in listaThreads:
    item.join()
    print("done")

