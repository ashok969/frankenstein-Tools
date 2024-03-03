
import hou


from frankensteinTools.nodes                            import SkeletonBuilderNode
from frankensteinTools.drawables                        import DrawableSkeleton
from frankensteinTools.viewerStates                     import BaseEvent
from frankensteinTools.viewerStates.skeletonBuilder.constants     import SkeletonToolState

class InsertJointEvent(BaseEvent):

    def __init__(self, viewerStates):
        super(InsertJointEvent, self).__init__(viewerStates)

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

        if(self.viewerStates.findJoint == True):
            skeletonDrawable.geometryCollision.linePointIntersect(rayOrigin, rayDirection)

        if(node.vsLive == 1):
            with(hou.undos.disabler()):
                node.vsJointPrimID    = skeletonDrawable.geometryCollision.hitPrimID
                node.vsJointPrimUVW   = skeletonDrawable.geometryCollision.hitPrimUV 

        if(reason == hou.uiEventReason.Picked):
            sceneViewer.beginStateUndo("skeletonBuilder_insertJoint")

            node.vsToolState      = SkeletonToolState.Enable
            node.vsJointPrimID    = skeletonDrawable.geometryCollision.hitPrimID
            node.vsJointPrimUVW   = skeletonDrawable.geometryCollision.hitPrimUV 
            node.cache()
            node.vsToolState  = SkeletonToolState.Disable
            node.vsJointPrimID   = -1

            sceneViewer.endStateUndo()


        if(reason == hou.uiEventReason.Start):
            sceneViewer.beginStateUndo("skeletonBuilder_insertJoint")
            self.viewerStates.findJoint = False
            node.vsToolState      = SkeletonToolState.Enable
            node.vsJointPrimID    = skeletonDrawable.geometryCollision.hitPrimID
            node.vsJointPrimUVW   = skeletonDrawable.geometryCollision.hitPrimUV 

        if(reason == hou.uiEventReason.Changed):
            node.cache()
            node.vsToolState  = SkeletonToolState.Disable
            self.viewerStates.findJoint = True
            node.vsJointPrimID   = -1
            sceneViewer.endStateUndo()

        if(reason == hou.uiEventReason.Active):
            if(device.isLeftButton()):
                with(hou.undos.disabler()):
                    skeletonDrawable.geometryCollision.linePointIntersect(rayOrigin, rayDirection)
                    if(skeletonDrawable.geometryCollision.hitPrimID == node.vsJointPrimID):
                        node.vsJointPrimUVW   = skeletonDrawable.geometryCollision.hitPrimUV

        return False
    