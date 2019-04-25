from  controller.buttonController import ButtonController
from bridge import MouseMotionToController
from configuration import ConfigOfButton
from objectOnCanvas import ClassObject, UseCaseObject

class CanvasController():
    
    availableModes = list()
    canvasContainer = None

    @classmethod
    def findWhichModeShouldBeActive(cls):
        for mode in cls.availableModes:
            if mode.nameOfMode == ButtonController.currentActiveButton:
                return mode

    @classmethod
    def handleClickOnCanvas(cls, mouseEvent):
        CanvasController.handlePortWhenDirectlyClickOnCanvas()

        mode = cls.findWhichModeShouldBeActive()
        mode.handleMouseClick(mouseEvent, cls.canvasContainer)
    
    @classmethod
    def handlePressAndDragOnCanvas(cls, mouseEvent):
        mode = cls.findWhichModeShouldBeActive()        
        mode.handleMousePressAndDrag(mouseEvent, cls.canvasContainer)
    
    @classmethod
    def handlePortWhenDirectlyClickOnCanvas(cls):
        if MouseMotionToController.currentActiveObjectOnCanvas == None:
            if MouseMotionToController.lastActiveObjectOnCanvas != None:
                lastActive = MouseMotionToController.lastActiveObjectOnCanvas
                lastActive.hidePort(lastActive)

