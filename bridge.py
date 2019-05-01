class MouseMotionToController():
    
    CLICK_ON_OBJECT = "CLICK_ON_OBJECT"
    CLICK_ON_CANVAS = "CLICK_ON_CANVAS"
    canvasContainer = None
    mouseReleasedObjId = list()
    multiSelectedObjs = list()
    singleClickedObj = list()
    
    @classmethod
    def displayAllReleasedObjs(cls):
        print("displayAllReleasedObjs_START")
        for id in cls.mouseReleasedObjId:
            if id != False:
                print("id:{}, obj:{}".format(id, cls.getObjById(id)))
        print("displayAllReleasedObjs_END")
    
    @classmethod
    def displayAllClickedObjs(cls):
        print("displayAllClickedObjs_START")

        for id in cls.singleClickedObj:
            print("id:{}, obj:{}".format(id, cls.getObjById(id)))
        print("displayAllClickedObjs_END")

    @classmethod
    def getObjById(cls, ids, objects = False):

        if not objects:
            objects = MouseMotionToController.singleClickedObj
            
        if type(ids) == list:
            objs = list()
            for obj in objects:
                for id in ids:
                    if obj.idInCanvas == id:
                        objs.append(obj)
            return objs
        else:
            # print("release Objs",objects)
            for obj in objects:
                if obj != False:
                    # print("id",ids[0], obj.idInCanvas)
                    if obj.idInCanvas == ids[0]:
                        # print("obj",obj)
                        return obj

    @classmethod
    def getCurrentClickedObj(cls):
        if len(cls.singleClickedObj) < 2:
            print("No clicked Object!")
        else:
            return MouseMotionToController.singleClickedObj[-2]
  
    @classmethod
    def getCurrentReleasedObj(cls, searchObjs = False):
        if len(cls.mouseReleasedObjId) < 1:
            print("No released Object!")
        else:
            if not searchObjs:
                return cls.getObjById(MouseMotionToController.mouseReleasedObjId[-1])
            else:
                return cls.getObjById(MouseMotionToController.mouseReleasedObjId[-1], searchObjs)
                

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
                return cls.CLICK_ON_CANVAS

            # directly click on Objects
            elif clickedObj[-2] != False and clickedObj[-1] == False:
                # [...Obj, False] := last click is on object
                return cls.CLICK_ON_OBJECT

class ButtonToMode():
    currentAvailableModes = list()

class PopTextToClassName():
    keyInText = None