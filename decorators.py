from bridge import MouseMotionToController
from controller.buttonController import ButtonController
from configuration import ConfigOfButton

def printCurrentAndLastActiveObj(funct):
    def wrapper(*args, **kwargs):
        print("_________Before method_________")
        print("ClickedObj",MouseMotionToController.clickedObjectOnCanvas)
        funct(*args, **kwargs)
        print("_________After method_________")
        print("ClickedObj",MouseMotionToController.clickedObjectOnCanvas)
    return wrapper


def callOnlyInSelectMode(func):
    def wrapper(*args):
        if ButtonController.currentActiveButton == ConfigOfButton.nameOfSelect:
            func(*args)

    return wrapper   
           

