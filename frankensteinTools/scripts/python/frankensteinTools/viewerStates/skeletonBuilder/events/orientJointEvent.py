

import hou

from frankensteinTools.nodes                            import SkeletonBuilderNode
from frankensteinTools.drawables                        import DrawableAxis
from frankensteinTools.drawables                        import DrawableSkin
from frankensteinTools.drawables                        import DrawableSkeleton
from frankensteinTools.viewerStates                     import BaseEvent
from frankensteinTools.viewerStates.skeletonBuilder.constants     import SkeletonToolState

class OrientJointEvent(BaseEvent):

    def __init__(self, viewerStates):
        super(OrientJointEvent, self).__init__(viewerStates)

    def mouseEvent(self,
        uiEvent:hou.UIEvent):
        """ Call in onMouseEvent. 
        """
        # Get the ray projection data.
        rayOrigin, rayDirection = uiEvent.ray()
        # Get the device and reason from the ui event.
        device  = uiEvent.device()      # type: hou.UIEventDevice 
        reason  = uiEvent.reason()      # type: hou.uiEventReason

        node                = self.viewerStates.node                # type: SkeletonBuilderNode
        skeletonDrawable    = self.viewerStates.skeletonDrawable    # type: DrawableSkeleton
        axisDrawable        = self.viewerStates.axisDrawable        # type: DrawableAxis
        sceneViewer         = self.viewerStates.sceneViewer         # type: hou.SceneViewer
        skinDrawable        = self.viewerStates.skinCollisionDrawable        # type: DrawableSkin


        if(self.viewerStates.findOrientPrim is True):
            with(hou.undos.disabler()):
                axisDrawable.findAxis(rayOrigin, rayDirection)
                node.vsOrientPrim = axisDrawable.geometry.hitPrimID

        if(reason == hou.uiEventReason.Start):
            if(device.isLeftButton() is True):
                self.viewerStates.findOrientPrim = False
                sceneViewer.beginStateUndo("skeleton_orientJoint")
                node.vsOrientPrim           = -1
                node.vsOrientTargetPrim     = -1
                node.vsJointID              = -1
                node.vsOrientAxis           = -1
                node.vsOrientJointID        = -1
                node.vsJointHighlight       = -1
                node.vsSkinPointHighlight   = -1
                node.vsOrientTargetJointID  = -1
                node.vsOrientTargetAxis     = -1
                node.vsToolState    = SkeletonToolState.Enable
                node.vsOrientPrim   = axisDrawable.geometry.hitPrimID
                if(axisDrawable.geometry.hitPrimID > -1):
                    axisPrim                = axisDrawable.geometry.prim(axisDrawable.geometry.hitPrimID) # type: hou.Prim
                    node.vsJointID          = axisPrim.attribValue("jointID")
                    node.vsOrientAxis       = axisPrim.attribValue("axis")
                    #node.vsJointHighlight   = node.vsJointID

        if(reason == hou.uiEventReason.Changed):
            node.cache()
            node.vsToolState            = SkeletonToolState.Disable 
            node.vsOrientPrim           = -1
            node.vsOrientTargetPrim     = -1
            node.vsJointID              = -1
            node.vsOrientAxis           = -1
            node.vsOrientJointID        = -1
            node.vsJointHighlight       = -1
            node.vsSkinPointHighlight   = -1
            node.vsOrientTargetJointID  = -1
            node.vsOrientTargetAxis     = -1
            self.viewerStates.findOrientPrim    = True
            sceneViewer.endStateUndo()

        if(reason == hou.uiEventReason.Active):
            with(hou.undos.disabler()):
                if(node.vsJointID > -1):
                    if(device.isLeftButton() is True):
                        node.vsRayOrigin    = rayOrigin
                        node.vsRayDirection = rayDirection              

                        snapToJoint         = node.orientSnapToJoint
                        snapToAxis          = node.orientSnapToJointAxis
                        snapToGeo           = node.orientSnapToSkinPoint

                        # Define the axis align behavior when the snap option are allowed.
                        # We start to check if we collide with joint, then with joint axis and last
                        # with geometry skin.
                        if(snapToJoint == 1):
                            skeletonDrawable.geometryCollision.surfacePointIntersect(rayOrigin, rayDirection)
                            if(skeletonDrawable.geometryCollision.hitPointID == -1):
                                skeletonDrawable.geometryCollision.pointIntersect(rayOrigin, rayDirection, 0.008)

                            node.vsOrientJointID    = skeletonDrawable.geometryCollision.hitPointID
                            
                            # Disable and reset snap to Axis and Geo.
                            if(skeletonDrawable.geometryCollision.hitPointID > -1):
                                node.vsOrientTargetPrim         = -1
                                node.vsSkinPointHighlight       = -1
                                node.vsOrientTargetJointID      = -1
                                node.vsOrientTargetAxis         = -1
                                snapToAxis                      = 0
                                snapToGeo                       = 0

                        if(snapToAxis == 1):
                            axisDrawable.geometry.surfacePointIntersect(rayOrigin, rayDirection)
                            node.vsOrientTargetPrim = axisDrawable.geometry.hitPrimID

                            # Disable and reset snap to Geo.
                            if(axisDrawable.geometry.hitPrimID > -1):
                                prim = axisDrawable.geometry.prim(axisDrawable.geometry.hitPrimID)
                                node.vsOrientTargetJointID      = prim.attribValue("jointID")
                                node.vsOrientTargetAxis         = prim.attribValue("axis")
                                node.vsOrientJointID            = -1
                                node.vsSkinPointHighlight       = -1
                                snapToGeo                       = 0

                        if(snapToGeo == 1):
                            node.vsSkinPointHighlight = skinDrawable.findPoint(rayOrigin, rayDirection)

                            # reset snap to Geo.
                            if(node.vsSkinPointHighlight > -1):
                                prim = axisDrawable.geometry.prim(axisDrawable.geometry.hitPrimID)
                                node.vsOrientTargetJointID      = -1
                                node.vsOrientTargetAxis         = -1
                                node.vsOrientJointID            = -1

        return False