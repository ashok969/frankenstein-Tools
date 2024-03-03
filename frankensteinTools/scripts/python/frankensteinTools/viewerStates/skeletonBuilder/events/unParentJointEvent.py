
import hou

from frankensteinTools.nodes                            import SkeletonBuilderNode
from frankensteinTools.drawables                        import DrawableSkeleton
from frankensteinTools.viewerStates                     import BaseEvent
from frankensteinTools.viewerStates.skeletonBuilder.constants     import SkeletonToolState

class UnParentJointEvent(BaseEvent):

    def __init__(self, viewerStates):
        super(UnParentJointEvent, self).__init__(viewerStates)

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
            node.vsJointPrimHighlight = skeletonDrawable.geometryCollision.hitPrimID

        if(reason == hou.uiEventReason.Start):
            sceneViewer.beginStateUndo("skeletonBuilder_unParentJoint")
            node.vsToolState = SkeletonToolState.Enable

        if(reason == hou.uiEventReason.Changed):
            node.cache()
            node.vsToolState  = SkeletonToolState.Disable
            sceneViewer.endStateUndo()

        if(reason == hou.uiEventReason.Picked):
            sceneViewer.beginStateUndo("skeletonBuilder_unParentJoint")
            node.vsToolState  = SkeletonToolState.Enable
            node.vsJointPrimID = skeletonDrawable.geometryCollision.hitPrimID
            node.cache()
            node.vsToolState  = SkeletonToolState.Disable
            sceneViewer.endStateUndo()

        if(reason == hou.uiEventReason.Active):
            with(hou.undos.disabler()):
                node.vsJointPrimID = skeletonDrawable.geometryCollision.hitPrimID

        return False