from bridge import MouseMotionToController
from configuration import ConfigOfButton
from controller.buttonController import ButtonController
from objectOnCanvas import ClassObject, UseCaseObject, LineObject, GeneralizationLine, CompositiontionLine
from decorators import overrides, trackMouseClickedObjs


class ModeController():

    def __init__(self, nameOfMode):
        self.nameOfMode = nameOfMode
    
    def handleMouseClick(self, mouseEvent, canvasContainer):
        pass


    def handleMousePressAndDrag(self, mouseEvent, canvasContainer):
        pass
    

    def handleMouseRelease(self, mouseEvent, canvasContainer):
        pass


    def normalizeGUIWhenUnactive(self):
        pass
    
    

class ShapeController(ModeController):

    def __init__(self, nameOfMode):
        super().__init__(nameOfMode)
   
    
    @staticmethod
    def verfiyLastClickIsOnShape():
        if MouseMotionToController.whatIsClickedByMouse() == MouseMotionToController.CLICK_ON_OBJECT:
            return True
        else:
            return False


class ClassModeController(ShapeController):

    availableObjOnCanvas = list()

    def __init__(self):
        super().__init__(ConfigOfButton.nameOfClass)

    @overrides
    def handleMouseClick(self, mouseEvent, canvasContainer):
        self.availableObjOnCanvas.append(ClassObject(mouseEvent, canvasContainer))
    
    @classmethod
    def getAvailableObjs(cls):
        return cls.availableObjOnCanvas
    

class UseCaseModeController(ShapeController):

    availableObjOnCanvas = list()

    
    def __init__(self):
        super().__init__(ConfigOfButton.nameOfUseCase)

    @overrides
    def handleMouseClick(self, mouseEvent, canvasContainer):
        self.availableObjOnCanvas.append(UseCaseObject(mouseEvent, canvasContainer))
    
    @classmethod
    def getAvailableObjs(cls):
        return cls.availableObjOnCanvas


class SelectModeController(ModeController):

    # should be revised when new mode added
    compatibleModes = [ClassModeController, UseCaseModeController]
    mouseClickX = None
    mouseClickY = None
    absXinDrage = None
    absYinDrage = None

    def __init__(self):
        super().__init__(ConfigOfButton.nameOfSelect)

    def clickOnCanvas():
    def clickOnShape():

    @trackMouseClickedObjs
    def handleMouseClick(self, mouseEvent, canvasContainer):
        
        # {no selected, single selected, multi selected} x {click on shape, click on canvas, drag}
        if ShapeController.verfiyLastClickIsOnShape():
            currentActiveObj = MouseMotionToController.singleClickedObj[-2]
            # SelectModeController.hidePortsByObj(MouseMotionToController.singleClickedObj, currentActiveObj)
            SelectModeController.hideAllPortsOfObjs()
            currentActiveObj.showPort()

        else:
            SelectModeController.hidePortsByObj(MouseMotionToController.singleClickedObj, None)
            if MouseMotionToController.multiSelectedObjs:
                SelectModeController.hideAllPortsOfObjs()

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
        
        if ShapeController.verfiyLastClickIsOnShape():
            draggingObj = MouseMotionToController.singleClickedObj[-2]
            canvasContainer.move(draggingObj.idInCanvas, dx, dy)
            draggingObj.movePortWhenShapIsDragged(dx, dy)
        
        else:
            x1 = self.absXinDrage
            y1 = self.absYinDrage
            x2 = self.mouseClickX + dx
            y2 = self.mouseClickY + dy
            selectedObj = canvasContainer.find_enclosed(min(x1,x2), max(y1,y2), max(x1,x2), min(y1,y2))
            MouseMotionToController.flushmultiSelectedObjs()
            MouseMotionToController.multiSelectedObjs.extend(selectedObj)
            self.showAllPortsOfObjs()
            # print(MouseMotionToController.multiSelectedObjs)

    @classmethod
    def hidePortsByObj(cls, objs, currentActiveObj):
        for obj in objs:
            if obj != currentActiveObj and obj:
                obj.hidePort(obj)

    @classmethod
    def hidePortsByIds(cls, objs, ids):
        for obj in cls.getMatchedObjsByIds(objs, ids):
            obj.hidePort(obj)

    @classmethod
    def showPortsOfObjs(cls, objs, ids):
        if cls.getMatchedObjsByIds(objs, ids):
            for obj in cls.getMatchedObjsByIds(objs, ids):
                obj.showPort()
    
    @classmethod
    def getMatchedObjsByIds(cls, objs, ids):
        tmp = list()
        for id in ids:
            for obj in objs:
                if obj.idInCanvas == id:
                    tmp.append(obj)
        return tmp
   
    @classmethod
    def hideAllPortsOfObjs(cls):
        for mode in cls.compatibleModes:
            cls.hidePortsByIds(mode.getAvailableObjs(), MouseMotionToController.multiSelectedObjs)


    def showAllPortsOfObjs(cls):
        for mode in cls.compatibleModes:
            cls.showPortsOfObjs(mode.getAvailableObjs(), MouseMotionToController.multiSelectedObjs)
 

    
    
class LineController(ModeController):

    availableLineMode = list()
    # coordinates
    startPoint = None
    endPoint = None
    belongRegion = None
    canvasContainer = None

    def __init__(self, nameOfMode):
        return super().__init__(nameOfMode)

    @classmethod
    def findShapeObjById(cls, objs, id):
        for obj in objs[0]:
            if obj.idInCanvas == id[0]:
                return obj
        for obj in objs[1]:
            if obj.idInCanvas == id[0]:
                return obj


    @classmethod
    def newLine(cls):
        coordinate = [cls.startPoint[0], cls.startPoint[1], cls.endPoint[0], cls.endPoint[1]]
        cls.availableLineMode.append(LineObject(cls.canvasContainer, *coordinate))
    
    @classmethod
    def handleMouseClick(cls, mouseEvent, canvasContainer):
        cls.canvasContainer = canvasContainer
        if ShapeController.verfiyLastClickIsOnShape():
            startCo = cls.findCoordById(cls.canvasContainer.find_closest(mouseEvent.x, mouseEvent.y))
            startObjId = cls.canvasContainer.find_closest(mouseEvent.x, mouseEvent.y,start = startCo)
            cls.startPoint = cls.canvasContainer.coords(startObjId)
            print("start",startObjId)
            
    
    
    @classmethod
    def handleMouseRelease(cls, mouseEvent, canvasContainer):
        cls.canvasContainer = canvasContainer
        endObjId = cls.canvasContainer.find_closest(mouseEvent.x, mouseEvent.y)
        cls.endPoint = cls.canvasContainer.coords(endObjId)
        print("end",cls.endPoint)


        cls.newLine()

    @classmethod
    def findCoordById(cls, id):
        return cls.canvasContainer.coords(id)

class AssociationLinController(LineController):

    def __init__(self):
        super().__init__(ConfigOfButton.nameOfAssociationLine)

    @classmethod
    def newLine(cls):
        coordinate = [cls.startPoint[0], cls.startPoint[1], cls.endPoint[0], cls.endPoint[1]]
        cls.availableLineMode.append(LineObject(cls.canvasContainer, *coordinate))

class GeneralizationLinController(LineController):

    def __init__(self):
        return super().__init__(ConfigOfButton.nameOfGeneralizationLine)

    @classmethod
    def newLine(cls):
        coordinate = [cls.startPoint[0], cls.startPoint[1], cls.endPoint[0], cls.endPoint[1]]
        cls.availableLineMode.append(GeneralizationLine(cls.canvasContainer, *coordinate))

class CompositionLinController(LineController):

    def __init__(self):
        return super().__init__(ConfigOfButton.nameOfCompositionLine)

    @classmethod
    def newLine(cls):
        coordinate = [cls.startPoint[0], cls.startPoint[1], cls.endPoint[0], cls.endPoint[1]]
        cls.availableLineMode.append(CompositiontionLine(cls.canvasContainer, *coordinate))