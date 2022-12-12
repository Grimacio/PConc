# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 16:23:23 2022

@author: guiga
"""

from threading import Thread
from PIL import Image
from tkinter import Tk
from tkinter.filedialog import askdirectory
import os


def resize(imagem, new_width):
    copy= Image.open(imagem)
    dimensoes = (new_width,new_width *1.0/copy.shape[1] * copy.shape[0])
    copy=copy.resize(dimensoes)
    return copy