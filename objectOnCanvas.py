import tkinter
from bridge import MouseMotionToController
from controller.buttonController import ButtonController
from decorators import trackMouseClickedObjs, callOnlyInSelectMode

# Bugs: port can't not work occassionally


class TwoDimensionShape():

    canvasContainer = None
    fillColorOfShape = "grey"
    fillColorOfPort = "black"

    def __init__(self, canvasContainer, createMethod, shiftX, shiftY, mouseEvent, textName):
        TwoDimensionShape.canvasContainer = canvasContainer
        self.coordinateOfPort = list()
        self.idOfPortInCanvas = list()
        self.textName = textName
        self.lineObjs = list()
        self.idInCanvas = TwoDimensionShape.instantiateToCanvas(createMethod, shiftX, shiftY, mouseEvent)
        self.updateCoordinateOfPort(mouseEvent, shiftX, shiftY)
        self.centerCoordinate = (mouseEvent.x+shiftX/2, mouseEvent.y+shiftY/2)
        self.text = self.instantiateText()
        self.bindToCanvasWithMouseEvent(self.idInCanvas)
        self.groupIds = list()
        self.layer = 0
        
    def handleMouseClickEvent(self, event):
        MouseMotionToController.singleClickedObj.append(self)

        TwoDimensionShape.canvasContainer.tag_raise(self.idInCanvas)
        self.raisePortToFront()
        self.raiseTextToFront()
        self.showPort()
        self.raiseHeadOfLineToFront()

    def handleMouseReleaseEvent(self, event):
        # MouseMotionToController.mouseReleasedObj.append(self)
        pass

    def bindToCanvasWithMouseEvent(self, bindingShape):
        pressHandler = self.handleMouseClickEvent
        releaseHandler = self.handleMouseReleaseEvent
        TwoDimensionShape.canvasContainer.tag_bind(bindingShape, '<Button-1>', pressHandler)
        TwoDimensionShape.canvasContainer.tag_bind(bindingShape, '<ButtonRelease-1>', releaseHandler)
    
    def instantiatePorts(self, coordinateOfPort, normOfPort):
        methodOfCreation = TwoDimensionShape.canvasContainer.create_oval
        for port in coordinateOfPort:
            self.idOfPortInCanvas.append(TwoDimensionShape.instantiateToCanvas(methodOfCreation, normOfPort, normOfPort, port))
    
    def instantiateText(self):
        idOfText = TwoDimensionShape.canvasContainer.create_text(*self.centerCoordinate,text = self.textName)
        self.bindToCanvasWithMouseEvent(idOfText)
        return idOfText


    def updateCoordinateOfPort(self, mouseEvent, shiftX, shiftY):
        
        normalizeOfPositionForPort = 5

        left = [(mouseEvent.x)-normalizeOfPositionForPort, (mouseEvent.y+shiftY/2)]
        top =  [(mouseEvent.x+shiftX/2), (mouseEvent.y)-normalizeOfPositionForPort]
        right =  [(mouseEvent.x+shiftX), (mouseEvent.y+shiftY/2)]
        bottom = [(mouseEvent.x+shiftX/2), (mouseEvent.y+shiftY)]
        
        self.coordinateOfPort = [left, top, right, bottom]
        self.instantiatePorts(self.coordinateOfPort, normalizeOfPositionForPort)

    @callOnlyInSelectMode
    def showPort(self):
        for portId in self.idOfPortInCanvas:
            TwoDimensionShape.canvasContainer.itemconfig(portId, state = tkinter.NORMAL)

    def hidePort(self, objecOfShape):
        if objecOfShape != None:
            for portId in objecOfShape.idOfPortInCanvas:
                TwoDimensionShape.canvasContainer.itemconfig(portId, state = tkinter.HIDDEN)

    def raiseHeadOfLineToFront(self):
        for lineobj in self.lineObjs:
            if lineobj.startPointObj == self and lineobj.objIdUsedToOverrideHead != None:
                TwoDimensionShape.canvasContainer.tag_raise(lineobj.objIdUsedToOverrideHead)
                TwoDimensionShape.canvasContainer.itemconfig(lineobj.objIdUsedToOverrideHead, state = tkinter.NORMAL)


    def raisePortToFront(self):
        for port in self.idOfPortInCanvas:
            TwoDimensionShape.canvasContainer.tag_raise(port)


    def raiseTextToFront(self):
        TwoDimensionShape.canvasContainer.tag_raise(self.text)

    
    def moveAttachedObjs(self, dx, dy):
        for idOfPort in self.idOfPortInCanvas:
            TwoDimensionShape.canvasContainer.move(idOfPort, dx, dy)
        
        TwoDimensionShape.canvasContainer.move(self.text, dx, dy)

        for lineObj in self.lineObjs:
            lineObj.updatePostion(self, dx, dy)


    @classmethod
    def instantiateToCanvas(cls, methodOfCreation, shiftX, shiftY, mouseEvent):
        try:
            # shape
            return methodOfCreation(mouseEvent.x, mouseEvent.y,mouseEvent.x+shiftX,mouseEvent.y+shiftY, fill = TwoDimensionShape.fillColorOfShape, tags = "shape")
        except:
            # port
            return methodOfCreation(mouseEvent[0], mouseEvent[1],mouseEvent[0]+shiftX,mouseEvent[1]+shiftY, fill = TwoDimensionShape.fillColorOfPort, state = tkinter.HIDDEN)

        

class ClassObject(TwoDimensionShape):

    def __init__(self, mouseEvent, canvasContainer):
        super().__init__(canvasContainer, canvasContainer.create_rectangle, 100, 140, mouseEvent, "Class")
    
class UseCaseObject(TwoDimensionShape):
    
    def __init__(self, mouseEvent, canvasContainer):
        super().__init__(canvasContainer, canvasContainer.create_oval, 140, 100, mouseEvent, "UseCase")

    # def instantiateText(self):
        # return TwoDimensionShape.canvasContainer.create_text(*self.centerCoordinate,text = "Use Case")

class LineObject():
      
    canvasContainer = None
    
    def __init__(self, canvasContainer,x1, y1, x2, y2, startPointObj, endPointObj):
        LineObject.canvasContainer = canvasContainer
        self.objIdUsedToOverrideHead = None
        self.idInCanvas = self.instantiateToCanvas(x1, y1, x2, y2)
        self.startPointObj = startPointObj
        self.endPointObj = endPointObj
        self.startPointCoords = [x1,y1]
        self.endPointCoords = [x2, y2]
        startPointObj.lineObjs.append(self)
        endPointObj.lineObjs.append(self)
    
    def instantiateToCanvas(self,x1, y1, x2, y2):
        raise NotImplementedError

    def updatePostion(self, attachedShape, dx, dy):
        if self.startPointObj == attachedShape:
            self.startPointCoords[0] += dx
            self.startPointCoords[1] += dy
          
        elif self.endPointObj == attachedShape:
            self.endPointCoords[0] += dx
            self.endPointCoords[1] += dy
        
        coordShift = (self.startPointCoords[0], 
            self.startPointCoords[1],
            self.endPointCoords[0],
            self.endPointCoords[1])

        LineObject.canvasContainer.coords(self.idInCanvas, *coordShift)

        if self.startPointObj == attachedShape and self.objIdUsedToOverrideHead != None:
            LineObject.canvasContainer.move(self.objIdUsedToOverrideHead, dx, dy)


        

class GeneralizationLine(LineObject):
    def instantiateToCanvas(self,x1, y1, x2, y2):
       
        return LineObject.canvasContainer.create_line(x1, y1, x2, y2, arrow = tkinter.FIRST, width=3, fill='black', arrowshape = (10,10,10))


class CompositiontionLine(LineObject):
    def instantiateToCanvas(self,x1, y1, x2, y2):
        EXTENSION = 10
        RIGHT_SHIFT = 2
        x1 += RIGHT_SHIFT
        coordOfArrowShape = (x1, y1-EXTENSION, x1-EXTENSION, y1, x1, y1+EXTENSION, x1+EXTENSION, y1)
        self.objIdUsedToOverrideHead = LineObject.canvasContainer.create_polygon(*coordOfArrowShape)
        
        return LineObject.canvasContainer.create_line(x1, y1, x2, y2, width=3, fill='black')


class AssociationLine(LineObject):
    def instantiateToCanvas(self,x1, y1, x2, y2):
        
        return LineObject.canvasContainer.create_line(x1, y1, x2, y2, width=3, fill='black')



class CompositionObject():

    def __init__(self, innerObjs, groupId):
        self.canvasContainer = MouseMotionToController.canvasContainer
        self.innerObjs = innerObjs
        self.flattenInnerObjs = self.getFlattenInnerObjs()
        self.layer = self.setLayer()
        self.coordsOfleftUpPoint = None
        self.coordsOfRightDownPoint = None
        self.updateBorder()
        self.groupId = groupId
        self.updateGroupIdForEachObj()

    def showAllObjs(self):
        for obj in self.flattenInnerObjs:
            obj.showPort()

    
    def updateGroupIdForEachObj(self):
        flattenInnerObjs = self.flattenInnerObjs
        for obj in flattenInnerObjs:
            obj.groupIds.append(self.groupId)


    def getFlattenInnerObjs(self):
        flattenInnerObjs = list()
        for compositionObj in self.innerObjs:
            if compositionObj.layer > 0:
                flattenInnerObjs.extend(self.getFlattenInnerObjs(compositionObj.innerObjs))
            else:
                flattenInnerObjs.append(compositionObj)
        return flattenInnerObjs

    
    def setLayer(self):
        return max([innerObj.layer for innerObj in self.innerObjs])+1


    def updateBorder(self):
        coordsXOfInnerObjs = list()
        coordsYOfInnerObjs = list()
        for obj in self.flattenInnerObjs:
            coordOfObj = self.canvasContainer.coords(obj.idInCanvas)
            coordsXOfInnerObjs.extend([coordOfObj[0], coordOfObj[2]])
            coordsYOfInnerObjs.extend([coordOfObj[1], coordOfObj[3]])
        
        self.coordsOfleftUpPoint = [min(coordsXOfInnerObjs), min(coordsYOfInnerObjs)]
        self.coordsOfRightDownPoint = [max(coordsXOfInnerObjs), max(coordsYOfInnerObjs)]

def testOfCompositionObject():
    class mouseEvent():
        def __init__(self, *args, **kwargs):
            self.x = 1
            self.y = 2

if __name__ == "__main__":
    pass