
import hou

from frankensteinTools.nodes        import SkeletonBuilderNode

from .constants                     import SkeletonTool
from .constants                     import SkeletonProjectionType
from .constants                     import SkeletonSelectionType
from .constants                     import SkeletonSelectionHierarchy
from .constants                     import SkeletonProjectionOrient
from .constants                     import SkeletonProjectionRayType
from .constants                     import SkeletonProjectionDepthType
from .constants                     import SkeletonInsertType
from .constants                     import SkeletonLockAxis

class SkeletonChangeEvents(object):

    def __init__(self, viewerState):

        self.viewerState    = viewerState

    def addParmCallback(self) -> None:
        """ Add the node parm callbacks.
        """

        self.viewerState.node.addParmCallback(self.jointsNameChanged, ["jointNames"])

        self.viewerState.node.addParmCallback(self.tool, ["tool"])
        
        self.viewerState.node.addParmCallback(self.selectionType, ["selection_type"])
        self.viewerState.node.addParmCallback(self.selectionHierarchyBehavior, ["selection_hierarchyBehavior"])

        self.viewerState.node.addParmCallback(self.projectionType, ["projection_type"])
        self.viewerState.node.addParmCallback(self.projectionPlanOrient, ["projection_planeOrient"])
        self.viewerState.node.addParmCallback(self.projectionPlaneScale, ["projection_planeScale"])
        self.viewerState.node.addParmCallback(self.projectionPlaneOrigin, ["projection_planeOrigin"])
        self.viewerState.node.addParmCallback(self.projectionSnapPoint, ["projection_snapPoint"])
        self.viewerState.node.addParmCallback(self.projectionRayType, ["projection_rayType"])
        self.viewerState.node.addParmCallback(self.projectionDepthType, ["projection_depthType"])
        self.viewerState.node.addParmCallback(self.projectionSurfaceDepthMix, ["projection_surfaceDephtMix"])

        self.viewerState.node.addParmCallback(self.insertType, ["insert_type"])
        self.viewerState.node.addParmCallback(self.insertSnapLocation, ["insert_snapLocation"])
        self.viewerState.node.addParmCallback(self.insertMultiJointCount, ["insert_multiJointCount"])

        self.viewerState.node.addParmCallback(self.orientLockAxis, ["orient_lockAxis"])
        self.viewerState.node.addParmCallback(self.orientSnapToJoint, ["orient_snapToJoint"])
        self.viewerState.node.addParmCallback(self.orientSnapToJointAxis, ["orient_snapToJointAxis"])
        self.viewerState.node.addParmCallback(self.orientSnapToSkinPoint, ["orient_snapToSkinPoint"])
        self.viewerState.node.addParmCallback(self.orientDisplayScale, ["orient_displayScale"])



    def jointsNameChanged(self,
        event_type:hou.nodeEventType, 
        **kwargs):
        """ Execute when the tool change.

        :param event_type: The current node event type.
        :type event_type: hou.nodeEventType

        :param kwargs: The node event type details.
        :type kwargs: dict
        """
        self.viewerState.node.setJointNames(disable=self.viewerState.ignoreJointRename)

    def tool(self,
        event_type:hou.nodeEventType, 
        **kwargs):
        """ Execute when the tool change.

        :param event_type: The current node event type.
        :type event_type: hou.nodeEventType

        :param kwargs: The node event type details.
        :type kwargs: dict
        """
        # Update the HUD Tool.
        tool = self.viewerState.node.tool
        updateHUD = {
            "tool"                  : SkeletonTool.StringValues[tool],
            "tool_g"                : tool,
            "selectInfos"           : {"visible": False},
            "addInfos"              : {"visible": False},
            "moveInfos"             : {"visible": False},
            "insertJointInfos"      : {"visible": False},
            "removeInfos"           : {"visible": False},
            "orientJointInfos"      : {"visible": False},
            "parentInfos"           : {"visible": False},
            "unParentInfos"         : {"visible": False},
        }

        # Update the skeleton geometries.
        # Sometimes the skeleton geometries drawable are not correctly update.
        self.viewerState.setSkeletonDrawableGeometries()
        # Update the skin and skeleton display.
        self.viewerState.skinSelectionDrawable.hideGeometry()
        self.viewerState.skeletonDrawable.showGeometry()
        self.viewerState.constructionPlaneDrawable.hidePlane()

        self.viewerState.axisDrawable.hideGeometry()
        self.viewerState.axisDrawable.hideHelper()
        self.viewerState.skinCollisionDrawable.hideGeometryPoints()

        updateHUD = updateHUD | self.projectionType(None)
        self.viewerState.node.endJointChain()
        self.viewerState.node.vsLive = 0
        
        # Set the HUD infos to update.
        if(tool == SkeletonTool.SelectJoints):
            updateHUD["selectInfos"] = {"visible": True}
            updateHUD = updateHUD | self.selectionType(None)
            updateHUD = updateHUD | self.selectionHierarchyBehavior(None)
        if(tool == SkeletonTool.AddJoint):
            updateHUD["addInfos"] = {"visible": True}
        if(tool == SkeletonTool.MoveJoint):
            updateHUD["moveInfos"] = {"visible": True}
        if(tool == SkeletonTool.InsertJoint):
            updateHUD["insertJointInfos"] = {"visible": True}
            updateHUD = updateHUD | self.insertType(None)
            self.viewerState.node.vsLive = 1
        if(tool == SkeletonTool.RemoveJoint):
            updateHUD["removeInfos"] = {"visible": True}
        if(tool == SkeletonTool.OrientJoint):
            updateHUD["orientJointInfos"] = {"visible": True}
            self.viewerState.setSkeletonAxisDrawableGeometries()
            self.viewerState.axisDrawable.showGeometry()
            self.viewerState.axisDrawable.showHelper()
            self.viewerState.skeletonDrawable.hideSkeletonShapes()
            self.viewerState.skinCollisionDrawable.showGeometryPoints()
            updateHUD = updateHUD | self.orientLockAxis(None)
            updateHUD = updateHUD | self.orientSnapToJoint(None)
            updateHUD = updateHUD | self.orientSnapToJointAxis(None)
            updateHUD = updateHUD | self.orientSnapToSkinPoint(None)
            updateHUD = updateHUD | self.orientDisplayScale(None)

        if(tool == SkeletonTool.ParentJoint):
            updateHUD["parentInfos"] = {"visible": True}
        if(tool == SkeletonTool.UnParentJoint):
            updateHUD["unParentInfos"] = {"visible": True}


        # Update the HUD infos.
        self.viewerState.sceneViewer.hudInfo(hud_values=updateHUD)

    def selectionType(self,
        event_type:hou.nodeEventType,
        **kwargs):
        """ Execute when the selectType change.

        :param event_type: The current node event type.
        :type event_type: hou.nodeEventType

        :param kwargs: The node event type details.
        :type kwargs: dict
        """
        tool                = self.viewerState.node.tool
        selectionType   = self.viewerState.node.selectionType

        if(tool == SkeletonTool.SelectJoints):
            updateHUD       = {}

            updateHUD["selectionType"]      = SkeletonSelectionType.StringValues[selectionType]
            updateHUD["selectionType_g"]    = selectionType
            updateHUD["selectJointInfos"]   = {"visible" : True}
            updateHUD["selectSkinInfos"]    = {"visible" : False}

            if(selectionType == SkeletonSelectionType.Skin):
                updateHUD["selectJointInfos"]   = {"visible" : False}
                updateHUD["selectSkinInfos"]    = {"visible" : True}
                self.viewerState.skinSelectionDrawable.showGeometry()
                self.viewerState.skeletonDrawable.hideGeometry()
            else:
                self.viewerState.skinSelectionDrawable.hideGeometry()
                self.viewerState.skeletonDrawable.showGeometry()

            if(event_type):
                self.viewerState.sceneViewer.hudInfo(hud_values=updateHUD)
                return None
            
            return updateHUD
        return None

    def selectionHierarchyBehavior(self,
        event_type:hou.nodeEventType,
        **kwargs):
        """ Execute when the select Hierarchy change.

        :param event_type: The current node event type.
        :type event_type: hou.nodeEventType

        :param kwargs: The node event type details.
        :type kwargs: dict
        """
        tool                = self.viewerState.node.tool
        hierarchyBehavior   = self.viewerState.node.selectionHierarchyBehavior

        if(tool == SkeletonTool.SelectJoints):

            updateHUD           = {}
            updateHUD["selHierarchyBehavior"] = SkeletonSelectionHierarchy.StringValues[hierarchyBehavior]
            if(event_type):
                self.viewerState.sceneViewer.hudInfo(hud_values=updateHUD)
                return None
            
            return updateHUD

        return None

    def projectionType(self,
        event_type:hou.nodeEventType, 
        **kwargs):
        """ Execute when the surface depth mix front back change.

        :param event_type: The current node event type.
        :type event_type: hou.nodeEventType

        :param kwargs: The node event type details.
        :type kwargs: dict
        """

        tool            = self.viewerState.node.tool
        projectionType  = self.viewerState.node.projectionType

        updateHUD = {
            "projectionTypeInfos"   : {"visible" : False}
        }


        if(tool == SkeletonTool.AddJoint or tool == SkeletonTool.MoveJoint):

            self.viewerState.constructionPlaneDrawable.hidePlane()

            updateHUD["projectionTypeInfos"]    = {"visible" : True}
            updateHUD["projectionType"]         = SkeletonProjectionType.StringValues[projectionType]
            updateHUD["projectionType_g"]       = projectionType

            updateHUD["constructionPlaneInfos"] = {"visible" : False}
            updateHUD["surfaceInfos"]           = {"visible" : False}
            updateHUD["surfaceDepthInfos"]      = {"visible" : False}

            if(projectionType == SkeletonProjectionType.ConstructionPlane):
                updateHUD["constructionPlaneInfos"] = {"visible" : True}
                updateHUD = updateHUD | self.projectionPlanOrient(None)
                updateHUD = updateHUD | self.projectionPlaneScale(None)
                updateHUD = updateHUD | self.projectionPlaneOrigin(None)
                self.viewerState.constructionPlaneDrawable.showPlane()
                self.viewerState.setConstructionPlaneGeometries()

            if(projectionType == SkeletonProjectionType.Surface):
                updateHUD["surfaceInfos"]       = {"visible" : True}
                updateHUD = updateHUD | self.projectionSnapPoint(None)

            if(projectionType == SkeletonProjectionType.SurfaceDepth):
                updateHUD["surfaceInfos"]           = {"visible" : True}
                updateHUD["surfaceDepthInfos"]      = {"visible" : True}
                updateHUD = updateHUD | self.projectionSnapPoint(None)
                updateHUD = updateHUD | self.projectionRayType(None)
                updateHUD = updateHUD | self.projectionDepthType(None)
                updateHUD = updateHUD | self.projectionSurfaceDepthMix(None)

        if(event_type):
            self.viewerState.sceneViewer.hudInfo(hud_values=updateHUD)
            return None
            
        return updateHUD
            
    def projectionPlanOrient(self,
        event_type:hou.nodeEventType, 
        **kwargs):
        """ Execute when the surface depth mix front back change.

        :param event_type: The current node event type.
        :type event_type: hou.nodeEventType

        :param kwargs: The node event type details.
        :type kwargs: dict
        """
        tool            = self.viewerState.node.tool
        projectionType  = self.viewerState.node.projectionType

        if(tool == SkeletonTool.AddJoint or tool == SkeletonTool.MoveJoint):
            if(projectionType == SkeletonProjectionType.ConstructionPlane):
                planeOrient = self.viewerState.node.projectionPlaneOrient

                updateHUD = {
                    "planeOrient"   : SkeletonProjectionOrient.StringValues[planeOrient],
                    "planeOrient_g" : planeOrient
                }

                if(event_type):
                    self.viewerState.sceneViewer.hudInfo(hud_values=updateHUD)
                    return None
                
                return updateHUD
            
        return None
    
    def projectionPlaneScale(self,
        event_type:hou.nodeEventType, 
        **kwargs):
        """ Execute when the surface depth mix front back change.

        :param event_type: The current node event type.
        :type event_type: hou.nodeEventType

        :param kwargs: The node event type details.
        :type kwargs: dict
        """
        tool            = self.viewerState.node.tool
        projectionType  = self.viewerState.node.projectionType

        if(tool == SkeletonTool.AddJoint or tool == SkeletonTool.MoveJoint):
            if(projectionType == SkeletonProjectionType.ConstructionPlane):

                updateHUD = {
                    "planeGlobalScale"   : "{:.2f}".format(self.viewerState.node.projectionPlaneScale)
                }

                if(event_type):
                    self.viewerState.sceneViewer.hudInfo(hud_values=updateHUD)
                    return None
                
                return updateHUD
            
        return None
    
    def projectionPlaneOrigin(self,
        event_type:hou.nodeEventType, 
        **kwargs):
        """ Execute when the surface depth mix front back change.

        :param event_type: The current node event type.
        :type event_type: hou.nodeEventType

        :param kwargs: The node event type details.
        :type kwargs: dict
        """
        tool            = self.viewerState.node.tool
        projectionType  = self.viewerState.node.projectionType

        if(tool == SkeletonTool.AddJoint or tool == SkeletonTool.MoveJoint):
            if(projectionType == SkeletonProjectionType.ConstructionPlane):

                updateHUD = {
                    "planeOrigin"   : "World"
                }

                jointID     = self.viewerState.node.projectionPlaneOrigin
                if(jointID > -1):            
                    jointName   = self.viewerState.skeletonDrawable.geometryCollision.getJointName(jointID)
                    updateHUD["planeOrigin"] = jointName

                if(event_type):
                    self.viewerState.sceneViewer.hudInfo(hud_values=updateHUD)
                    return None
                
                return updateHUD
            
        return None

    def projectionSnapPoint(self,
        event_type:hou.nodeEventType, 
        **kwargs):
        """ Execute when the surface depth mix front back change.

        :param event_type: The current node event type.
        :type event_type: hou.nodeEventType

        :param kwargs: The node event type details.
        :type kwargs: dict
        """
        tool            = self.viewerState.node.tool
        projectionType  = self.viewerState.node.projectionType

        if(tool == SkeletonTool.AddJoint or tool == SkeletonTool.MoveJoint):
            if(projectionType == SkeletonProjectionType.Surface or
               projectionType == SkeletonProjectionType.SurfaceDepth):

                updateHUD = {
                    "surfaceSnapPoint"   : "Off"
                }

                if(self.viewerState.node.projectionSnapPoint == 1):
                    updateHUD["surfaceSnapPoint"] = "On"

                if(event_type):
                    self.viewerState.sceneViewer.hudInfo(hud_values=updateHUD)
                    return None
                
                return updateHUD
            
        return None
    
    def projectionRayType(self,
        event_type:hou.nodeEventType, 
        **kwargs):
        """ Execute when the surface depth mix front back change.

        :param event_type: The current node event type.
        :type event_type: hou.nodeEventType

        :param kwargs: The node event type details.
        :type kwargs: dict
        """
        tool            = self.viewerState.node.tool
        projectionType  = self.viewerState.node.projectionType

        if(tool == SkeletonTool.AddJoint or tool == SkeletonTool.MoveJoint):
            if(projectionType == SkeletonProjectionType.Surface or
               projectionType == SkeletonProjectionType.SurfaceDepth):

                rayType = self.viewerState.node.projectionRayType

                updateHUD = {
                    "surfaceDepthRayType"   : SkeletonProjectionRayType.StringValues[rayType]
                }

                if(event_type):
                    self.viewerState.sceneViewer.hudInfo(hud_values=updateHUD)
                    return None
                
                return updateHUD
            
        return None
    
    def projectionDepthType(self,
        event_type:hou.nodeEventType, 
        **kwargs):
        """ Execute when the surface depth mix front back change.

        :param event_type: The current node event type.
        :type event_type: hou.nodeEventType

        :param kwargs: The node event type details.
        :type kwargs: dict
        """
        tool            = self.viewerState.node.tool
        projectionType  = self.viewerState.node.projectionType

        if(tool == SkeletonTool.AddJoint or tool == SkeletonTool.MoveJoint):
            if(projectionType == SkeletonProjectionType.Surface or
               projectionType == SkeletonProjectionType.SurfaceDepth):

                depthType = self.viewerState.node.projectionDepthType

                updateHUD = {
                    "surfaceDepthDepthType"   : SkeletonProjectionDepthType.StringValues[depthType]
                }

                if(event_type):
                    self.viewerState.sceneViewer.hudInfo(hud_values=updateHUD)
                    return None
                
                return updateHUD
            
        return None

    def projectionSurfaceDepthMix(self,
        event_type:hou.nodeEventType, 
        **kwargs):
        """ Execute when the surface depth mix front back change.

        :param event_type: The current node event type.
        :type event_type: hou.nodeEventType

        :param kwargs: The node event type details.
        :type kwargs: dict
        """
        tool            = self.viewerState.node.tool
        projectionType  = self.viewerState.node.projectionType

        if(tool == SkeletonTool.AddJoint or tool == SkeletonTool.MoveJoint):
            if(projectionType == SkeletonProjectionType.Surface or
               projectionType == SkeletonProjectionType.SurfaceDepth):

                updateHUD = {
                    "surfaceDepthMix"   : "{:.2f}".format(self.viewerState.node.projectionSurfaceDepthMix)
                }

                if(event_type):
                    self.viewerState.sceneViewer.hudInfo(hud_values=updateHUD)
                    return None
                
                return updateHUD
            
        return None
    
    def insertType(self,
        event_type:hou.nodeEventType, 
        **kwargs):
        """ Execute when the surface depth mix front back change.

        :param event_type: The current node event type.
        :type event_type: hou.nodeEventType

        :param kwargs: The node event type details.
        :type kwargs: dict
        """
        tool            = self.viewerState.node.tool

        if(tool == SkeletonTool.InsertJoint):

            insertType = self.viewerState.node.insertType

            updateHUD = {
                "insertType"            : SkeletonInsertType.StringValues[insertType],
                "insertType_g"          : insertType,
                "insertJointActions"    : {"visible" : True},
                "insertSnappedInfos"    : {"visible" : False},
                "insertMultiInfos"      : {"visible" : False}
            }

            if(insertType == SkeletonInsertType.Snapped):
                updateHUD["insertSnappedInfos"] = {"visible" : True}
                updateHUD = updateHUD | self.insertSnapLocation(None)
            if(insertType == SkeletonInsertType.Multi):
                updateHUD["insertMultiInfos"] = {"visible" : True}
                updateHUD = updateHUD | self.insertMultiJointCount(None)

            if(event_type):
                self.viewerState.sceneViewer.hudInfo(hud_values=updateHUD)
                return None
            
            return updateHUD
        
        return None
    
    def insertSnapLocation(self,
        event_type:hou.nodeEventType, 
        **kwargs):
        """ Execute when the surface depth mix front back change.

        :param event_type: The current node event type.
        :type event_type: hou.nodeEventType

        :param kwargs: The node event type details.
        :type kwargs: dict
        """
        tool            = self.viewerState.node.tool

        if(tool == SkeletonTool.InsertJoint):

            insertType = self.viewerState.node.insertType

            updateHUD = {}

            if(insertType == SkeletonInsertType.Snapped):
                updateHUD["snapLocation"] = "{:.2f}".format(self.viewerState.node.insertSnapLocation)

            if(event_type):
                self.viewerState.sceneViewer.hudInfo(hud_values=updateHUD)
                return None
            
            return updateHUD
        
        return None

    def insertMultiJointCount(self,
        event_type:hou.nodeEventType, 
        **kwargs):
        """ Execute when the surface depth mix front back change.

        :param event_type: The current node event type.
        :type event_type: hou.nodeEventType

        :param kwargs: The node event type details.
        :type kwargs: dict
        """
        tool            = self.viewerState.node.tool

        if(tool == SkeletonTool.InsertJoint):

            insertType = self.viewerState.node.insertType

            updateHUD = {}

            if(insertType == SkeletonInsertType.Multi):
                updateHUD["jointCount"] = "{}".format(self.viewerState.node.insertMultiJointCount)

            if(event_type):
                self.viewerState.sceneViewer.hudInfo(hud_values=updateHUD)
                return None
            
            return updateHUD
        
        return None
    
    def orientLockAxis(self,
        event_type:hou.nodeEventType, 
        **kwargs):
        """ Execute when the surface depth mix front back change.

        :param event_type: The current node event type.
        :type event_type: hou.nodeEventType

        :param kwargs: The node event type details.
        :type kwargs: dict
        """ 
        tool            = self.viewerState.node.tool

        if(tool == SkeletonTool.OrientJoint):

            lockAxis = self.viewerState.node.orientLockAxis

            updateHUD = {
                "lockAxis"      : SkeletonLockAxis.StringValues[lockAxis],
                "lockAxis_g"    : lockAxis
            }

            if(event_type):
                self.viewerState.sceneViewer.hudInfo(hud_values=updateHUD)
                return None
            
            return updateHUD
        
        return None
    
    def orientSnapToJoint(self,
        event_type:hou.nodeEventType, 
        **kwargs):
        """ Execute when the surface depth mix front back change.

        :param event_type: The current node event type.
        :type event_type: hou.nodeEventType

        :param kwargs: The node event type details.
        :type kwargs: dict
        """ 
        tool            = self.viewerState.node.tool

        if(tool == SkeletonTool.OrientJoint):

            snapToJoint = self.viewerState.node.orientSnapToJoint

            updateHUD = {"snapToJoint" : "Off"}

            if(snapToJoint == 1):
                updateHUD["snapToJoint"] = "On"

            if(event_type):
                self.viewerState.sceneViewer.hudInfo(hud_values=updateHUD)
                return None
            
            return updateHUD
        
        return None
    
    def orientSnapToJointAxis(self,
        event_type:hou.nodeEventType, 
        **kwargs):
        """ Execute when the surface depth mix front back change.

        :param event_type: The current node event type.
        :type event_type: hou.nodeEventType

        :param kwargs: The node event type details.
        :type kwargs: dict
        """ 
        tool            = self.viewerState.node.tool

        if(tool == SkeletonTool.OrientJoint):

            snapToJointAxis = self.viewerState.node.orientSnapToJointAxis

            updateHUD = {"snapToJointAxis" : "Off"}

            if(snapToJointAxis == 1):
                updateHUD["snapToJointAxis"] = "On"

            if(event_type):
                self.viewerState.sceneViewer.hudInfo(hud_values=updateHUD)
                return None
            
            return updateHUD
        
        return None
    
    def orientSnapToSkinPoint(self,
        event_type:hou.nodeEventType, 
        **kwargs):
        """ Execute when the surface depth mix front back change.

        :param event_type: The current node event type.
        :type event_type: hou.nodeEventType

        :param kwargs: The node event type details.
        :type kwargs: dict
        """ 
        tool            = self.viewerState.node.tool

        if(tool == SkeletonTool.OrientJoint):

            snapToSkinPoint = self.viewerState.node.orientSnapToSkinPoint

            updateHUD = {"snapToSkinPoint" : "Off"}

            if(snapToSkinPoint == 1):
                updateHUD["snapToSkinPoint"] = "On"

            if(event_type):
                self.viewerState.sceneViewer.hudInfo(hud_values=updateHUD)
                return None
            
            return updateHUD
        
        return None
    
    def orientDisplayScale(self,
        event_type:hou.nodeEventType, 
        **kwargs):
        """ Execute when the surface depth mix front back change.

        :param event_type: The current node event type.
        :type event_type: hou.nodeEventType

        :param kwargs: The node event type details.
        :type kwargs: dict
        """ 
        tool            = self.viewerState.node.tool

        if(tool == SkeletonTool.OrientJoint):

            updateHUD = {"orientDisplayScale" : "{:.2f}".format(self.viewerState.node.orientDisplayScale)}

            if(event_type):
                self.viewerState.sceneViewer.hudInfo(hud_values=updateHUD)
                return None
            
            return updateHUD
        
        return None