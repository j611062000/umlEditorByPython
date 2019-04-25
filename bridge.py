class MouseMotionToController():
    
    # These two variables are instances of TwoDimensionShape
    currentActiveObjectOnCanvas = None
    lastActiveObjectOnCanvas = None

    # isClickOnCanvas = None
    # isClickOnClass = None
    # isClickonUseCase = None

    @classmethod
    def updatecurrentActiveObjectOnCanvas(cls, objOfShape):
        cls.currentActiveObjectOnCanvas = objOfShape
    
    @classmethod
    def flushcurrentActiveObjectOnCanvas(cls):
        cls.currentActiveObjectOnCanvas = None

    @classmethod
    def updateLastActiveObjectOnCanvas(cls, objOfShape):
        cls.lastActiveObjectOnCanvas = objOfShape
    
    @classmethod
    def flushLastActiveObjectOnCanvas(cls):
        cls.lastActiveObjectOnCanvas = None
        