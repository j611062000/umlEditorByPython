import tkinter

from initController import *

top = tkinter.Tk()

buttonsContainer = tkinter.Frame(top)
buttonsContainer.pack(side = tkinter.LEFT)

menubar = tkinter.Menu(top)

initAllButtons(buttonsContainer)
initCanvasContainer(top)
initModeControllers()

top.mainloop()