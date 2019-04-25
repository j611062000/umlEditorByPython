from controller.buttonController import ButtonController
from bridge import MouseMotionToController
from configuration import ConfigOfButton
from objectOnCanvas import ClassObject, UseCaseObject


class ModeController():
    
    def handleMouseClick(self, mouseEvent, canvasContainer):
        pass

    def handleMousePressAndDrag(self, mouseEvent, canvasContainer):
        pass

    def normalizeGUIWhenUnactive(self):
        pass


class ClassModeController(ModeController):

    nameOfMode = ConfigOfButton.nameOfClass
    availableClassModes = list()

    # @overrides(ModeController)
    def handleMouseClick(self, mouseEvent, canvasContainer):
        self.availableClassModes.append(ClassObject(mouseEvent, canvasContainer))

class UseCaseModeController(ModeController):
    
    nameOfMode = ConfigOfButton.nameOfUseCase
    availableUseCaseModes = list()

    # @overrides(ModeController)
    def handleMouseClick(self, mouseEvent, canvasContainer):
        self.availableUseCaseModes.append(UseCaseObject(mouseEvent, canvasContainer))


class SelectModeController(ModeController):

    nameOfMode = ConfigOfButton.nameOfSelect
    mouseClickX = None
    mouseClickY = None
    absXinDrage = None
    absYinDrage = None

    def normalizePorts(self, objects, currentActiveObj):
        for obj in objects:
            if obj != currentActiveObj and obj:
                obj.hidePort(obj)

    def handleMouseClick(self, mouseEvent, canvasContainer):
        if SelectModeController.verfiyTheLastActtion():
            currentActiveObj = MouseMotionToController.clickedObjectOnCanvas[-2]
            self.normalizePorts(MouseMotionToController.clickedObjectOnCanvas, currentActiveObj)
        else:
            self.normalizePorts(MouseMotionToController.clickedObjectOnCanvas, None)
        
        self.mouseClickX = mouseEvent.x
        self.mouseClickY = mouseEvent.y
        self.absXinDrage = mouseEvent.x
        self.absYinDrage = mouseEvent.y

    # @overrides(ModeController)
    def handleMousePressAndDrag(self, mouseEvent, canvasContainer):
        
        dx = mouseEvent.x - self.mouseClickX
        dy = mouseEvent.y - self.mouseClickY
        self.mouseClickX += dx
        self.mouseClickY += dy
        
        if SelectModeController.verfiyTheLastActtion():
            draggingObj = MouseMotionToController.clickedObjectOnCanvas[-2]
            canvasContainer.move(draggingObj.idInCanvas, dx, dy)
            draggingObj.movePortWhenShapIsDragged(dx, dy)
        
        else:
            x1 = self.absXinDrage
            y1 = self.absYinDrage
            x2 = self.mouseClickX + dx
            y2 = self.mouseClickY + dy
            print(x1,y1,x2,y2)
            MouseMotionToController.selectedObjectOnCanvas.
            canvasContainer.find_enclosed(min(x1,x2), max(y1,y2), max(x1,x2), min(y1,y2)))
        
            
    
    @classmethod
    def verfiyTheLastActtion(cls):
        if MouseMotionToController.modeOfClickedObjectOnCaanvas() == 3:
            return True
        else:
            return False
    
    
      