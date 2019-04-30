from bridge import MouseMotionToController
from configuration import ConfigOfButton
from controller.buttonController import ButtonController
from objectOnCanvas import ClassObject, UseCaseObject, LineObject, GeneralizationLine, CompositiontionLine
from decorators import overrides, trackMouseClickedObjs, trackMouseReleasedObjs


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
    
    @staticmethod
    def isClickOnCanvas():

        return MouseMotionToController.whatIsClickedByMouse() == MouseMotionToController.CLICK_ON_CANVAS

    @staticmethod
    def isClickOnShape():

        return MouseMotionToController.whatIsClickedByMouse() == MouseMotionToController.CLICK_ON_OBJECT
    
    @classmethod
    def isACoordinateInGivenRange(cls, coord, coords):
        inTheRangeOfX = None
        inTheRangeOfY = None

        if coord[0] >= coords[0] and coord[0] <= coords[2]:
            inTheRangeOfX = True
        
        if coord[1] >= coords[1] and coord[1] <= coords[3]:
            inTheRangeOfY = True
        
        return (inTheRangeOfX) and (inTheRangeOfY)

class ShapeController(ModeController):


    def __init__(self, nameOfMode):
        super().__init__(nameOfMode)
    

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

    
    @staticmethod
    def hideMultiSelectedObj():
         if MouseMotionToController.multiSelectedObjs:
                SelectModeController.hideAllPortsOfObjs()


    # @trackMouseClickedObjs
    def handleMouseClick(self, mouseEvent, canvasContainer):
        
        if ModeController.isClickOnShape():
            currentActiveObj = MouseMotionToController.getCurrentClickedObj()
            SelectModeController.hidePortsByObj(MouseMotionToController.singleClickedObj, currentActiveObj)
            SelectModeController.hideMultiSelectedObj()
            currentActiveObj.showPort()

        else:
            SelectModeController.hidePortsByObj(MouseMotionToController.singleClickedObj, None)
            SelectModeController.hideMultiSelectedObj()

        self.mouseClickX = mouseEvent.x
        self.mouseClickY = mouseEvent.y
        self.absXinDrage = mouseEvent.x
        self.absYinDrage = mouseEvent.y

    @overrides
    def handleMousePressAndDrag(self, mouseEvent, canvasContainer):
        dx = mouseEvent.x - self.mouseClickX
        dy = mouseEvent.y - self.mouseClickY
        self.mouseClickX += dx
        self.mouseClickY += dy
        
        if ModeController.isClickOnShape():
            draggingObj = MouseMotionToController.getCurrentClickedObj()
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
            SelectModeController.showAllPortsOfObjs()

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

    @classmethod
    def showAllPortsOfObjs(cls):
        for mode in cls.compatibleModes:
            cls.showPortsOfObjs(mode.getAvailableObjs(), MouseMotionToController.multiSelectedObjs)
 
       
class LineController(ModeController):

    availableLineObj = list()
    canvasContainer = None
    # startPoint = None
    # endPoint = None

    def __init__(self, nameOfMode):
        self.startPoint = None
        self.endPoint = None
        return super().__init__(nameOfMode)


    @classmethod
    def calDistanceOfTwoCoordinate(cls,x1,y1,x2,y2):
        dx = x1-x2
        dy = y1-y2
        return (dx**2+dy**2)**(1/2)


    def newLine(self):
        raise NotImplementedError
    
    @classmethod
    def getAllShapeObjsOnCanvas(cls):
        allShapeObjectsOnCanvas = list()
           
        for mode in SelectModeController.compatibleModes:
            allShapeObjectsOnCanvas.extend(mode.getAvailableObjs())
        
        return allShapeObjectsOnCanvas


    @classmethod
    def getCoordOfClosestPort(cls, portsCandidates, mouseEvent):
        minDistance = float("inf")
        winnerOfPorts = None
        for candidate in portsCandidates:
            distance = cls.calDistanceOfTwoCoordinate(mouseEvent.x, mouseEvent.y,*cls.findCoordById(candidate)[:2])
            if distance < minDistance:
                minDistance = distance
                winnerOfPorts = cls.canvasContainer.coords(candidate)[:2]
        return winnerOfPorts


    def handleMouseClick(self, mouseEvent, canvasContainer):
        LineController.canvasContainer = canvasContainer
        if ModeController.isClickOnShape():
            clickedObj = MouseMotionToController.getCurrentClickedObj()
            portsCandidates = clickedObj.idOfPortInCanvas
            self.startPoint = LineController.getCoordOfClosestPort(portsCandidates, mouseEvent)
    
    
    def handleMouseRelease(self, mouseEvent, canvasContainer):

        allShapeObjectsOnCanvas = self.getAllShapeObjsOnCanvas()
        for obj in allShapeObjectsOnCanvas:
            if obj != False:
                if self.isACoordinateInGivenRange((mouseEvent.x, mouseEvent.y), self.canvasContainer.coords(obj.idInCanvas)):
                    currentReleasedObjId = self.canvasContainer.find_closest(mouseEvent.x, mouseEvent.y, 5)
                    break
                else:
                    currentReleasedObjId = False
            else:
                currentReleasedObjId = False

        MouseMotionToController.mouseReleasedObjId.append(currentReleasedObjId)
        
        
        if ModeController.isClickOnShape():
            portsCandidates = MouseMotionToController.getCurrentReleasedObj(allShapeObjectsOnCanvas).idOfPortInCanvas
            self.endPoint = LineController.getCoordOfClosestPort(portsCandidates, mouseEvent)
            self.newLine()

    @classmethod
    def findCoordById(cls, id):
        return cls.canvasContainer.coords(id)


class AssociationLinController(LineController):

    def __init__(self):
        super().__init__(ConfigOfButton.nameOfAssociationLine)

    def newLine(self):
        coordinate = [self.startPoint[0], self.startPoint[1], self.endPoint[0], self.endPoint[1]]
        self.availableLineObj.append(LineObject(self.canvasContainer, *coordinate))


class GeneralizationLinController(LineController):

    def __init__(self):
        return super().__init__(ConfigOfButton.nameOfGeneralizationLine)

    def newLine(self):
        coordinate = [self.startPoint[0], self.startPoint[1], self.endPoint[0], self.endPoint[1]]
        self.availableLineObj.append(GeneralizationLine(self.canvasContainer, *coordinate))


class CompositionLinController(LineController):

    def __init__(self):
        return super().__init__(ConfigOfButton.nameOfCompositionLine)

    def newLine(self):
        coordinate = [self.startPoint[0], self.startPoint[1], self.endPoint[0], self.endPoint[1]]
        self.availableLineObj.append(CompositiontionLine(self.canvasContainer, *coordinate))