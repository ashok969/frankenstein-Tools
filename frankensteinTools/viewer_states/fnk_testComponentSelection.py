
import hou
import viewerstate.utils as su

from    fnkTools        import FNKRigDrawable


class State(object):

    def __init__(self, state_name, scene_viewer):

        self._stateName                 = state_name
        self._sceneViewer               = scene_viewer 

        self._rigDrawable               = FNKRigDrawable(self._stateName, self._sceneViewer)
        self._node                      = None

    def onEnter(self, kwargs):

        self._node = kwargs["node"]
        self._rigDrawable.rigGeometry = self._node.node("RIG").geometry()
        self._rigDrawable.showRig
    
    def onDraw(self, kwargs):

        self._rigDrawable.setDraw(kwargs["draw_handle"])

    def onDrawInterrupt(self, kwargs):

        self._rigDrawable.setDraw(kwargs["draw_handle"])

    def onMouseEvent(self, kwargs):
        ui_event    = kwargs["ui_event"]
        dev         = ui_event.device()
        reason      = ui_event.reason()

        return False

    def onSelection(self, kwargs):

        jointID = self._rigDrawable.setSelection(kwargs)
        print(jointID)
        self._node.parm("jointID").set(jointID)


    def onLocatedSelection(self, kwargs):

        self._rigDrawable.setLocatedSelection(kwargs)


    def onStopSelection(self, kwargs):

        self._rigDrawable.setStopSelection(kwargs)

def createViewerStateTemplate():

    state_typename  = "highlight_line_points"
    state_label     = "Highlight Line Point Demo"
    state_cat       = hou.sopNodeTypeCategory()

    template        = hou.ViewerStateTemplate(
        state_typename,
        state_label,
        state_cat
    ) 
    template.bindFactory(State)

    hk1 = su.hotkey(state_typename, "drawable selector", "1")

    template.bindDrawableSelector(
        "Select a drawable component",
        auto_start=False,
        drawable_mask=["fnk_rig_rigLines", "fnk_rig_rigPoints"],
        hotkey=hk1
    )

    return template