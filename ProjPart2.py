import math 
from threading import Thread
from threading import Condition
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

def tWatermark(self):
    global listacopy
    global path
    global watermarkReady
    while len(listacopy)>0:
        self.acquire()
        imagem= listacopy.pop()

        watermark(path+"/"+imagem).save(path+ "/watermark/"+imagem, "PNG")
        print("acabei 1")
        watermarkReady+=[path+"/watermark/"+imagem]
        self.notify_all()
        self.release()
    return

def tResize(self):
    
    global dimensoes
    i=0
    while watermarkThread.is_alive() or len(watermarkReady)>i:
        self.acquire()
        if len(watermarkReady)<=i:
            self.wait()
            print("acordei")
        else:
            target=watermarkReady[i]
            print("encontrei1")
            resize(target, dimensoes).save(path +"/resized/"+ target.split("/")[-1], "PNG")
            i+=1
        self.release()
    return

def tThumbnail(self):
    
    global tamanho
    j=0
    while watermarkThread.is_alive() or len(watermarkReady)>j:
        self.acquire()  
        if len(watermarkReady)<=j:
            self.wait()
            print("acordei")
        else:
            target=watermarkReady[j]
            print("encontrei2")
            thumbnail(target, tamanho).save(path +"/thumbnail/"+ target.split("/")[-1], "PNG")
            j+=1
        self.release()
    
    return
        

dimensoes= (500,500)
tamanho = (50,50)
watermarkReady=[]
print("Select Image Folder")
path = askdirectory(title='Select Folder')
print(path)
os.mkdir(path+"/watermark")
os.mkdir(path+"/resized")
os.mkdir(path+"/thumbnail")

lista=[]

f= open("nomes.txt", "r")

with f as texto:
    for line in texto:
        lista+=[line.replace("\n", "")]

listacopy=lista.copy()


condition = Condition()

watermarkThread= Thread(target=tWatermark, args=(condition,))
resizeThread= Thread(target=tResize, args=(condition,))
thumbnailThread= Thread(target=tThumbnail, args=(condition,))

watermarkThread.start()
resizeThread.start()
thumbnailThread.start()

watermarkThread.join()
resizeThread.join()
thumbnailThread.join()

print("done")