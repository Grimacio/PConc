from threading import Thread
import math 
from PIL import Image
from tkinter.filedialog import askdirectory
import os


path=""
numeroThreads=0
dimensoes=0
tamanho=0
lista=[]
listacopy=[]
watermarkLOC="watermark.png"



# Inicializa o programa recolhendo inputs pelo terminal, 
# recolhe os endereços das imagens e cria as threads de acordo

def ap_paralelo_1():
    global lista, path
    initalize()
    lista=readtxt(path)
    createThreads(numeroThreads)




# Define os valores a utilizar no programa, bem como
# a diretoria das imagens requeridas

def initalize():
    print("Select Image Folder")
    global path, numeroThreads, dimensoes, tamanho

    # Abre uma janela em que se navega até à diretoria em
    # que se econtram as imagens e o ficheiro .txt, 
    # guardando-se o path
    path = askdirectory(title='Select Folder')

    
    while numeroThreads<=0:
        numeroThreads=int(input("Number of Threads?:\n"))
        if numeroThreads<=0:
            print("Invalid number of Threads")

    # A dimensao referente a imagem redimensionada
    dimensoes=int(input("Resize to which size? (px):\n"))

    # A dimensao da thumbnail
    tamanho=int(input("Thumbnail to which size? (px):\n"))

    # Apenas criamos as novas pastas se estas nao existirem
    if not os.path.exists(path+"/Watermark-dir"):
        os.mkdir(path+"/Watermark-dir")
    if not os.path.exists(path+"/Resize-dir"):
        os.mkdir(path+"/Resize-dir")
    if not os.path.exists(path+"/Thumbnail-dir"):
        os.mkdir(path+"/Thumbnail-dir")



# Com base no ficheiro "image-list.txt" presente na diretoria em que
# as imagens se encontram, é retornada uma lista com os nomes das imagens

def readtxt(path):

    res=[]

    f= open(path+"/image-list.txt", "r")

    with f as texto:
        for line in texto:
            res+=[line.replace("\n", "")]

    return res




# Sao criadas n Threads, cada uma executa a funcao threadFunc
# Para eventual identificacao, a propriedade "name" e alterada
# de acordo com a ordem pela qual sao criadas

def createThreads(n):

    global lista, listacopy

    listacopy=lista.copy()

    listaThreads=[]

    for i in range(n):

        # Cria-se e inicializa-se uma Thread
        newThread = Thread(target=threadFunc)
        newThread.name = "Processa_ficheiro("+ str(i)+")"
        newThread.start()

        # Uma lista de Threads e criada para posterior finalizacao
        listaThreads+=[newThread]

    for item in listaThreads:
        item.join()



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

def watermark(imagem):
    global watermarkLOC
    try:
        imagem=Image.open(imagem)
        try:
            # image watermark
            position=(0,0) 
            crop_image = resize(watermarkLOC, math.ceil(imagem.size[0]/3))
            
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


# Enquanto a listacopy contiver enderecos de imagens para processar,
# o último dos seus elementos e usado para criar uma cópia da imagem
# com watermark, que depois e redimensionada e por fim cria-se uma thumbnail
# Cada uma destas imagens é gravada no formato .png 

def threadFunc():

    global listacopy
    global path
    global dimensoes
    global tamanho


    # Enquanto a listacopy contiver enderecos de imagens para processar,
    # a Thread continua ativa

    while len(listacopy)>0:
        

        # O último dos seus elementos é usado 

        imagem= listacopy.pop()

        if not os.path.exists(path+"/Watermark-dir/"+imagem):
            print("watermark de "+imagem.split(".")[0]+": nao encontrado")
            watermark(path+"/"+imagem).save(path+ "/Watermark-dir/"+imagem, "PNG")
        else:
            print("watermark de "+imagem.split(".")[0]+": encontrado")
        
        if not os.path.exists(path+"/Resize-dir/"+imagem):
            print("resize de "+imagem.split(".")[0]+": nao encontrado")
            resize(path+ "/Watermark-dir/" +imagem, dimensoes).save(path +"/Resize-dir/"+ imagem, "PNG")
        else:
            print("resize de "+imagem.split(".")[0]+": encontrado")
        
        if not os.path.exists(path+"/Thumbnail-dir/"+imagem):
            print("resize de "+imagem.split(".")[0]+": nao encontrado")
            thumbnail(path+"/Resize-dir/" + imagem, tamanho).save(path + "/Thumbnail-dir/" +imagem, "PNG")
        else:
            print("resize de "+imagem.split(".")[0]+": encontrado")

    return



ap_paralelo_1()
