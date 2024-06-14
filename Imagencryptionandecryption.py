#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 01:28:37 2022

@author: dhruv
"""
import cv2
import matplotlib.image as mpimg
from matplotlib import pyplot as plt
#import Front
from tkinter import *
from tkinter import filedialog
import os
from PIL import ImageTk
import tkinter as tk
import numpy as np
from math import log10, sqrt
import skimage.measure
import PIL                          
from PIL import Image
from scipy.stats import pearsonr 

def choose_File():
    filename = filedialog.askopenfilename(initialdir=os.getcwd(),title="Select Image file",filetypes=(("JPG File","*.jpg"),("PNG file","*.png"),("All files","*.*")))
    entry1.insert(0,str(filename))
    img=Image.open(filename)
    img.thumbnail((200,200))
    img=ImageTk.PhotoImage(img)
    lbl.configure(imag=img)
    lbl.image=img
    img1=mpimg.imread(filename)
    height=img1.shape[0]
    width=img1.shape[1]
    entropy = skimage.measure.shannon_entropy(img1)
    marg = np.histogramdd(np.ravel(img1), bins = 256)[0]/img1.size
    marg = list(filter(lambda p: p > 0, np.ravel(marg)))
    entropy = -np.sum(np.multiply(marg, np.log2(marg)))
    print(entropy)
    if entropy>=0.000000000000000 and entropy<=3.500000000000000:
        button2 = Button(Frame2, text = "This Image is PLAIN image and  using TENT map",font="time 20 bold", pady= 10,command=tentKeygen(0.61,1.91,height*width)) 
        button2.pack(side = LEFT,padx= 40)
        print("Tent")
    elif entropy>3.500000000000000 and entropy<=7.000000000000000:
        button2 = Button(Frame2, text = "This Image is TEXT image and using LOGISTIC map",font="time 20 bold", pady= 10,command =logistickeygen(0.01,3.951,height*width))
        button2.pack(side = LEFT,padx= 40)
        print("Logistic")
    elif entropy>7.000000000000000:
        button2 = Button(Frame2, text = "This Image is COLORED image and using HENON map ",font="time 20 bold", pady= 10) 
        button2.pack(side = LEFT,padx= 40,command =henonkeygen(0.001,0.2,1.4,0.3,height*width))
        print("Henon")
            
#*************************************************** HENON KEY GENERATION **********************************************************************************        
            
def henonkeygen(x,y,a,b,size):
        key=[]
        key1=[]
        for i in range(size):
            x1=1-a*x*x+y
            y1=b*x
            key.append(int((x1*pow(10,16))%256))
            x=x1
            y=y1
        performEntireEncryption(key)   
               
#************************************************* Logistic KEY GENERATION **********************************************************************************
def logistickeygen(x,r,size):
        key=[]
        for i in range(size):
            x=r*x*(1-x)
            key.append(bin(int(x*10000)).replace('0b',''))
        performEntireEncryptionandDecryption(key)   
    
    
#**************************************************** Tent KEY GENERATION ************************************************************************************* 
def tentKeygen(x,r,size):   
        key=[]
        for i in range(size):
            if(x<0.5):
                x=r*x
            elif(x>=0.5):
                x=r*x*(1-x)
            #.append(int(x*10000000))
            key.append(int((x*pow(10,16))%256))
        performEntireEncryption(key) 
    
    #****************************************************** Xor based Encrypton using henon and tent **************************************************************
def performEntireEncryption(key):
        filename=entry1.get()
        img=mpimg.imread(filename)
        height=img.shape[0]
        width=img.shape[1]
        z=0
        enimg=np.zeros(shape=[height,width,3],dtype=np.uint8)
        for i in range(height):
            for j in range(width):
                enimg[i,j]=img[i,j]^key[z]
                z+=1
        mpimg.imsave('/Users/dhruv/Desktop/! Working Dir/Encryptedimage.jpg',enimg)
        img=Image.open('/Users/dhruv/Desktop/! Working Dir/Encryptedimage.jpg')
        img.thumbnail((200,200))
        img=ImageTk.PhotoImage(img)
        lbl1.configure(imag=img)
        lbl1.image=img
        z=0
        deimg=np.zeros(shape=[height,width,3],dtype=np.uint8)
        for i in range(height):
            for j in range(width):
                deimg[i,j]=enimg[i,j]^key[z]
                z+=1
        mpimg.imsave('/Users/dhruv/Desktop/! Working Dir/Decryptedimage.bmp',deimg)
        img1=Image.open('/Users/dhruv/Desktop/! Working Dir/Decryptedimage.bmp')
        img1.thumbnail((200,200))
        img1=ImageTk.PhotoImage(img1)
        lbl2.configure(imag=img1)
        lbl2.image=img1
    
    
       
#**************************************************** Neural network  based using logistic map *******************************************************       
def performEntireEncryptionandDecryption(key):
         fname=entry1.get()
         img = PIL.Image.open(fname)
         wid, hgt = img.size
         height = int(hgt)
         width = int(wid)    
         image = Image.open(fname).convert("L")
         arr = np.asarray(image)
         arrimg_2d = np.reshape(arr, (width*height, 1))
         arr_2d = np.reshape(key,(height,width))
    #generation of weights bias
         li = []
         bias = []
         for i in range(height):
            for j in range(width):
                 y = []
                 y = arr_2d[i][j]
                 key = []
                 for k in range(8):
                     if(j == i and y[k] == '0'):
                         w = 100
                                          
                     elif(j == i and y[k] == '1'):
                         w = 250                   
                     else:
                         w = 75                    
                     key.append(w)
                 li.append(key) 
                 if(y[8] == '0'):
                    bias.append(1)      
                 if(y[8] == '1'):
                    bias.append(255)     
    #generated weights are now xored with image array as well as with bias to get encrypted image
    #the same process is carried out to get the original image back
         into = []
         into_rev = []
         apply_bias = []
         apply_rev_bias = []
         come_out = []
         for i in range(height*width):
             for j in range(8):
                 out = li[i][j] ^ arrimg_2d[i] ^ bias[i]
                 into.append(int(out))
                 outcome = li[i][j] ^ out  ^ bias[i]
                 into_rev.append(int(outcome))
    #--------------------------------------------------------------
    #extraction of pixels and ploting the encrypted image
         into_of_size_eight = np.reshape(into,(height*width, 8))
         encrypt_img = []
         for i in range(height*width):
             enimg = into_of_size_eight[i][0]
             encrypt_img.append(enimg)
         into_again_2d = np.reshape(encrypt_img,(height, width))
         mpimg.imsave('/Users/dhruv/Desktop/! Working Dir/Encryptedimage.jpg',into_again_2d)
         img=Image.open('/Users/dhruv/Desktop/! Working Dir/Encryptedimage.jpg').convert("L")
         img.thumbnail((200,200))
         img=ImageTk.PhotoImage(img)
         lbl1.configure(imag=img)
         lbl1.image=img
    #-----------------------------------------------------------------------
    #extraction of pixels and ploting the decrypted image
         into_rev_of_size_eight = np.reshape(into_rev,(height*width, 8))
         decrypt_img = []
         for i in range(height*width):
             decimg = into_rev_of_size_eight[i][0]
             decrypt_img.append(decimg)       
         into_rev_again_2d = np.reshape(decrypt_img,(height, width))
         mpimg.imsave('/Users/dhruv/Desktop/! Working Dir/Decryptedimage.bmp',into_rev_again_2d)
         img1=Image.open('/Users/dhruv/Desktop/! Working Dir/Decryptedimage.bmp').convert("L") 
         img1.thumbnail((200,200))
         img1=ImageTk.PhotoImage(img1)
         lbl2.configure(imag=img1)
         lbl2.image=img1
         
        
root =Tk()
root.title("Capstone Project - team 112")
root.configure(background='cyan3')
root.state("zoomed")            
Frame1 = Frame(root,bg="brown")
Frame1.pack()
    
Frame2 = Frame(root,background='cyan3')
Frame2.pack()

Frame3 = Frame(root,bg="gray")
Frame3.pack(side=tk.LEFT,padx= 30, pady= 30)
labelframe1=LabelFrame(Frame3,text="Original Image",font="time 20 bold")    
labelframe1.pack(side=tk.LEFT,padx= 30, pady= 10)

Frame4 = Frame(root,bg="gray")
Frame4.pack(side=tk.LEFT,padx= 30, pady= 30)
labelframe2=LabelFrame(Frame4,text="Encrypted Image",font="time 20 bold") 
labelframe2.pack(side=tk.LEFT,padx= 30, pady= 10)    

Frame5 = Frame(root,bg="gray")
Frame5.pack(side=tk.LEFT,padx= 30, pady= 30)
labelframe3=LabelFrame(Frame5,text="Decrypted Image",font="time 20 bold") 
labelframe3.pack(side=tk.LEFT,padx= 30, pady= 10)
    
label_1 = Label(Frame1, text ="Image Encryption and Decryption: ",font="time 30 bold",fg="white",width = 200,bg="gray")
label_1.pack(side = TOP)

entry1 = Entry(Frame1,width =100)
entry1.pack(side = TOP,pady= 20)

button1 = Button(Frame1, text = "Select Image", padx=10, pady= 10,command = choose_File,bg="cyan3")
button1.pack(side = TOP,pady= 20)

button3 = Button(root, text = "Data Visualization", padx=10, pady= 10,command = next)
button3.pack(side =tk.LEFT,pady= 20)
    
lbl=Label(labelframe1)
lbl.pack(side=tk.LEFT, padx= 30, pady= 10)
    
lbl1=Label(labelframe2)
lbl1.pack(side=tk.LEFT, padx= 30, pady= 10)
    
lbl2=Label(labelframe3)
lbl2.pack(side=tk.LEFT,padx= 30, pady= 10)
root.mainloop()
