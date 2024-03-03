

import hou

from frankensteinTools.nodes                            import SkeletonBuilderNode
from frankensteinTools.drawables                        import DrawableSkeleton
from frankensteinTools.viewerStates                     import BaseEvent
from frankensteinTools.viewerStates.skeletonBuilder.constants     import SkeletonToolState

class ParentJointEvent(BaseEvent):

    def __init__(self, viewerStates):
        super(ParentJointEvent, self).__init__(viewerStates)

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
            sceneViewer.beginStateUndo("skeletonBuilder_parentJoint")
            node.vsToolState        = 1
            node.vsJointParentID    = skeletonDrawable.geometryCollision.hitPointID

        if(reason == hou.uiEventReason.Changed):
            node.vsJointID          = skeletonDrawable.geometryCollision.hitPointID
            node.cache()
            node.vsToolState        = 0
            node.vsJointParentID    = -1
            node.vsJointID          = -1
            sceneViewer.endStateUndo()

        if(reason == hou.uiEventReason.Active):
            with(hou.undos.disabler()):
                node.vsJointID          = skeletonDrawable.geometryCollision.hitPointID

        return False