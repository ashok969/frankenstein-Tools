
import  hou
import  viewerstate.utils as su

from frankensteinTools.viewerStates     import BaseStates
from frankensteinTools.geometries       import CollisionGeometry
from frankensteinTools.geometries       import SkeletonGeometry
from frankensteinTools.drawables        import DrawableSkin
from frankensteinTools.drawables        import DrawableSkeleton
from frankensteinTools.drawables        import DrawableConstructionPlane
from frankensteinTools.drawables        import DrawableAxis
from frankensteinTools.nodes            import SkeletonBuilderNode

from .events        import SelectJointEvent
from .events        import AddJointEvent
from .events        import MoveJointEvent
from .events        import InsertJointEvent
from .events        import RemoveJointEvent
from .events        import ParentJointEvent
from .events        import UnParentJointEvent
from .events        import OrientJointEvent

from .constants     import SkeletonTool
from .constants     import SkeletonProjectionType
from .constants     import SkeletonToolState
from .constants     import SkeletonProjectionOrient
from .constants     import SkeletonSelectionHierarchy
from .constants     import SkeletonSelectionType
from .constants     import SkeletonInsertType
from .constants     import SkeletonLockAxis
from .constants     import SkeletonFunctions

from .skeletonBuilderHUD                import HUD_TEMPLATE
from .skeletonBuilderChangeEvents       import SkeletonChangeEvents

class SkeletonBuilderViewerStates(BaseStates):

    def __init__(self, state_name, scene_viewer):
        super(SkeletonBuilderViewerStates, self).__init__(
            state_name,
            scene_viewer,
            "skeletonBuilder"
        )


        self.drawablePrefix             = "skeletonBuilder"

        # Define the drawables.
        self.skinSelectionDrawable      = DrawableSkin(
            self.stateName, 
            self.sceneViewer, 
            "{}_skinSelection".format(self.drawablePrefix))
        self.skinCollisionDrawable      = DrawableSkin(
            self.stateName, 
            self.sceneViewer, 
            "{}_skinCollision".format(self.drawablePrefix))
        self.skeletonDrawable           = DrawableSkeleton(
            self.stateName,  
            self.sceneViewer,
            "{}_skeleton".format(self.drawablePrefix))
        self.constructionPlaneDrawable  = DrawableConstructionPlane(
            self.stateName, 
            self.sceneViewer, 
            "{}_constructionPlane".format(self.drawablePrefix))
        self.axisDrawable               = DrawableAxis(
            self.stateName, 
            self.sceneViewer, 
            "{}_jointOrient".format(self.drawablePrefix))

        self.changeEvents               = SkeletonChangeEvents(self)

        # Define the tool event factory.
        self.eventFactory       = [
            SelectJointEvent(self),
            AddJointEvent(self),
            MoveJointEvent(self),
            InsertJointEvent(self),
            RemoveJointEvent(self),
            ParentJointEvent(self),
            UnParentJointEvent(self),
            OrientJointEvent(self)
        ]

        # Define the usefull internal properties.
        self.selectionBehavior          = 0
        self.selectedJoints             = []
        self.ignoreJointRename          = False
        self.findJoint                  = True
        self.findOrientPrim             = True
        self.addPreviousJointID = -1
        self.resetParent        = False

        self.oldToolID          = -1
        # Allow to handle the event chain, when we implement
        # the mouse double click event and mouse event picked.
        self.doubleClick                = False
    
    def onEnter(self, 
        kwargs:dict) -> bool:
        """ Implement the onEnter function.
            Execute by the viewer start when enter in the tool

        :param kwargs: The viewer state dictionary.
        :type kwargs: dict
        """
        # Store the skeleton builder node return by the viewer state. 
        self.node = SkeletonBuilderNode(kwargs["node"])

        # Init the viewer state HUD infos.
        self.sceneViewer.hudInfo(template=HUD_TEMPLATE)

        # Init the drawables skin geometries.
        self.skinSelectionDrawable.geometry         = CollisionGeometry(self.node.drawableSkinForSelection)
        self.skinCollisionDrawable.geometry         = CollisionGeometry(self.node.drawableSkinCollision)
        self.skinCollisionDrawable.pointsGeometry   = self.node.drawableSkinPoints

        # Init the skeleton geometries.
        self.setSkeletonDrawableGeometries()
        self.skeletonDrawable.showSkeletonJoints()
        self.skeletonDrawable.showSkeletonShapes()

        # Init the joint axis geometry.
        self.setSkeletonAxisDrawableGeometries()

        # Init the construction plane geometries.
        self.setConstructionPlaneGeometries()

        if(self.node.projectionType == SkeletonProjectionType.ConstructionPlane):
            self.constructionPlaneDrawable.showPlane()

        # Add the tool parameter callback to allow to update the viewerstate infos.
        self.changeEvents.addParmCallback()
        # Synchronize the HUD Infos.
        self.changeEvents.tool(None)

        # Add the tool parameter callback to allow to update the viewerstate infos.
        #self.node.addParmCallback(self.toolChanged, ["tool"])
        #self.node.addParmCallback(self.projectTypeChanged, ["projection_type"])
        #self.node.addParmCallback(self.constructionPlaneGlobalScaleChanged, ["projection_planeScale"])
        #
        #self.node.addParmCallback(self.jointsNameChanged, ["jointNames"])
        #self.node.addParmCallback(self.selectionHierarchyBehaviorChanged, ["selection_hierarchyBehavior"])
        #self.node.addParmCallback(self.selectionTypeChanged, ["selection_type"])
        #self.node.addParmCallback(self.insertTypeChanged, ["insert_type"])
        #self.node.addParmCallback(self.insertSnapLocationChanged, ["insert_snapLocation"])
        #self.node.addParmCallback(self.insertMultiCountChanged, ["insert_multiJointCount"])
        #self.node.addParmCallback(self.orientLockAxisChanged, ["orient_lockAxis"])
        #self.node.addParmCallback(self.orientSnapToJointChanged, ["orient_snapToJoint"])
        #self.node.addParmCallback(self.orientSnapToJointAxisChanged, ["orient_snapToJointAxis"])
        #self.node.addParmCallback(self.orientSnapToSkinPointChanged, ["orient_snapToSkinPoint"])
        #self.node.addParmCallback(self.orientDisplayScaleChanged, ["orient_displayScale"])

        # Synchronize the HUD Infos.
        # self.toolChanged(None)

    def setSkeletonAxisDrawableGeometries(self) -> None:

        self.axisDrawable.geometry          = CollisionGeometry(self.node.drawableJointOrientation)
        self.axisDrawable.helperGeometry    = CollisionGeometry(self.node.drawableOrientationHelper)
        
    def setSkeletonDrawableGeometries(self) -> None:

        self.skeletonDrawable.geometryJointPoints   = self.node.drawableSkeletonPoints
        self.skeletonDrawable.geometryJointLines    = self.node.drawableSkeletonLines
        self.skeletonDrawable.geometryJointShapes   = self.node.drawableSkeletonShapes
        self.skeletonDrawable.geometryCollision     = SkeletonGeometry(self.node.skeletonCollision)

    def onExit(self, kwargs):

        self.node.removeAllEventCallbacks()

    def onDraw(self, kwargs):

        self.skeletonDrawable.drawableJointLines.draw(kwargs["draw_handle"])
        self.axisDrawable.onDraw(kwargs)
        self.skeletonDrawable.drawableJointPoints.draw(kwargs["draw_handle"])
        self.skeletonDrawable.onDraw(kwargs)
        self.constructionPlaneDrawable.onDraw(kwargs)
        self.skinSelectionDrawable.onDraw(kwargs)
        self.skinCollisionDrawable.onDraw(kwargs)

    def onDrawInterrupt(self, kwargs):

        self.skeletonDrawable.drawableJointLines.draw(kwargs["draw_handle"])
        self.axisDrawable.onDrawInterrupt(kwargs)
        self.skeletonDrawable.drawableJointPoints.draw(kwargs["draw_handle"])
        self.skeletonDrawable.onDrawInterrupt(kwargs)
        self.constructionPlaneDrawable.onDrawInterrupt(kwargs)
        self.skinSelectionDrawable.onDrawInterrupt(kwargs)
        self.skinCollisionDrawable.onDrawInterrupt(kwargs)

    def onMouseEvent(self, kwargs):

        if(self.doubleClick is True):
            self.doubleClick = False
            return True

        uiEvent     = kwargs["ui_event"]

        return self.eventFactory[self.node.tool].mouseEvent(uiEvent)

    def onMouseWheelEvent(self, kwargs):
        """ Implement the Mouse Wheel Event.
        """
        uiEvent = kwargs["ui_event"]
        device = uiEvent.device()

        scroll = device.mouseWheel()

        tool = self.node.tool

        if(tool == SkeletonTool.AddJoint or
            tool == SkeletonTool.MoveJoint):
            if(self.node.projectionType == SkeletonProjectionType.ConstructionPlane):
                self.node.projectionPlaneScale += scroll * 0.01
                return False
            if(self.node.projectionType == SkeletonProjectionType.SurfaceDepth):
                self.node.projectionSurfaceDepthMix += scroll * 0.1
                return False
        if(tool == SkeletonTool.InsertJoint):
            insertType = self.node.insertType
            if(insertType == SkeletonInsertType.Snapped):
                self.node.insertSnapLocation += scroll * 0.1
                return False
            if(insertType == SkeletonInsertType.Multi):
                self.node.insertMultiJointCount += scroll
                return False
        if(tool == SkeletonTool.OrientJoint):
            self.node.orientDisplayScale += scroll * 0.05

        return False

    def onMouseDoubleClickEvent(self, kwargs):
        """ Implement the mouse double click event.
        """
        self.doubleClick = True
        uiEvent = kwargs["ui_event"]

        tool = self.node.tool

        return self.eventFactory[tool].mouseDoubleClickEvent(uiEvent)


    def onKeyEvent(self, kwargs):
        """ Implement the on Key Event.
        """
        uiEvent = kwargs["ui_event"]

        tool = self.node.tool

        keyPressed = uiEvent.device().keyString()

        # Define short cut for tool.
        for i, key in enumerate(SkeletonTool.KeyValues):
            if(keyPressed == key):
                self.node.tool = i
                return True

        # Define short cut for projection type and construction plane orientation. 
        if(tool == SkeletonTool.AddJoint or
           tool == SkeletonTool.MoveJoint):
            # Define short cur for projection type.
            for i, key in enumerate(SkeletonProjectionType.KeyValues):
                if(keyPressed == key):
                    self.node.projectionType = i
                    return True

            projectionType = self.node.projectionType
            if(projectionType == SkeletonProjectionType.ConstructionPlane):
                # Define short cut for construction plane orientation.
                for i, key in enumerate(SkeletonProjectionOrient.KeyValues):
                    if(keyPressed == key):
                        self.node.projectionPlaneOrient = i
                        return True
                    
            if(projectionType == SkeletonProjectionType.Surface or
               projectionType == SkeletonProjectionType.SurfaceDepth):
                if(keyPressed == "d"):
                    if(self.node.projectionSnapPoint == 1):
                        self.node.projectionSnapPoint = 0
                    else:
                        self.node.projectionSnapPoint = 1
                    return True
                if(keyPressed == "f"):
                    if(self.node.projectionRayType == 1):
                        self.node.projectionRayType = 0
                    else:
                        self.node.projectionRayType = 1
                    return True
                if(keyPressed == "g"):
                    if(self.node.projectionDepthType == 1):
                        self.node.projectionDepthType = 0
                    else:
                        self.node.projectionDepthType = 1
                    return True

            if(tool == SkeletonTool.AddJoint):
                if(keyPressed == "b"):
                    self.node.endJointChain()
                    return True

        elif(tool == SkeletonTool.InsertJoint):
            for i, key in enumerate(SkeletonInsertType.KeyValues):
                if(keyPressed == key):
                    self.node.insertType = i
                    return True
        elif(tool == SkeletonTool.OrientJoint):
            for i, key in enumerate(SkeletonLockAxis.KeyValues):
                if(keyPressed == key):
                    self.node.orientLockAxis = i
                    return True
            if(keyPressed == "d"):
                if(self.node.orientSnapToJoint == 1):
                    self.node.orientSnapToJoint = 0
                else:
                    self.node.orientSnapToJoint = 1
                return True
            if(keyPressed == "f"):
                if(self.node.orientSnapToJointAxis == 1):
                    self.node.orientSnapToJointAxis = 0
                else:
                    self.node.orientSnapToJointAxis = 1
                return True
            if(keyPressed == "g"):
                if(self.node.orientSnapToSkinPoint == 1):
                    self.node.orientSnapToSkinPoint = 0
                else:
                    self.node.orientSnapToSkinPoint = 1
                return True


        # Define short cut for All Event.
        return self.eventFactory[tool].keyEvent(uiEvent)

    def onMenuPreOpen(self, kwargs):

        menu_item_states = kwargs['menu_item_states']

        tool = self.node.tool

        if("jointSelectionMenu" in menu_item_states):
            menu_item_states["jointSelectionMenu"]["visible"] = 0
        if("skinSelectionMenu" in menu_item_states):
            menu_item_states["skinSelectionMenu"]["visible"] = 0
        if("planeMenu" in menu_item_states):
            menu_item_states["planeMenu"]["visible"] = 0

        if(tool == SkeletonTool.SelectJoints):
            selectionType = self.node.selectionType

            if(selectionType == SkeletonSelectionType.Joint):
                if("jointSelectionMenu" in menu_item_states):
                    menu_item_states["jointSelectionMenu"]["visible"] = 1
            if(selectionType == SkeletonSelectionType.Skin):
                if("skinSelectionMenu" in menu_item_states):
                    menu_item_states["skinSelectionMenu"]["visible"] = 1
        
        if(tool == SkeletonTool.AddJoint or tool == SkeletonTool.MoveJoint):
            projectionType = self.node.projectionType
            if(projectionType == SkeletonProjectionType.ConstructionPlane):
                if("planeMenu" in menu_item_states):
                    menu_item_states["planeMenu"]["visible"] = 1

    def onMenuAction(self, kwargs):

        menuItem = kwargs["menu_item"]


        if(menuItem == "invertSelection"):
            self.node.invertJointSelection()
            return True

        if(menuItem == "deleteJoints"):
            self.sceneViewer.beginStateUndo("skeleton_deleterJointSelection")
            self.node.removeSelectedJoints()
            self.sceneViewer.endStateUndo()
            return True

        if(menuItem == "setSkinToIsolate"):
            self.node.setIsolateSkinWithSkinSelection()
            return True
        
        if(menuItem ==  "symmetrizeSkeleton"):
            self.node.symmetrizeSkeleton()
            return True
        
        if(menuItem == "disableJoints"):
            self.node.setJointSelectionDisable()
            return True

        if(menuItem == "enableJoints"):
            self.node.setJointSelectionEnable()
            return True
        
        if(menuItem == "resetDisable"):
            self.node.resetDisableJoint()
            return True

        if(menuItem == "normalizeJoints"):
            self.node.normalizeJointPosition()
            return True
        
        if(menuItem == "setJointAsPlaneOrigin"):
            self.node.setJointAsPlaneOrigin()
            return True

        if(menuItem == "resetPlaneOrigin"):
            self.node.resetPlaneOrigin()
            return True
        
        if(menuItem == "resetJointsOrientation"):
            self.node.resetJointsOrient()
            return True


    def setConstructionPlaneGeometries(self):
        self.constructionPlaneDrawable.planeGeometry    = CollisionGeometry(self.node.constructionPlane)
        self.constructionPlaneDrawable.locationGeometry = CollisionGeometry(self.node.constructionPlaneLocation)
        self.constructionPlaneDrawable.borderGeometry   = CollisionGeometry(self.node.constructionPlaneBorder)


    def toolChanged(self, event_type, **kwargs):
        """ React to tool parameter changes.

        :param kwargs: _description_
        :type kwargs: _type_
        """
        tool = self.node.tool
        updateHUD = {
            "tool"                  : SkeletonTool.StringValues[tool],
            "tool_g"                : tool,
            "selectInfos"           : {"visible": False},
            "insertJointInfos"      : {"visible": False},
            "orientJointInfos"      : {"visible": False}
        }
        
        self.axisDrawable.hideGeometry()
        self.axisDrawable.hideHelper()
        self.skinSelectionDrawable.hideGeometry()
        self.skinCollisionDrawable.hideGeometryPoints()
        self.skeletonDrawable.geometryJointShapes = self.node.drawableSkeletonShapes
        self.skeletonDrawable.showSkeletonShapes()
        self.node.vsLive = 0
        
        if(tool == SkeletonTool.SelectJoints):
            updateHUD["selectInfos"] = {"visible" : True}
            self.selectionTypeChanged(None)
            self.selectionHierarchyBehaviorChanged(None)
        elif(tool == SkeletonTool.OrientJoint):
            updateHUD["orientJointInfos"] = {"visible" : True}
            self.axisDrawable.geometry  = CollisionGeometry(self.node.drawableJointOrientation)
            self.axisDrawable.helperGeometry    = CollisionGeometry(self.node.drawableOrientationHelper)
            self.axisDrawable.showGeometry()
            self.axisDrawable.showHelper()
            self.skeletonDrawable.hideSkeletonShapes()
            self.skinCollisionDrawable.showGeometryPoints()
            self.orientLockAxisChanged(None)
            self.orientSnapToJointChanged(None)
            self.orientSnapToJointAxisChanged(None)
            self.orientSnapToSkinPointChanged(None)
            self.orientDisplayScaleChanged(None)
        elif(tool == SkeletonTool.InsertJoint):
            self.insertTypeChanged(None)
            updateHUD["insertJointInfos"] = {"visible" : True}
            self.node.vsLive = 1

 
        self.sceneViewer.hudInfo(hud_values=updateHUD)

        self.projectTypeChanged(None)

        self.doubleClick = False



    def selectionTypeChanged(self, event_type, **kwargs):
        """ Execute when the selection type change.
        """
        updateHUD       = {}
        tool            = self.node.tool
        selectionType   = self.node.selectionType

        if(tool == SkeletonTool.SelectJoints):
                
            updateHUD["selectionType"]      = SkeletonSelectionType.StringValues[selectionType]
            updateHUD["selectionType_g"]    = selectionType

            if(selectionType == SkeletonSelectionType.Joint):
                updateHUD["selectJointInfos"]   = {"visible": True}
                updateHUD["selectSkinInfos"]    = {"visible": False}
                self.skinSelectionDrawable.hideGeometry()
            elif(selectionType == SkeletonSelectionType.Skin):
                updateHUD["selectJointInfos"]   = {"visible": False}
                updateHUD["selectSkinInfos"]    = {"visible": True}
                self.skinSelectionDrawable.showGeometry()

        self.sceneViewer.hudInfo(hud_values=updateHUD)

    def projectTypeChanged(self, event_type, **kwargs):
        """ Execute when the projection type change.

        :param event_type: _description_
        :type event_type: _type_
        """
        updateHUD = {}

        if(self.node.tool == SkeletonTool.AddJoint or
           self.node.tool == SkeletonTool.MoveJoint):
            updateHUD["projectionTypeInfos"]    = {"visible" : True}
        else:
            updateHUD["projectionTypeInfos"]    = {"visible" : False}
            updateHUD["constructionPlaneInfos"] = {"visible" : False}
            updateHUD["surfaceDepthInfos"]      = {"visible" : False}
            self.constructionPlaneDrawable.hidePlane()

        if(updateHUD["projectionTypeInfos"]["visible"] == True):

            updateHUD["projectionType"]     = SkeletonProjectionType.StringValues[self.node.projectionType]
            updateHUD["projectionType_g"]   = self.node.projectionType

            if(self.node.projectionType == SkeletonProjectionType.ConstructionPlane):
                self.constructionPlaneDrawable.showPlane()
                updateHUD["constructionPlaneInfos"] = {"visible" : True}
            else:
                self.constructionPlaneDrawable.hidePlane()
                updateHUD["constructionPlaneInfos"] = {"visible" : False}

            if(self.node.projectionType == SkeletonProjectionType.SurfaceDepth):
                updateHUD["surfaceDepthInfos"] = {"visible" : True}
            else:
                updateHUD["surfaceDepthInfos"] = {"visible" : False}

        self.sceneViewer.hudInfo(hud_values=updateHUD)
    
        self.setConstructionPlaneGeometries()

    def constructionPlaneGlobalScaleChanged(self, event_type, **kwargs):
        """ Execute when the construction plane global scale change.

        :param event_type: _description_
        :type event_type: _type_
        """
        updateHUD  = {}

        updateHUD["planeGlobalScale"] = "{:.2f}".format(self.node.projectionPlaneScale)

        self.sceneViewer.hudInfo(hud_values=updateHUD)



    def selectionHierarchyBehaviorChanged(self, event_type, **kwargs):
        """ Execute when the selection hierarchy behavior change.

        :param event_type: _description_
        :type event_type: _type_
        """
        updateHUD = {}
        updateHUD["selHierarchyBehavior"] = SkeletonSelectionHierarchy.StringValues[self.node.selectionHierarchyBehavior]

        self.sceneViewer.hudInfo(hud_values=updateHUD)

    def insertTypeChanged(self, event_type, **kwargs):
        """ Execute when the insert type change.

        :param event_type: _description_
        :type event_type: _type_
        """
        updateHUD   = {}
        insertType  = self.node.insertType

        updateHUD["insertFreeInfos"]    = {"visible": False}
        updateHUD["insertSnappedInfos"] = {"visible": False}
        updateHUD["insertMultiInfos"]   = {"visible": False}
        updateHUD["insertType"]         = SkeletonInsertType.StringValues[insertType]
        updateHUD["insertType_g"]       = insertType

        if(self.node.tool == SkeletonTool.InsertJoint):
            if(insertType == SkeletonInsertType.Free):
                updateHUD["insertFreeInfos"] = {"visible": True}
            elif(insertType == SkeletonInsertType.Snapped):
                updateHUD["insertSnappedInfos"] = {"visible": True}
            elif(insertType == SkeletonInsertType.Multi):
                updateHUD["insertMultiInfos"] = {"visible": True}

        self.sceneViewer.hudInfo(hud_values=updateHUD)

        self.insertSnapLocationChanged(None)
        self.insertMultiCountChanged(None)

    def insertSnapLocationChanged(self, event_type, **kwargs):
        """ Execute when the insert snap location change.

        :param event_type: _description_
        :type event_type: _type_
        """
        updateHUD = {}

        updateHUD["snapLocation"] = "{:.2f}".format(self.node.insertSnapLocation)

        self.sceneViewer.hudInfo(hud_values=updateHUD)

    def insertMultiCountChanged(self, event_type, **kwargs):
        """ Execute when the insert multi count change.

        :param event_type: _description_
        :type event_type: _type_
        """
        updateHUD = {}

        updateHUD["jointCount"] = "{}".format(self.node.insertMultiJointCount)

        self.sceneViewer.hudInfo(hud_values=updateHUD)

    def orientLockAxisChanged(self, event_type, **kwargs):
        """ Execute when the orient lock axis change.

        :param event_type: _description_
        :type event_type: _type_
        """
        updateHUD = {}

        lockAxis                = self.node.orientLockAxis
        updateHUD["lockAxis"]   = SkeletonLockAxis.StringValues[lockAxis]
        updateHUD["lockAxis_g"] = lockAxis

        self.sceneViewer.hudInfo(hud_values=updateHUD)

    def orientSnapToJointChanged(self, event_type, **kwargs):
        """ Execute when the orient snap to joint change.

        :param event_type: _description_
        :type event_type: _type_
        """
        updateHUD = {}
        updateHUD["snapToJoint"] = "Off"
        if(self.node.orientSnapToJoint == 1):
            updateHUD["snapToJoint"] = "On"
        self.sceneViewer.hudInfo(hud_values=updateHUD)

    def orientSnapToJointAxisChanged(self, event_type, **kwargs):
        """ Execute when the orient snap to joint axis change.

        :param event_type: _description_
        :type event_type: _type_
        """
        updateHUD = {}
        updateHUD["snapToJointAxis"] = "Off"
        if(self.node.orientSnapToJointAxis == 1):
            updateHUD["snapToJointAxis"] = "On"
        self.sceneViewer.hudInfo(hud_values=updateHUD)

    def orientSnapToSkinPointChanged(self, event_type, **kwargs):
        """ Execute when the orient snap skin point change.

        :param event_type: _description_
        :type event_type: _type_
        """
        updateHUD = {}
        updateHUD["snapToSkinPoint"] = "Off"
        if(self.node.orientSnapToSkinPoint == 1):
            updateHUD["snapToSkinPoint"] = "On"
        self.sceneViewer.hudInfo(hud_values=updateHUD)

    def orientDisplayScaleChanged(self, event_type, **kwargs):
        """ Execute when the orient display scale change.

        :param event_type: _description_
        :type event_type: _type_
        """
        updateHUD = {}

        updateHUD["orientDisplayScale"] = "{:.2f}".format(self.node.orientDisplayScale)

        self.sceneViewer.hudInfo(hud_values=updateHUD)
