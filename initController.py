import tkinter

from buttons import Button as bt
from controller.buttonController import ButtonController
from configuration import ConfigOfButton, ConfigOfCanvas
from controller.canvasController import CanvasController
from modeController import *

def initAllButtons(master):
    
    associationLine = bt(master,ConfigOfButton.nameOfAssociationLine)
    class_          = bt(master,ConfigOfButton.nameOfClass)
    compositionLine = bt(master,ConfigOfButton.nameOfCompositionLine)
    generalizationLine = bt(master,ConfigOfButton.nameOfGeneralizationLine)
    select             = bt(master,ConfigOfButton.nameOfSelect)
    useCase            = bt(master,ConfigOfButton.nameOfUseCase)

    buttons = [select, associationLine, generalizationLine, compositionLine, class_, useCase]
    
    for button in buttons:
        button.pack()

    
    ButtonController.knwoWhatAreAvailableButtons(buttons)

    return buttons


def initCanvasContainer(master):
    
    canvasContainer = tkinter.Canvas(master)
    canvasContainer.configure(bg = "white", height = ConfigOfCanvas.heightOfInitCanvas, width = ConfigOfCanvas.widthOfInitCanvas)
    canvasContainer.pack(side = tkinter.LEFT)
    
    addMouseListenerToCanvas(canvasContainer)
    
    CanvasController.canvasContainer = canvasContainer


# Should be revised when there is mouse action added
def addMouseListenerToCanvas(canvasContainer):
    canvasContainer.bind("<Button-1>", CanvasController.handleClickOnCanvas)
    canvasContainer.bind("<B1-Motion>", CanvasController.handlePressAndDragOnCanvas)


# Should be revised when there is new mode added
def initModeControllers():
    CanvasController.availableModes.append(ClassModeController())
    CanvasController.availableModes.append(SelectModeController())
    CanvasController.availableModes.append(UseCaseModeController())