class MouseMotionToController():
    
    singleClickedObj = list()
    idOfMouseReleaseObject = list()
    multiSelectedObjs = list()
    CLICK_ON_OBJECT = "CLICK_ON_OBJECT"
    CLICK_ON_CANVAS = "CLICK_ON_CANVAS"
   

    @classmethod
    def flushsingleClickedObj(cls):
        cls.singleClickedObj = []
    
    @classmethod
    def flushmultiSelectedObjs(cls):
        cls.multiSelectedObjs = []
    
    @classmethod
    def flushMouseReleaseOnObjectOfCanvas(cls):
        cls.mouseReleaseOnObjectOfCanvas = []
    
    @classmethod
    def whatIsClickedByMouse(cls):
        clickedObj = cls.singleClickedObj

        if not clickedObj:
            #  no action
            return 0

        elif len(clickedObj) == 1:
            if not clickedObj[-1]:
                # [False] := last click isn't on object
                return 1

        elif len(clickedObj) >= 2:
            # directly click on Canvas
            if clickedObj[-2] == False and clickedObj[-1] == False:
                # [...False, False] := last click isn't on object
                return 2

            # directly click on Objects
            elif clickedObj[-2] != False and clickedObj[-1] == False:
                # [...Obj, False] := last click is on object
                return cls.CLICK_ON_OBJECT

class ButtonToMode():
    currentAvailableModes = list()

class PopTextToClassName():
    keyInText = None