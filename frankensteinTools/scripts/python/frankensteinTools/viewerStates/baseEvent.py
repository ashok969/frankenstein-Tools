
import hou

class BaseEvent(object):

    def __init__(self, viewerStates):

        self.viewerStates = viewerStates

    def mouseEvent(self,
        uiEvent:hou.ViewerEvent):
        """ Call in onMouseEvent. 
        """
        return False

    def keyEvent(self,
        uiEvent:hou.ViewerEvent):
        """ Call in onKeyEvent. 
        """
        return False

    def mouseDoubleClickEvent(self,
        uiEvent:hou.ViewerEvent):
        """ Call in onMouseEvent. 
        """
        return False

    