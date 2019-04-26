import tkinter

from initController import *
from tkinter import Menu
from bridge import MouseMotionToController
from controller.canvasController import CanvasController

top = tkinter.Tk()

buttonsContainer = tkinter.Frame(top)
buttonsContainer.pack(side = tkinter.LEFT)

variable = 0



def create_window():
    window = tkinter.Toplevel(top)
    window.geometry('{}x{}'.format(512, 256))
   
    def close():
        window.destroy()
   
   
    def getText(event):
            CanvasController.canvasContainer.itemconfig(MouseMotionToController.clickedObjectOnCanvas[-2].text, text = e.get())
   
    button1 = tkinter.Button(window, text="Close", command=close, width = 50)
    button2 = tkinter.Button(window, text="OK", command=close,  width = 50)
    button1.pack(side = tkinter.BOTTOM)
    button2.pack(side = tkinter.BOTTOM)
    e = tkinter.Entry(window)
   
    e.bind("<Return>", getText)
    e.pack()


menubar = Menu(top)
editMenu = Menu(menubar, tearoff=0)
editMenu.add_command(label="Exit", command=top.quit)
editMenu.add_command(label="Edit Menu", command=create_window)
menubar.add_cascade(label="Setting", menu=editMenu)



initAllButtons(buttonsContainer)
initCanvasContainer(top)
initModeControllers()

top.config(menu = menubar)
top.mainloop()