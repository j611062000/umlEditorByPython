import tkinter

from controller.buttonController import ButtonController

class Button(tkinter.Button):


        def __init__(self, master, nameOfButton):
            tkinter.Button.__init__(self, master,text = nameOfButton, width = 20,height = 3 ,font = ("Helvetica", 20))
            self.bind("<Button-1>", self.activateThisButton)
            self.nameOfButton = nameOfButton
        
        def activateThisButton(self, event):
            self.configure(background = "black", fg="white")
            ButtonController.knwoWhatIsCurrentActiveButton(self.nameOfButton)
            ButtonController.deactivateUnnecessaryButtons()
        