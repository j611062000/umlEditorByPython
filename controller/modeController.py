from bridge import MouseMotionToController
from configuration import ConfigOfButton
from controller.buttonController import ButtonController
from decorators import overrides, trackMouseClickedObjs, trackMouseReleasedObjs
from objectOnCanvas import ClassObject, UseCaseObject, LineObject, GeneralizationLine, CompositiontionLine, CompositionObject, AssociationLine
from time import sleep


class ModeController():

    def __init__(self, nameOfMode):
        self.nameOfMode = nameOfMode
    
    def handleMouseClick(self, mouseEvent, canvasContainer):
        raise NotImplementedError


    def handleMousePressAndDrag(self, mouseEvent, canvasContainer):
        pass
    

    def handleMouseRelease(self, mouseEvent, canvasContainer):
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
    objIdOfSelectionArea = False

    def __init__(self):
        super().__init__(ConfigOfButton.nameOfSelect)

    def handleMouseRelease(self, mouseEvent, canvasContainer):
        if SelectModeController.objIdOfSelectionArea:
            canvasContainer.delete(self.objIdOfSelectionArea)
            SelectModeController.objIdOfSelectionArea = False
    


    @staticmethod
    def hideMultiSelectedObj():
         if MouseMotionToController.multiSelectedObjs:
                SelectModeController.hideAllPortsOfObjs()


    # @trackMouseClickedObjs
    def handleMouseClick(self, mouseEvent, canvasContainer):

        allShapeObjsOnCanvas = self.getAllShapeObjsOnCanvas()
        
        if ModeController.isClickOnShape():
            currentActiveObj = MouseMotionToController.getCurrentClickedObj()
            currentActiveObj.showPort()
            SelectModeController.hidePortsByObj(allShapeObjsOnCanvas, currentActiveObj)
            # SelectModeController.hideMultiSelectedObj()
            
            if CompositionObjectController.verifyClickedObjIsInGroup(currentActiveObj):
                CompositionObjectController.showAllObjs(currentActiveObj.groupIds[-1])

        else:
            SelectModeController.hidePortsByObj(allShapeObjsOnCanvas, None)
            # SelectModeController.hideMultiSelectedObj()

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
         
            if CompositionObjectController.verifyClickedObjIsInGroup(draggingObj):
                CompositionObjectController.moveAllObjsInAGroup(draggingObj.groupIds[-1], dx, dy)
         
            else:
                canvasContainer.move(draggingObj.idInCanvas, dx, dy)
                draggingObj.moveAttachedObjs(dx, dy)
        
        else:
            x1 = self.absXinDrage
            y1 = self.absYinDrage
            x2 = self.mouseClickX + dx
            y2 = self.mouseClickY + dy
            selectedObj = canvasContainer.find_enclosed(min(x1,x2), min(y1,y2), max(x1,x2), max(y1,y2))
            MouseMotionToController.flushmultiSelectedObjs()
            MouseMotionToController.multiSelectedObjs.extend(selectedObj)
            CompositionObjectController.groupCandidatesObj = self.getShapeObjsByIds(MouseMotionToController.multiSelectedObjs)
            SelectModeController.showAllPortsOfSelectedObjs()
            self.updateSelectionArea(canvasContainer, (x1, y1, x2, y2))

    
    @classmethod
    def updateSelectionArea(cls, canvasContainer, argsOfCoords):
        if not cls.objIdOfSelectionArea:
            cls.objIdOfSelectionArea = canvasContainer.create_rectangle(*argsOfCoords)
        else:
            canvasContainer.coords(cls.objIdOfSelectionArea, *argsOfCoords)


    @classmethod
    def getAllShapeObjsOnCanvas(cls):
        allShapeObjsOnCanvas = list()
        for mode in cls.compatibleModes:
            allShapeObjsOnCanvas.extend(mode.getAvailableObjs())
        return allShapeObjsOnCanvas


    @classmethod
    def getShapeObjsByIds(cls, ids):
        if not ids:
            return False
        else:
            allShapeObjsOnCanvas = cls.getAllShapeObjsOnCanvas()
            
            return MouseMotionToController.getObjById(ids,allShapeObjsOnCanvas)

    @classmethod
    def hidePortsByObj(cls, objs, currentActiveObj):
        print("enter hide port____")
        for obj in objs:
            if obj != currentActiveObj and obj:
                print("hide port", obj)
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
    def showAllPortsOfSelectedObjs(cls):
        for mode in cls.compatibleModes:
            cls.showPortsOfObjs(mode.getAvailableObjs(), MouseMotionToController.multiSelectedObjs)
 
       
class LineController(ModeController):

    availableLineObj = list()
    canvasContainer = None
    startPointObj = None
    endPointObj = None

    def __init__(self, nameOfMode):
        self.startPoint = None
        self.endPoint = None
        return super().__init__(nameOfMode)


    def newLine(self, startPointObj, endPointObj):
        raise NotImplementedError
    

    @classmethod
    def calDistanceOfTwoCoordinate(cls,x1,y1,x2,y2):
        dx = x1-x2
        dy = y1-y2
        return (dx**2+dy**2)**(1/2)


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
            self.startPointObj = clickedObj
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
        
        if currentReleasedObjId != False and ModeController.isClickOnShape():
            self.endPointObj = MouseMotionToController.getObjById(currentReleasedObjId, allShapeObjectsOnCanvas)
            portsCandidates = MouseMotionToController.getCurrentReleasedObj(allShapeObjectsOnCanvas).idOfPortInCanvas
            self.endPoint = LineController.getCoordOfClosestPort(portsCandidates, mouseEvent)
            self.newLine(self.startPointObj, self.endPointObj)

    @classmethod
    def findCoordById(cls, id):
        return cls.canvasContainer.coords(id)


class AssociationLinController(LineController):

    def __init__(self):
        super().__init__(ConfigOfButton.nameOfAssociationLine)

    def newLine(self, startPointObj, endPointObj):
        coordinate = [self.startPoint[0], self.startPoint[1], self.endPoint[0], self.endPoint[1]]
        self.availableLineObj.append(AssociationLine(self.canvasContainer, *coordinate, startPointObj, endPointObj))


class GeneralizationLinController(LineController):

    def __init__(self):
        return super().__init__(ConfigOfButton.nameOfGeneralizationLine)

    def newLine(self,startPointObj, endPointObj):
        coordinate = [self.startPoint[0], self.startPoint[1], self.endPoint[0], self.endPoint[1]]
        self.availableLineObj.append(GeneralizationLine(self.canvasContainer, *coordinate, startPointObj, endPointObj))


class CompositionLinController(LineController):

    def __init__(self):
        return super().__init__(ConfigOfButton.nameOfCompositionLine)

    def newLine(self,startPointObj, endPointObj):
        coordinate = [self.startPoint[0], self.startPoint[1], self.endPoint[0], self.endPoint[1]]
        self.availableLineObj.append(CompositiontionLine(self.canvasContainer, *coordinate,startPointObj, endPointObj))


class CompositionObjectController(ModeController):
    
    groupCandidatesObj = list()
    groupsOnCanvas = list()
    groupIdForNewGroup = 0

    @classmethod
    def killAGroup(cls):
        currentActiveObj = MouseMotionToController.getCurrentClickedObj()
        
        if CompositionObjectController.verifyClickedObjIsInGroup(currentActiveObj):
            groupId = currentActiveObj.groupIds[-1]
            flattenObjs = cls.getFlattenObjsByGroupId(groupId)
            
            for obj in flattenObjs:
                obj.groupIds.pop()

            for count, group in enumerate(cls.groupsOnCanvas):
                if group.groupId == groupId:
                    groupToBeDeleted = cls.groupsOnCanvas.pop(count)
                    del groupToBeDeleted
                    break
        else:
            pass
                


    @classmethod
    def getGroupById(cls, groupId):
        for group in cls.groupsOnCanvas:
            if group.groupId == groupId:
                return group

    @classmethod
    def getFlattenObjsByGroupId(cls, groupId):
        group = cls.getGroupById(groupId)
        return group.flattenInnerObjs


    @classmethod
    def moveAllObjsInAGroup(cls, groupId, dx, dy):
        objs = cls.getFlattenObjsByGroupId(groupId)
        for obj in objs:
            MouseMotionToController.canvasContainer.move(obj.idInCanvas, dx, dy)
            obj.moveAttachedObjs(dx, dy)


    @classmethod
    def createNewGroup(cls):
        cls.groupsOnCanvas.append(CompositionObject(cls.groupCandidatesObj,cls.groupIdForNewGroup))
        cls.groupIdForNewGroup += 1


    @classmethod
    def verifyClickedObjIsInGroup(cls, obj):
        if len(obj.groupIds) > 0:
            return True
        else:
            return False


    @classmethod
    def showAllObjs(cls, groupId):
        cls.getGroupById(groupId).showAllObjs()
       


