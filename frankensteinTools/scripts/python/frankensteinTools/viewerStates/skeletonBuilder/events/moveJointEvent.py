
import hou

from frankensteinTools.nodes                            import SkeletonBuilderNode
from frankensteinTools.drawables                        import DrawableSkeleton
from frankensteinTools.drawables                        import DrawableSkin
from frankensteinTools.viewerStates                     import BaseEvent
from frankensteinTools.viewerStates.skeletonBuilder.constants     import SkeletonToolState

class MoveJointEvent(BaseEvent):

    def __init__(self, viewerStates):
        super(MoveJointEvent, self).__init__(viewerStates)

    def mouseEvent(self,
        uiEvent:hou.ViewerEvent):
        """ Call in onMouseEvent. 
        """
        # Get the ray projection data.
        rayOrigin, rayDirection = uiEvent.ray()
        # Get the device and reason from the ui event.
        device  = uiEvent.device()      # type: hou.UIEventDevice 
        reason  = uiEvent.reason()      # type: hou.uiEventReason

        node                = self.viewerStates.node                    # type: SkeletonBuilderNode
        skeletonDrawable    = self.viewerStates.skeletonDrawable        # type: DrawableSkeleton
        skinDrawable        = self.viewerStates.skinCollisionDrawable   # type: DrawableSkin
        sceneViewer         = self.viewerStates.sceneViewer             # type: hou.SceneViewer

        with(hou.undos.disabler()):
            if(self.viewerStates.findJoint is True):
                jointID = skeletonDrawable.findJoint(rayOrigin, rayDirection, 0.005)
                node.vsJointHighlight = jointID

        if(reason == hou.uiEventReason.Start):
            sceneViewer.beginStateUndo("skeletonBuilder_moveJoint")
            if(device.isLeftButton()):
                self.viewerStates.findJoint = False
                node.vsRayOrigin            = rayOrigin
                node.vsRayDirection         = rayDirection
                node.vsToolState            = SkeletonToolState.Enable
                node.vsJointID              = skeletonDrawable.geometryCollision.hitPointID
                skeletonDrawable._jointID   = skeletonDrawable.geometryCollision.hitPointID
                self.viewerStates.findJoint = False

        if(reason == hou.uiEventReason.Changed):
            node.cache()
            node.vsToolState            = SkeletonToolState.Disable
            node.vsSkinPointID          = -1
            node.vsSkinPrimID           = -1
            node.vsSkinPrimUVW          = hou.Vector3()
            self.viewerStates.findJoint = True
            sceneViewer.endStateUndo()

        if(reason == hou.uiEventReason.Active):
            with(hou.undos.disabler()):
                if(device.isLeftButton()):
                    node.vsRayOrigin    = rayOrigin
                    node.vsRayDirection = rayDirection
                    skeletonDrawable.jointHighlight()
                    if(node.projectionSnapPoint == 1 or node.projectionRayType == 1):
                        skinDrawable.findPoint(rayOrigin, rayDirection)
                        node.vsSkinPointID = skinDrawable.geometry.hitPointID
                        node.vsSkinPrimID = skinDrawable.geometry.hitPrimID
                        node.vsSkinPrimUVW = skinDrawable.geometry.hitPrimUV



        return False
    