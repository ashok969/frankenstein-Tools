
import  hou
import  viewerstate.utils as su

from frankensteinTools.viewerStates.skeletonBuilder     import SkeletonBuilderViewerStates

def createViewerStateTemplate():
    """ Function to register the viewer state template.
    """

    state_typename      = "frankenstein__SkeletonBuilder"
    state_label         = "Frankenstein Skeleton Builder Tools"
    state_cat           = hou.sopNodeTypeCategory()
    
    template            = hou.ViewerStateTemplate(state_typename, state_label, state_cat)
    template.bindFactory(SkeletonBuilderViewerStates)
    template.bindIcon("SOP_kinefx-skeleton")

    """
    hk1 = su.hotkey(state_typename, "drawable selector", "1")

    template.bindDrawableSelector(
        "Select Joints",
        auto_start=False,
        drawable_mask=["skeleton_jointPoints"],
        hotkey=hk1,
        name="skeleton_jointsSelector"
    )
    """

    menu = hou.ViewerStateMenu("actionsMenu", "Actions")

    menu.addActionItem("invertSelection", "Invert Selection")

    menu.addSeparator()

    menu.addActionItem("clearSelection", "Clear Selection")

    menu.addSeparator()

    menu.addActionItem("enableSelectedJoints", "Enable Selected Joints")

    menu.addActionItem("disableSelectedJoints", "Disable Selected Joints")

    menu.addActionItem("disableUnselectedJoints", "Disable Unselected Joints")

    menu.addActionItem("resetDisable", "Reset Joints Disable")

    menu.addSeparator()

    menu.addActionItem("focusGeometry", "Focus Geometry")

    menu.addActionItem("focusSetSelected", "Set Selected Geometry to Focus")

    menu.addActionItem("focusAddSelected", "Add Selected Geometry to Focus")

    menu.addActionItem("focusRemoveSelected", "Remove Selected Geometry from Focus")

    menu.addActionItem("focusClear", "Clear Focus Geometry")

    menu.addSeparator()


    skinSelectionMenu = hou.ViewerStateMenu("skinSelectionMenu", "Skin Selection")

    skinSelectionMenu.addActionItem("setSkinToIsolate", "Isolate Skin Selection")

    menu.addMenu(skinSelectionMenu)

    planeMenu = hou.ViewerStateMenu("planeMenu", "Contruction Plane")

    planeMenu.addActionItem("setJointAsPlaneOrigin", "Set Joint As Plane Origin")

    planeMenu.addActionItem("resetPlaneOrigin", "Reset Plan Origin")

    menu.addMenu(planeMenu)

    toolsMenu = hou.ViewerStateMenu("toolsMenu", "Tools Menu")

    toolsMenu.addActionItem("deleteJoints", "Delete Joints")

    toolsMenu.addActionItem("symmetrizeSkeleton", "Symmetrize Skeleton")

    toolsMenu.addActionItem("normalizeJoints", "Normalize Joints")

    toolsMenu.addActionItem("resetJointsOrientation", "Reset Joints Orientation")

    menu.addMenu(toolsMenu)


    template.bindMenu(menu)

    return template