
import hou

from frankensteinTools.nodes                            import SkeletonBuilderNode
from frankensteinTools.drawables                        import DrawableSkeleton
from frankensteinTools.drawables                        import DrawableSkin
from frankensteinTools.viewerStates                     import BaseEvent
from frankensteinTools.viewerStates.skeletonBuilder.constants     import SkeletonToolState

class AddJointEvent(BaseEvent):

    def __init__(self, viewerStates):
        super(AddJointEvent, self).__init__(viewerStates)

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
        skinDrawable        = self.viewerStates.skinCollisionDrawable   # type: DrawableSkin


        with(hou.undos.disabler()):
            jointID = skeletonDrawable.findJoint(rayOrigin, rayDirection, 0.005)
            node.vsJointHighlight = jointID

        if(reason == hou.uiEventReason.Start):
            sceneViewer.beginStateUndo("skeletonBuilder_addJoint")
            if(device.isLeftButton() is True):
                node.vsRayOrigin      = rayOrigin
                node.vsRayDirection   = rayDirection

                self.viewerStates.findJoint = False
                if(node.vsJointParentID == -1):
                    node.vsJointParentID = skeletonDrawable.geometryCollision.hitPointID
                if(skeletonDrawable.geometryCollision.hitPointID != -1 and
                skeletonDrawable.geometryCollision.hitPointID != node.vsJointParentID):
                    node.vsJointParentID = skeletonDrawable.geometryCollision.hitPointID

                node.vsToolState = SkeletonToolState.Enable
                return False

        if(reason == hou.uiEventReason.Active):
            with(hou.undos.disabler()):
                if(device.isLeftButton() is True):
                    node.vsRayOrigin      = rayOrigin
                    node.vsRayDirection   = rayDirection
                    if(node.projectionSnapPoint == 1 or node.projectionRayType == 1):
                        skinDrawable.findPoint(rayOrigin, rayDirection)
                        node.vsSkinPointID = skinDrawable.geometry.hitPointID
                        node.vsSkinPrimID = skinDrawable.geometry.hitPrimID
                        node.vsSkinPrimUVW = skinDrawable.geometry.hitPrimUV
                    return False

        if(reason == hou.uiEventReason.Picked):
            sceneViewer.beginStateUndo("skeleton_addJoint")
            if(device.isMiddleButton() is True):
                node.vsJointParentID = -1
                sceneViewer.endStateUndo()
                return False
            sceneViewer.endStateUndo()

        if(reason == hou.uiEventReason.Changed):
            node.cache()
            node.vsToolState = SkeletonToolState.Disable
            node.vsJointParentID = len(node.toCache.geometry().points()) - 1
            self.viewerStates.findJoint = True
            sceneViewer.endStateUndo()
            return False

        return False


    def keyEvent(self,
        uiEvent:hou.ViewerEvent):
        """ Call in onKeyEvent.
        """
        device  = uiEvent.device()          # type: hou.UIEventDevice
        reason  = uiEvent.reason()          # type: hou.uiEventReason

        node            = self.viewerStates.node    # type: SkeletonBuilderNode
        sceneViewer     = self.viewerStates.sceneViewer         # type: hou.SceneViewer

        if(device.keyString() == "b"):
            sceneViewer.beginStateUndo("skeleon_Addjoint_BKey")
            node.vsJointParentID = -1
            sceneViewer.endStateUndo()
            return True
    
        return False
