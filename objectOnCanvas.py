import tkinter
from bridge import MouseMotionToController
from controller.buttonController import ButtonController
from decorators import printCurrentAndLastActiveObj, callOnlyInSelectMode

# Bugs: port can't not work occassionally


class TwoDimensionShape():

    canvasContainer = None
    fillColorOfShape = "grey"
    fillColorOfPort = "black"

    def __init__(self, canvasContainer, createMethod, shiftX, shiftY, mouseEvent):
        TwoDimensionShape.canvasContainer = canvasContainer
        self.coordinateOfPort = list()
        self.idOfPortInCanvas = list()
        self.idInCanvas = TwoDimensionShape.instantiateToCanvas(createMethod, shiftX, shiftY, mouseEvent)
        self.bindToCanvasWithMouseEvent(self.idInCanvas)
        self.updateCoordinateOfPort(mouseEvent, shiftX, shiftY)
        
    def handleMouseClickEvent(self, event):
        MouseMotionToController.clickedObjectOnCanvas.append(self)
        TwoDimensionShape.canvasContainer.tag_raise(self.idInCanvas)
        self.raisePortToFront()
        self.showPort()

    def handleMouseReleaseEvent(self, event):
        pass
        # self.hidePort(MouseMotionToController.lastActiveObjectOnCanvas)

    def bindToCanvasWithMouseEvent(self, bindingShape):
        pressHandler = self.handleMouseClickEvent
        TwoDimensionShape.canvasContainer.tag_bind(bindingShape, '<Button-1>', pressHandler)

        releaseHandler = self.handleMouseReleaseEvent
        TwoDimensionShape.canvasContainer.tag_bind(bindingShape, '<ButtonRelease-1>', releaseHandler)
    
    def instantiatePorts(self, coordinateOfPort, normOfPort):
        methodOfCreation = TwoDimensionShape.canvasContainer.create_oval
        for port in coordinateOfPort:
            self.idOfPortInCanvas.append(TwoDimensionShape.instantiateToCanvas(methodOfCreation, normOfPort, normOfPort, port))


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


    def raisePortToFront(self):
        for port in self.idOfPortInCanvas:
            TwoDimensionShape.canvasContainer.tag_raise(port)


    def movePortWhenShapIsDragged(self, dx, dy):
        for idOfPort in self.idOfPortInCanvas:
            TwoDimensionShape.canvasContainer.move(idOfPort, dx, dy)


    @classmethod
    def instantiateToCanvas(cls, methodOfCreation, shiftX, shiftY, mouseEvent):
        try:
            # shape
            return methodOfCreation(mouseEvent.x, mouseEvent.y,mouseEvent.x+shiftX,mouseEvent.y+shiftY, fill = TwoDimensionShape.fillColorOfShape)
        except:
            # port
            return methodOfCreation(mouseEvent[0], mouseEvent[1],mouseEvent[0]+shiftX,mouseEvent[1]+shiftY, fill = TwoDimensionShape.fillColorOfPort, state = tkinter.HIDDEN)

        





class ClassObject(TwoDimensionShape):

    def __init__(self, mouseEvent, canvasContainer):
        super().__init__(canvasContainer, canvasContainer.create_rectangle, 100, 140, mouseEvent)
    

class UseCaseObject(TwoDimensionShape):
    
    def __init__(self, mouseEvent, canvasContainer):
        super().__init__(canvasContainer, canvasContainer.create_oval, 140, 100, mouseEvent)



    