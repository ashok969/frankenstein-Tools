
import hou

from frankensteinTools.nodes                            import SkeletonBuilderNode
from frankensteinTools.drawables                        import DrawableSkeleton
from frankensteinTools.viewerStates                     import BaseEvent
from frankensteinTools.viewerStates.skeletonBuilder.constants     import SkeletonToolState

class RemoveJointEvent(BaseEvent):

    def __init__(self, viewerStates):
        super(RemoveJointEvent, self).__init__(viewerStates)

    def mouseEvent(self,
        uiEvent:hou.ViewerEvent):
        """ Call in onMouseEvent. 
        """
        # Get the ray projection data.
        rayOrigin, rayDirection = uiEvent.ray()
        # Get the device and reason from the ui event.
        device  = uiEvent.device()      # type: hou.UIEventDevice 
        reason  = uiEvent.reason()      # type: hou.uiEventReason 

        node                = self.viewerStates.node                # type: SkeletonBuilderNode
        skeletonDrawable    = self.viewerStates.skeletonDrawable    # type: DrawableSkeleton
        sceneViewer         = self.viewerStates.sceneViewer         # type: hou.SceneViewer

        with(hou.undos.disabler()):
            jointID = skeletonDrawable.findJoint(rayOrigin, rayDirection, 0.005)
            node.vsJointHighlight = jointID

        if(reason == hou.uiEventReason.Start):
            sceneViewer.beginStateUndo("skeletonBuilder_removeJoint")
            if(device.isLeftButton() is True):
                node.vsToolState  = 1
                node.vsJointID = skeletonDrawable.geometryCollision.hitPointID

        if(reason == hou.uiEventReason.Changed):
            node.cache()
            node.vsToolState  = 0
            node.vsJointID = -1
            node.vsJointHighlight = -1
            sceneViewer.endStateUndo()
        
        if(reason == hou.uiEventReason.Active):
            with(hou.undos.disabler()):
                if(device.isLeftButton() is True):
                    node.vsJointHighlight = -1

        if(reason == hou.uiEventReason.Picked):
            sceneViewer.beginStateUndo("skeletonBuilder_removeJoint")
            if(device.isLeftButton() is True):
                node.vsJointHighlight   = -1
                node.vsJointID          = skeletonDrawable.geometryCollision.hitPointID
                node.vsToolState        = 1
                node.cache()
                node.vsToolState        = 0
                node.vsJointID          = -1
            sceneViewer.endStateUndo()
    
        return False