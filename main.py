import tkinter

from initController import *
from tkinter import Menu
from tkinter.ttk import *
from bridge import MouseMotionToController
from controller.canvasController import CanvasController
from controller.modeController import CompositionObjectController

top = tkinter.Tk()

buttonsContainer = tkinter.Frame(top)
buttonsContainer.pack(side = tkinter.LEFT)


def create_window():
    window = tkinter.Toplevel(top)
    window.geometry('{}x{}'.format(200 , 100))
   
    def close():
        window.destroy()
   
    def getText(event):
            CanvasController.canvasContainer.itemconfig(MouseMotionToController.singleClickedObj[-2].text, text = e.get())
   
    button1 = tkinter.Button(window, text="Close", command=close, width = 50)
    button2 = tkinter.Button(window, text="OK", command=close,  width = 50)
    button1.pack(side = tkinter.BOTTOM)
    button2.pack(side = tkinter.BOTTOM)
    e = tkinter.Entry(window)
   
    e.bind("<Return>", getText)
    e.pack()


def createNewGroup():
    CompositionObjectController.createNewGroup()


def killAGroup():
    CompositionObjectController.killAGroup()

menubar = Menu(top)
editMenu = Menu(menubar, tearoff=0)
editMenu.add_command(label="Group", command=createNewGroup)
editMenu.add_command(label="UnGroup", command=killAGroup)
editMenu.add_command(label="Change Object Name", command=create_window)
menubar.add_cascade(label="Edit Menu", menu=editMenu)

initAllButtons(buttonsContainer)
initCanvasContainer(top)
initModeControllers()

top.config(menu = menubar)
top.mainloop()