from controller.buttonController import ButtonController
from bridge import MouseMotionToController
from configuration import ConfigOfButton
from objectOnCanvas import ClassObject, UseCaseObject

# class GeneralModeController():

#     availableModes = list()
#     canvasContainer = None

#     @classmethod
#     def findWhichModeShouldBeActive(cls):
#         for mode in cls.availableModes:
#             if mode.nameOfMode == ButtonController.currentActiveButton:
#                 return mode

#     @classmethod
#     def handleClickOnCanvas(cls, mouseEvent):
#         mode = cls.findWhichModeShouldBeActive()
#         mode.handleMouseClick(mouseEvent, cls.canvasContainer)
    
#     @classmethod
#     def handlePressAndDragOnCanvas(cls, mouseEvent):
#         mode = cls.findWhichModeShouldBeActive()        
#         mode.handleMousePressAndDrag(mouseEvent, cls.canvasContainer)


class ModeController():
    
    def handleMouseClick(self, mouseEvent, canvasContainer):
        pass


    def handleMousePressAndDrag(self, mouseEvent, canvasContainer):
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

    # @overrides(ModeController)
    def handleMouseClick(self, mouseEvent, canvasContainer):
        self.mouseClickX = mouseEvent.x
        self.mouseClickY = mouseEvent.y
        print("selcetmode")

    # @overrides(ModeController)
    def handleMousePressAndDrag(self, mouseEvent, canvasContainer):
        dx = mouseEvent.x - self.mouseClickX
        dy = mouseEvent.y - self.mouseClickY
        self.mouseClickX += dx
        self.mouseClickY += dy
        canvasContainer.move(MouseMotionToController.currentActiveObjectOnCanvas.idInCanvas, dx, dy)
