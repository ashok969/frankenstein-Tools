
import hou

class BaseStates(object):

    def __init__(self, 
        stateName:str, 
        sceneViewer:hou.SceneViewer,
        undoName:str):

        self.stateName      = stateName
        self.sceneViewer    = sceneViewer
        self.undoName       = undoName

        self.mouseScreenPosStart        = hou.Vector2()
        self.mouseScreenPosCurrent      = hou.Vector2()
        self.mouseScreenPosEnd          = hou.Vector2()
        self.mouseScreenDisplaceVector  = hou.Vector2()
        self.mouseScreenDisplace        = 0.0

        self._inAction          = False

    def startUndo(self):
        """ Initialize the start of undo block when inAction is True.
        """
        self.sceneViewer.beginStateUndo(self.undoName)
        
    def endUndo(self):
        """ End the undo block when the inAction is False.
        """
        self.sceneViewer.endStateUndo()

