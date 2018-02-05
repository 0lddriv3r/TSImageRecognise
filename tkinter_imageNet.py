# -*- coding:utf-8 -*-
# from Tkinter import *
import Tkinter
import tkMessageBox
import tkFileDialog
from Tkinter import Frame
from Tkinter import Button
from Tkinter import PhotoImage
from Tkinter import Entry
from Tkinter import Label
from Tkinter import Menu
from tkinter import *
from PIL import Image, ImageTk
from image_classify.classify_api import classify
import json

global imageFile

def handlerAdaptor(fun, **kwds):
    return lambda event, fun=fun, kwds=kwds : fun(event, **kwds)

def displayImage(app):
    global imageFile
    configImage = ImageTk.PhotoImage(Image.open(imageFile))
    imageLabel.configure(image=configImage)
    imageLabel.image = configImage

def openImage(app):
    global imageFile
    imageFile = tkFileDialog.askopenfilename(title='选择图片',
                filetypes=[('Python', '*.png *.jpg *.jpeg *.bmp'), ('All Files', '*')])

    if open(imageFile):
        displayImage(app)

def recogniseImage(app):
    global imageFile
    file = open(imageFile)
    data = file.read()
    results = classify(data)

    # listBoxRecognise.delete(FIRST, LAST)

    for result in results:
        listBoxRecognise.insert(END, result)
        print result

# GUI initial
def init(app):
    # title
    app.title("TensorFlow图像识别")

    # size
    app.geometry('600x400')
    # app.resizable(width=False, height=False)

    # menu bar
    menuBar = Menu(app)

    # file menu
    fileMenu = Menu(menuBar, tearoff=0)
    fileMenu.add_separator()
    fileMenu.add_command(label="Exit", command=app.quit)
    # filemenu.add_command(label="Export", command=export)
    menuBar.add_cascade(label="File", menu=fileMenu)

    # edit menu
    editMenu = Menu(menuBar, tearoff=0)
    editMenu.add_separator()
    menuBar.add_cascade(label="Edit", menu=editMenu)

    # help menu
    helpMenu = Menu(menuBar, tearoff=0)
    helpMenu.add_command(label='About', command=aboutMessageBox)
    menuBar.add_cascade(label="Help", menu=helpMenu)

    app.config(menu=menuBar)

    label1 = Label(app, text='图片：').grid(row=0, column=0, sticky=W)
    label2 = Label(app, text='结果：').grid(row=0, column=1, sticky=W)

    # push button
    openImageButton = Button(app, text='选择图片', width='20', command=lambda : openImage(app=app))
    openImageButton.grid(row=3, column=0)
    # openImageButton.bind("<Return>", openImage)
    openImageButton.focus_set()

    recogniseImageButton = Button(app, text='TF识别', width='20', command=lambda : recogniseImage(app=app))
    recogniseImageButton.grid(row=3, column=1)

def aboutMessageBox():
    tkMessageBox.showinfo('TensorFlow图像识别', '关于Google开源机器学习项目\n'
                          '使用方法：\n1.点击 选择图片，选择要识别的图片；\n2. 点击 TF识别，进行图像识别。')

if __name__ == '__main__':
    app = Tkinter.Tk()

    init(app)

    image = ImageTk.PhotoImage(Image.open('image_classify/images/my_photo.png'))
    imageLabel = Tkinter.Label(app, image=image)
    imageLabel.grid(row=1, column=0, rowspan=2)

    scrl = Scrollbar(app)
    # scrl.place(height=80, width=120, relx=0.1, rely=0.8)
    scrl.grid(row=1, column=1)
    listBoxRecognise = Listbox(app, height=5, selectmode=BROWSE)
    listBoxRecognise.configure(yscrollcommand=scrl.set)
    listBoxRecognise.grid(row=1, column=1, rowspan=2)
    scrl['command'] = listBoxRecognise.yview

    app.mainloop()
