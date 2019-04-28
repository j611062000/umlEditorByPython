from bridge import MouseMotionToController
from controller.buttonController import ButtonController
from configuration import ConfigOfButton

def overrides(func):
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
    
    return wrapper

def trackMouseClickedObjs(funct):
    def wrapper(*args, **kwargs):
        print("_________Before method_________")
        print("ClickedObj:",MouseMotionToController.singleClickedObj)
        print("SelectedObj:",MouseMotionToController.multiSelectedObjs)
        funct(*args, **kwargs)
        print("_________After method_________")
        print("ClickedObj:",MouseMotionToController.singleClickedObj)
        print("SelectedObj:",MouseMotionToController.multiSelectedObjs)
    return wrapper


def callOnlyInSelectMode(func):
    def wrapper(*args):
        if ButtonController.currentActiveButton == ConfigOfButton.nameOfSelect:
            func(*args)

    return wrapper   
           

