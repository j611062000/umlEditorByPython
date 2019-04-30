from controller.buttonController import ButtonController
from bridge import MouseMotionToController

def trackMouseAction(mouseEvent, actionName):
    print(actionName+"x:{}, Y:{}".format(mouseEvent.x, mouseEvent.y))


class CanvasController():
    
    availableModes = list()
    canvasContainer = None
    
    @classmethod
    def findWhichModeShouldBeActive(cls):
        currentActiveMode = None
        for mode in cls.availableModes:
            if mode.nameOfMode == ButtonController.currentActiveButton:
                currentActiveMode = mode
                break
            
        return currentActiveMode


    @classmethod
    def handleClickOnCanvas(cls, mouseEvent):
        # trackMouseAction(mouseEvent, "click")
        MouseMotionToController.singleClickedObj.append(False)
        currentActiveMode = cls.findWhichModeShouldBeActive()
        currentActiveMode.handleMouseClick(mouseEvent, cls.canvasContainer)
    

    @classmethod
    def handlePressAndDragOnCanvas(cls, mouseEvent):
        currentActiveMode = cls.findWhichModeShouldBeActive()        
        currentActiveMode.handleMousePressAndDrag(mouseEvent, cls.canvasContainer)
    
    
 


    @classmethod
    def handleMouseReleaseOnCanvas(cls, mouseEvent):
        # trackMouseAction(mouseEvent, "Release")
        currentActiveMode = cls.findWhichModeShouldBeActive()  
        currentActiveMode.handleMouseRelease(mouseEvent, cls.canvasContainer)

    
   

