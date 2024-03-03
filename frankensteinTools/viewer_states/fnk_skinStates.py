
import hou
import viewerstate.utils as vs

from    stateutils      import ancestorObject
from    stateutils      import sopGeometryIntersection
from    stateutils      import cplaneIntersection

from    frankensteinTools.drawables        import FNKBrushDrawable
from    frankensteinTools.drawables        import DrawableSkeleton



HUD_TEMPLATE = {
    "title" : "Frankenstein Skin",
    "desc"  : "tool",
    "icon"  : "SOP_capturelayerpaint",
    "rows"  : [
        {"id" : "brushRadius", "label" : "Brush Radius", "key" : "Ctrl LMB"},
        {"id" : "brushRadius_g", "type" : "bargraph"},
        {"id" : "brushInnderRadius", "label" : "Brush Inner Radius", "key" : "Shift LMB"},
        {"id" : "brushInnderRadius_g", "type" : "bargraph"},
        {"id" : "selectJoint", "label" : "Select Joint", "key" : "1"}
    ]
}




class FKNSkinState(object):

    def __init__(self, state_name, scene_viewer):

        self.state_name         = state_name
        self.scene_viewer       = scene_viewer
        
        self.brush              = FNKBrushDrawable(state_name, scene_viewer)
        self.brush.hide()

        self._rigDrawable       = DrawableSkeleton(state_name, scene_viewer)

        self.scene_viewer.hudInfo(template=HUD_TEMPLATE)


        self.mouseScreenPosStart        = hou.Vector2()
        self.mouseScreenPosCurrent      = hou.Vector2()
        self.mouseScreenPosEnd          = hou.Vector2()
        self.mouseScreenDisplaceVector  = hou.Vector2()
        self.mouseScreenDisplace        = 0.0

        self.rayPrimIDCurrent   = -1
        self.rayPosCurrent      = hou.Vector3()
        self.rayNormalCurrent   = hou.Vector3()
        self.rayPrimUVCurrent   = hou.Vector3()

        self.rayPrimIDStart     = -1
        self.rayPosStart        = hou.Vector3()
        self.rayNormalStart     = hou.Vector3()
        self.rayPrimUVStart     = hou.Vector3()

        self.innerSizeParm      = 0.0
        self.outerSizeParm      = 0.0

        self._pressed           = False


    def _startUndo(self):

        if(not self._pressed):
            self.scene_viewer.beginStateUndo("Paint")
        
        self._pressed = True

    def _endUndo(self):

        if(self._pressed):
            self.scene_viewer.endStateUndo()
        
        self._pressed = False

    def onEnter(self, kwargs):

        self.node = kwargs["node"]

        inputs = self.node.inputs()

        if(len(inputs) > 1):
            self._rigDrawable.rigGeometry = self.node.node("RIG").geometry()
            self._rigDrawable.showRig

        # Get the brush size values.
        self.brush.innerSize    = self.node.parm("brushInnerSize").eval()
        self.brush.outerSize    = self.node.parm("brushOuterSize").eval()
        self.innerSizeParm      = self.brush.innerSize
        self.outerSizeParm      = self.brush.outerSize

        self.scene_viewer.hudInfo(show=1)


    def onDraw(self, kwargs):

        self._rigDrawable.setDraw(kwargs["draw_handle"])
        self.brush.onDraw(kwargs)


    def onDrawInterrupt(self, kwargs):

        self._rigDrawable.setDraw(kwargs["draw_handle"])
        self.brush.onDrawInterrupt(kwargs)

    def onMouseEvent(self, kwargs):

        state = self.node.parm("state").eval()

        if(state == 0):

            # Get the node sync with the state.
            node = kwargs["node"]

            ui_event    = kwargs["ui_event"]
            dev         = ui_event.device()
            reason      = ui_event.reason()

            ray_origin, ray_dir = ui_event.ray()

            self.rayPrimIDCurrent = -1
            if(node.inputs() and node.inputs()[0]):
                geometry = node.node("SKIN_INTERSECT").geometry()
                self.rayPrimIDCurrent, self.rayPosCurrent, self.rayNormalCurrent, self.rayPrimUVCurrent = sopGeometryIntersection(geometry, ray_origin, ray_dir)


            if(reason == hou.uiEventReason.Start):
                self.mouseScreenPosStart[0] = dev.mouseX()
                self.mouseScreenPosStart[1] = dev.mouseY()
                self.rayPrimIDStart         = self.rayPrimIDCurrent
                self.rayPosStart            = self.rayPosCurrent
                self.rayNormalStart         = self.rayNormalCurrent
                self.rayPrimUVStart         = self.rayPrimUVCurrent
                self._startUndo()

            if(dev.isLeftButton()):
                # Define the brush size behavior.
                if(dev.isCtrlKey() or dev.isShiftKey()):

                    self.rayPrimIDCurrent         = self.rayPrimIDStart
                    self.rayPosCurrent            = self.rayPosStart
                    self.rayNormalCurrent         = self.rayNormalStart
                    self.rayPrimUVCurrent         = self.rayPrimUVStart

                    if(reason == hou.uiEventReason.Active): # Mouse dragged with Down.
                        self.mouseScreenPosCurrent[0]   = dev.mouseX()
                        self.mouseScreenPosCurrent[1]   = dev.mouseY()
                        self.mouseScreenDisplaceVector  = self.mouseScreenPosCurrent - self.mouseScreenPosStart
                        self.mouseScreenDisplace        = self.mouseScreenDisplaceVector.length()

                        offset = 0.0

                        if(self.mouseScreenPosStart.x() <= self.mouseScreenPosCurrent.x()):
                            offset = self.mouseScreenDisplace * 0.001
                        else:
                            offset = -self.mouseScreenDisplace * 0.001

                        if(dev.isShiftKey()):
                            self.brush.innerSize = self.innerSizeParm + offset
                            if(self.brush.innerSize < 0.0):
                                self.brush.innerSize = 0.0
                            if(self.brush.innerSize > self.brush.outerSize):
                                self.brush.outerSize = self.brush.innerSize
                        elif(dev.isCtrlKey()):
                            innerSizeRatio = 0.0
                            if(self.outerSizeParm > 0.0):
                                innerSizeRatio = self.innerSizeParm / self.outerSizeParm
                            self.brush.outerSize = self.outerSizeParm + offset
                            if(self.brush.outerSize < 0.0):
                                self.brush.outerSize = 0.0
                            self.brush.innerSize = self.brush.outerSize * innerSizeRatio

                        


            if(reason == hou.uiEventReason.Changed) : # Mouse Relased.
                self.innerSizeParm = self.brush.innerSize
                self.outerSizeParm = self.brush.outerSize
                self.node.parm("brushInnerSize").set(self.brush.innerSize)
                self.node.parm("brushOuterSize").set(self.brush.outerSize)
                self._endUndo()



            # Define the brush behavior.
            if(dev.isLeftButton()):
                
                # Update the brush inner size.
                if(dev.isCtrlKey() or dev.isShiftKey()):
                    pass

                else:

                    with hou.undos.disabler():
                        node.parm("brushPositionx").set(self.rayPosCurrent.x())
                        node.parm("brushPositiony").set(self.rayPosCurrent.y())
                        node.parm("brushPositionz").set(self.rayPosCurrent.z())
                        node.parm("brushLeftClick").set(True)

                    node.parm("skinCache").set(node.node("SKIN_TO_CACHE").geometry())
            
            else:
                
                with hou.undos.disabler():
                    node.parm("brushPositionx").set(0.0)
                    node.parm("brushPositiony").set(0.0)
                    node.parm("brushPositionz").set(0.0)
                    node.parm("brushLeftClick").set(False)

            if(self.rayPrimIDCurrent > -1):
                self.brush.transformFromRayDatas(self.rayPosCurrent, self.rayNormalCurrent)
                self.brush.show()
            else:
                self.brush.hide()

            return False

        elif(state == 1):
            return False


    def onInterrupt(self, kwargs):

        self.brush.hide()
        self.node.parm("brushInnerSize").set(self.brush.innerSize)
        self.node.parm("brushOuterSize").set(self.brush.outerSize)

        #self.rigDrawable.show(False)

    def onStartSelection(self, kwargs):

        self.brush.hide()
        self.node.parm("state").set(1)
        print("Start Selection")
        

    def onSelection(self, kwargs):

        jointID = self._rigDrawable.setSelection(kwargs)
        print(jointID)
        self.node.parm("state").set(0)
        self.node.parm("jointID").set(jointID)


    def onLocatedSelection(self, kwargs):
        self.brush.hide()
        self.node.parm("state").set(1)
        self._rigDrawable.setLocatedSelection(kwargs)


    def onStopSelection(self, kwargs):

        self.node.parm("state").set(0)
        self._rigDrawable.setStopSelection(kwargs)
        print("Stop Selection")
        self.brush.show()



def createViewerStateTemplate():

    state_typename      = "fnk__SkinTools"
    state_label         = "Frankenstein Skin Tools"
    state_cat           = hou.sopNodeTypeCategory()
    
    template            = hou.ViewerStateTemplate(state_typename, state_label, state_cat)
    template.bindFactory(FKNSkinState)
    template.bindIcon("SOP_capturelayerpaint")

    hk1 = vs.hotkey(state_typename, "Select Joint", "1")

    template.bindDrawableSelector(
        "Select a joint",
        auto_start=False,
        drawable_mask=["fnk_rig_rigLines", "fnk_rig_rigPoints"],
        hotkey=hk1
    )

    return template
