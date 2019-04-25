class MouseMotionToController():
    
    clickedObjectOnCanvas = list()
    selectedObjectOnCanvas = list()
    
    
    # @classmethod
    # def verifySelectedObj(cls):
    #     if MouseMotionToController.modeOfClickedObjectOnCaanvas == 3:


    @classmethod
    def flushclickedObjectOnCanvas(cls):
        cls.clickedObjectOnCanvas = []
    
    @classmethod
    def modeOfClickedObjectOnCaanvas(cls):
        clickedObj = cls.clickedObjectOnCanvas

        if not clickedObj:
            #  no action
            return 0

        elif len(clickedObj) == 1:
            if not clickedObj[-1]:
                # [False] := last click isn't on object
                return 1
 
        elif len(clickedObj) >= 2:
            if clickedObj[-2] == False and clickedObj[-1] == False:
                # [...False, False] := last click isn't on object
                return 2
            elif clickedObj[-2] != False and clickedObj[-1] == False:
                # [...Obj, False] := last click is on object
                return 3

class ButtonToMode():
    
    currentAvailableModes = list()