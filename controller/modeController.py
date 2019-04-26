from controller.buttonController import ButtonController
from bridge import MouseMotionToController
from configuration import ConfigOfButton
from objectOnCanvas import ClassObject, UseCaseObject, LineObject, GeneralizationLine, CompositiontionLine


class ModeController():
    
    def handleMouseClick(self, mouseEvent, canvasContainer):
        pass

    def handleMousePressAndDrag(self, mouseEvent, canvasContainer):
        pass

    def normalizeGUIWhenUnactive(self):
        pass
    
    def handleMouseRelease(self, mouseEvent, canvasContainer):
        pass
    
    @classmethod
    def verfiyLastClickIsOnShape(cls):
        if MouseMotionToController.modeOfClickedObjectOnCaanvas() == 3:
            return True
        else:
            return False
    


class ClassModeController(ModeController):

    nameOfMode = ConfigOfButton.nameOfClass
    availableClassModes = list()

    # @overrides(ModeController)
    def handleMouseClick(self, mouseEvent, canvasContainer):
        self.availableClassModes.append(ClassObject(mouseEvent, canvasContainer))
    
    @classmethod
    def availableObjs(cls):
        return cls.availableClassModes


class UseCaseModeController(ModeController):
    
    nameOfMode = ConfigOfButton.nameOfUseCase
    availableUseCaseModes = list()

    # @overrides(ModeController)
    def handleMouseClick(self, mouseEvent, canvasContainer):
        self.availableUseCaseModes.append(UseCaseObject(mouseEvent, canvasContainer))
    
    @classmethod
    def availableObjs(cls):
        return cls.availableUseCaseModes



class SelectModeController(ModeController):

    nameOfMode = ConfigOfButton.nameOfSelect
    mouseClickX = None
    mouseClickY = None
    absXinDrage = None
    absYinDrage = None

    def disablePortByObj(self, objects, currentActiveObj):
        for obj in objects:
            if obj != currentActiveObj and obj:
                obj.hidePort(obj)

    def handleMouseClick(self, mouseEvent, canvasContainer):

        if ModeController.verfiyLastClickIsOnShape():
            currentActiveObj = MouseMotionToController.clickedObjectOnCanvas[-2]
            self.disablePortByObj(MouseMotionToController.clickedObjectOnCanvas, currentActiveObj)
            self.batchdisablePortById()
            currentActiveObj.showPort()

        else:
            self.disablePortByObj(MouseMotionToController.clickedObjectOnCanvas, None)
            if MouseMotionToController.selectedObjectOnCanvas:
                self.batchdisablePortById()

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
        
        if ModeController.verfiyLastClickIsOnShape():
            draggingObj = MouseMotionToController.clickedObjectOnCanvas[-2]
            canvasContainer.move(draggingObj.idInCanvas, dx, dy)
            draggingObj.movePortWhenShapIsDragged(dx, dy)
        
        else:
            x1 = self.absXinDrage
            y1 = self.absYinDrage
            x2 = self.mouseClickX + dx
            y2 = self.mouseClickY + dy
            selectedObj = canvasContainer.find_enclosed(min(x1,x2), max(y1,y2), max(x1,x2), min(y1,y2))
            MouseMotionToController.flushselectedObjectOnCanvas()
            MouseMotionToController.selectedObjectOnCanvas.extend(selectedObj)
            self.batchinablePortById()
            # print(MouseMotionToController.selectedObjectOnCanvas)


    def isIdMatchObjects(self, objs, ids):
        tmp = list()
        for id in ids:
            for obj in objs:
                if obj.idInCanvas == id:
                    tmp.append(obj)
        return tmp
   

    def setMultipleObjePort(self, objs, ids):
        if self.isIdMatchObjects(objs, ids):
            for obj in self.isIdMatchObjects(objs, ids):
                obj.showPort()
        
    def disablePortById(self, objs, ids):
        for obj in self.isIdMatchObjects(objs, ids):
            obj.hidePort(obj)

    def batchdisablePortById(self):
        self.disablePortById(ClassModeController.availableObjs(), MouseMotionToController.selectedObjectOnCanvas)
        self.disablePortById(UseCaseModeController.availableObjs(), MouseMotionToController.selectedObjectOnCanvas)


    def batchinablePortById(self):
        self.setMultipleObjePort(ClassModeController.availableObjs(), MouseMotionToController.selectedObjectOnCanvas)
        self.setMultipleObjePort(UseCaseModeController.availableObjs(), MouseMotionToController.selectedObjectOnCanvas)
 

    
    
class LineController(ModeController):

    nameOfMode = None
    availableLineMode = list()
    # coordinates
    startPoint = None
    endPoint = None
    belongRegion = None
    canvasContainer = None

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
        if ModeController.verfiyLastClickIsOnShape():
            startObjId = cls.canvasContainer.find_closest(mouseEvent.x, mouseEvent.y)
            cls.startPoint = cls.canvasContainer.coords(startObjId)
            print("test",cls.startPoint)
            
    
    
    @classmethod
    def handleMouseRelease(cls, mouseEvent, canvasContainer):
        cls.canvasContainer = canvasContainer
        # idOfEndObj = MouseMotionToController.idOfMouseReleaseObject[-1]
        # objs = [ClassModeController.availableClassModes, UseCaseModeController.availableUseCaseModes]
        # endObj = cls.findShapeObjById(objs,idOfEndObj)
        # MouseMotionToController.flushMouseReleaseOnObjectOfCanvas()
        # cls.endPoint = cls.calEndPoint(mouseEvent, endObj)
        endObjId = cls.canvasContainer.find_closest(mouseEvent.x, mouseEvent.y)
        cls.endPoint = cls.canvasContainer.coords(endObjId)

        cls.newLine()


    # @classmethod
    # def pointHelpler(cls, mouseEvent, targetShapeObj):
    #     centerX = sum([port[0] for port in targetShapeObj.coordinateOfPort])/4
    #     centerY = sum([port[1] for port in targetShapeObj.coordinateOfPort])/4
    #     cls.belongRegion = cls.calBelongRegion(targetShapeObj.plusSlope, targetShapeObj.negativeSlope,centerX, centerY, mouseEvent.x, mouseEvent.y)
    #     return cls.findOutTheDrawPoint(targetShapeObj.coordinateOfPort, cls.belongRegion)


    # @classmethod
    # def calEndPoint(cls, mouseEvent, endObj):
    #     return cls.pointHelpler(mouseEvent, endObj)


    # @classmethod
    # def calStartPoint(cls, mouseEvent, startObj):
    #     return cls.pointHelpler(mouseEvent, startObj)
       


    # @classmethod
    # def availableObjs(cls):
    #     return cls.availableLineMode

    # @classmethod
    # def calSlope(cls, x1, y1, x2, y2):
    #     return (y2-y1)/(x2-x1)
    
    # @classmethod 
    # def findOutTheDrawPoint(cls, ports, belongPostion):
    #     if belongPostion == "TOP":
    #         return sorted(ports, key = lambda port: port[1], reverse = True)[0]
            
    #     elif belongPostion == "BOTTOM":
    #         return sorted(ports, key = lambda port: port[1], reverse = False)[0]

    #     elif belongPostion == "RIGHT":
    #         return sorted(ports, key = lambda port: port[0], reverse = True)[0]

    #     elif belongPostion == "LEFT":
    #         return sorted(ports, key = lambda port: port[1], reverse = False)[0]



    # @classmethod
    # def calBelongRegion(cls, plusSlope, negativeSlope, centerX, centerY, x, y):
    #     slope = cls.calSlope(x, y, centerX, centerY)
    #     if x >= centerX:
    #         if slope >= plusSlope:
    #             return "TOP"
    #         elif slope <= negativeSlope:
    #             return "BOTTOM"
    #         else:
    #             return "RIGHT"
        
    #     else:
    #         if slope >= plusSlope:
    #             return "BOTTOM"
    #         elif slope <= negativeSlope:
    #             return "TOP"
    #         else:
    #             return "LEFT"

class associationLinController(LineController):
    nameOfMode = ConfigOfButton.nameOfAssociationLine

    @classmethod
    def newLine(cls):
        coordinate = [cls.startPoint[0], cls.startPoint[1], cls.endPoint[0], cls.endPoint[1]]
        cls.availableLineMode.append(LineObject(cls.canvasContainer, *coordinate))

class generalizationLinController(LineController):
    nameOfMode = ConfigOfButton.nameOfGeneralizationLine

    @classmethod
    def newLine(cls):
        coordinate = [cls.startPoint[0], cls.startPoint[1], cls.endPoint[0], cls.endPoint[1]]
        cls.availableLineMode.append(GeneralizationLine(cls.canvasContainer, *coordinate))

class compositionLinController(LineController):
    nameOfMode = ConfigOfButton.nameOfCompositionLine

    @classmethod
    def newLine(cls):
        coordinate = [cls.startPoint[0], cls.startPoint[1], cls.endPoint[0], cls.endPoint[1]]
        cls.availableLineMode.append(CompositiontionLine(cls.canvasContainer, *coordinate))