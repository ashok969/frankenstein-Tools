
import hou

from frankensteinTools.viewerStates.skeletonBuilder.constants   import SkeletonTool
from frankensteinTools.viewerStates.skeletonBuilder.constants   import SkeletonFunctions

from .hNode         import HNode



class SkeletonBuilderNode(HNode):

    def __init__(self, node:hou.Node):
        super(SkeletonBuilderNode, self).__init__(node)


    def resetJointsOrient(self) -> None:
        """ Reset the joints orientation.
        """
        oldTool             = self.tool
        self.tool           = SkeletonTool.SelectJoints
        self.functions      = SkeletonFunctions.ResetJointsOrientation
        self.vsToolState    = 1
        self.cache()
        self.vsToolState    = 0
        self.functions      = SkeletonFunctions.Void
        self.tool           = oldTool

    def setJointNames(self, disable:bool=False):
        """ Rename the joints

        :param enable: Allow the renaming, defaults to False
        :type enable: bool, optional
        """
        if(disable == True):
            return False
        
        if(self.tool != SkeletonTool.SelectJoints):
            return False

        self.functions         = SkeletonFunctions.RenameJoints
        self.vsToolState       = 1
        self.cache()
        self.vsToolState       = 0
        self.functions         = SkeletonFunctions.Void
        self.namingSequence    = 0

        return True
    
    def resetSkeletonCache(self, node:hou.Node=None) -> None:
        """ Reset the skeleton cache.

        :param node: The current node, defaults to None
        :type node: hou.Node, optional
        """
        if(node):
            self.node = node

        self.fromCache.parm("stashinput").pressButton()

    def endJointChain(self) -> None:
        """ End the joint chain.
        """
        self.vsJointParentID = -1

    def resetDisableJoint(self) -> None:
        """ Reset the disable joint.
        """
        pass

    def resetPlaneOrigin(self) -> None:
        """ Set the contruction plan origin to world.
        """
        self.projectionPlaneOrigin = -1

    def setJointAsPlaneOrigin(self) -> None:
        """ Set the current selected joint as contruction plan origin.
        """
        self.projectionPlaneOrigin = self.vsJointHighlight

    def normalizeJointPosition(self) -> None:
        """ Normalize the joint selection position.
        """
        oldTool         = self.tool
        self.tool       = SkeletonTool.SelectJoints
        self.functions  = SkeletonFunctions.NormalizeJoints
        self.cache()
        self.functions  = SkeletonFunctions.Void
        self.tool       = oldTool

        return True

    def invertJointSelection(self) ->  None:
        """ Invert the joint selection.
        """
        jointSelection = self.vsJointSelection
        
        invertedSelection = [point.number() 
            for point in self.skeletonCollision.points()
            if point.number() not in jointSelection]
        
        self.vsJointSelection = invertedSelection
        self.updateJointsNameFromSelection()

    def removeSelectedJoints(self) -> None:
        """ Remove the selected joints.
        """        
        if(self.tool != SkeletonTool.SelectJoints):
            return False
        
        if(len(self.vsJointSelection) == 0):
            return False

        self.functions          = SkeletonFunctions.RemoveSelectedJoints
        self.cache()
        self.functions          = SkeletonFunctions.Void

        self.vsJointSelection = []
        self.updateJointsNameFromSelection()

        return True

    def symmetrizeSkeleton(self) -> None:
        """ Symmetrize the skeleton.
        """

        oldTool         = self.tool
        self.tool       = SkeletonTool.SelectJoints
        self.functions  = SkeletonFunctions.SymmetrizeSkeleton
        self.cache()
        self.functions  = SkeletonFunctions.Void
        self.tool       = oldTool


        return True

    def setJointSelectionDisable(self) -> None:
        """ Set the current joint selection to disable.
        """
        oldTool         = self.tool
        self.tool       = SkeletonTool.SelectJoints
        self.functions  = SkeletonFunctions.DisableJoints
        self.cache()
        self.functions  = SkeletonFunctions.Void
        self.tool       = oldTool

        self.vsJointSelection = []
        self.updateJointsNameFromSelection()

        return True

    def setJointSelectionEnable(self) -> None:
        """ Set the current joint selection to disable.
        """
        oldTool         = self.tool
        self.tool       = SkeletonTool.SelectJoints
        self.functions  = SkeletonFunctions.EnableJoints
        self.cache()
        self.functions  = SkeletonFunctions.Void
        self.tool       = oldTool

        self.vsJointSelection = []
        self.updateJointsNameFromSelection()

        return True

    def setIsolateSkinWithSkinSelection(self) -> None:
        """ Add the skin selection to the skin isolate.
        """
        self.geometrySkinToIsolate = self.vsSkinSelection

    def cache(self) -> None:
        """ Store the geometry to the node internal cache.
        """
        self.skeletonCache = self.toCache.geometry()

    def resetRays(self) -> None:
        """ Reset the ray data parameters.
        """
        self.vsRayOrigin      = hou.Vector3()
        self.vsRayDirection   = hou.Vector3()

    def addSkinToSelection(self,
        skinPaths:list[str]) -> None:
        """ Add the skin path to the skin selection.

        :param skinPaths: The list of skin path to add.
        :type skinPaths: list[str]
        """
        selection = self.vsSkinSelection
        addSkin = [path for path in skinPaths if path not in selection]
        self.vsSkinSelection = selection + addSkin

    def removeSkinFromSelection(self,
        skinPaths:list[str]) -> None:
        """ Remove the skin path from the skin selection.

        :param skinPaths: The list of skin path to remove.
        :type skinPaths: list[str]
        """
        self.vsSkinSelection = [path for path in self.vsSkinSelection if path not in skinPaths]

    def addToSelectedJointIDs(self,
        jointIDs:list[int]) -> None:
        """ Add the joint IDs to the current joint seletion.

        :param jointIDs: The joint to add to selection. 
        :type jointIDs: list[int]
        """
        selection = self.vsJointSelection
        addJoints = [jointID for jointID in jointIDs if jointID not in selection]
        self.vsJointSelection = selection + addJoints

    def removeFromJointIDs(self,
        jointIDs:list[int]) -> None:
        """ Remove the joint IDs from the current joint selection.

        :param jointIDs: The joint to remove from selection.
        :type jointIDs: list[int]
        """
        self.vsJointSelection = [jointID for jointID in self.vsJointSelection if jointID not in jointIDs]

    def updateJointsNameFromSelection(self) -> None:
        """ Update the joint names from the current joint seleciton.
        """
        skeletonGeometry    = self.skeletonCollision
        points              = skeletonGeometry.points()
        if(self.namingUseRules == 0):
            self.jointNames     = [points[jointID].attribValue("name") for jointID in self.vsJointSelection]
        else:
            self.jointNames     = ["_".join(points[jointID].attribValue("name").split("_")[1:]) for jointID in self.vsJointSelection]

    # ================
    # ================
    # NODE PARAMETERS.
    # ================
    # ================

    @property
    def tool(self) -> int:
        return self.parm("tool").eval()

    @tool.setter
    def tool(self, value:int) -> None:
        self.parm("tool").set(value)

    @property
    def functions(self) -> int:
        return self.parm("functions").eval()
    
    @functions.setter
    def functions(self, value:int) -> None:
        self.parm("functions").set(value)

    # ======================
    # PROJECTION PARAMETERS.
    # ======================
     
    @property
    def projectionType(self) -> int:
        return self.parm("projection_type").eval()
    
    @projectionType.setter
    def projectionType(self, value:int) -> None:
        self.parm("projection_type").set(value)

    @property
    def projectionPlaneOrient(self) -> int:
        return self.parm("projection_planeOrient").eval()
    
    @projectionPlaneOrient.setter
    def projectionPlaneOrient(self, value:int) -> None:
        self.parm("projection_planeOrient").set(value)

    @property
    def projectionPlaneOrigin(self) -> int:
        return self.parm("projection_planeOrigin").eval()
    
    @projectionPlaneOrigin.setter
    def projectionPlaneOrigin(self, value:int) -> None:
        self.parm("projection_planeOrigin").set(value)

    @property
    def projectionPlaneToFloor(self) -> int:
        return self.parm("projection_planeToFloor").eval()

    @projectionPlaneToFloor.setter
    def projectionPlaneToFloor(self, value:int) -> None:
        self.parm("projection_planeToFloor").set(value)

    @property
    def projectionPlaneScale(self) -> float:
        return self.parm("projection_planeScale").eval()
    
    @projectionPlaneScale.setter
    def projectionPlaneScale(self, value:float) -> None:
        self.parm("projection_planeScale").set(value)

    @property
    def projectionPlaneOffsetPos(self) -> hou.Vector3:
        return self.getVector3Parm("projection_planeOffsetPos")
    
    @projectionPlaneOffsetPos.setter
    def projectionPlaneOffsetPos(self, value:hou.Vector3) -> None:
        self.setVector3Parm("projection_planeOffsetPos", value)

    @property
    def projectionPlaneOffsetRot(self) -> hou.Vector3:
        return self.getVector3Parm("projection_planeOffsetRot")

    @projectionPlaneOffsetRot.setter
    def projectionPlaneOffsetRot(self, value:hou.Vector3) -> None:
        self.setVector3Parm("projection_planeOffsetRot", value)
    
    @property
    def projectionPlaneOffsetScl(self) -> hou.Vector3:
        return self.getVector3Parm("projection_planeOffsetScl")

    @projectionPlaneOffsetScl.setter
    def projectionPlaneOffsetScl(self, value:hou.Vector3) -> None:
        self.setVector3Parm("projection_planeOffsetScl", value)

    @property
    def projectionSurfaceDepthMix(self) -> float:
        return self.parm("projection_surfaceDephtMix").eval()
    
    @projectionSurfaceDepthMix.setter
    def projectionSurfaceDepthMix(self, value:float) -> None:
        self.parm("projection_surfaceDephtMix").set(value)

    @property
    def projectionRayType(self) -> int:
        return self.parm("projection_rayType").eval()

    @projectionRayType.setter
    def projectionRayType(self, value:int) -> None:
        self.parm("projection_rayType").set(value)
    
    @property
    def projectionDepthType(self) -> int:
        return self.parm("projection_depthType").eval()

    @projectionDepthType.setter
    def projectionDepthType(self, value:int) -> None:
        self.parm("projection_depthType").set(value)

    @property
    def projectionSnapPoint(self) -> int:
        return self.parm("projection_snapPoint").eval()

    @projectionSnapPoint.setter
    def projectionSnapPoint(self, value:int) -> None:
        self.parm("projection_snapPoint").set(value)
    
    # ========================
    # VIEWER STATES PARAMETERS
    # ========================
        
    @property
    def vsToolState(self) -> int:
        return self.parm("vs_toolState").eval()
    
    @vsToolState.setter
    def vsToolState(self, value:int) -> None:
        self.parm("vs_toolState").set(value)

    @property
    def vsRayOrigin(self) -> hou.Vector3:
        return self.getVector3Parm("vs_rayOrigin")
    
    @vsRayOrigin.setter
    def vsRayOrigin(self, value:hou.Vector3) -> None:
        self.setVector3Parm("vs_rayOrigin", value)

    @property
    def vsRayDirection(self) -> hou.Vector3:
        return self.getVector3Parm("vs_rayDirection")

    @vsRayDirection.setter
    def vsRayDirection(self, value:hou.Vector3) -> None:
        self.setVector3Parm("vs_rayDirection", value)

    @property
    def vsJointID(self) -> int:
        return self.parm("vs_jointID").eval()
    
    @vsJointID.setter
    def vsJointID(self, value:int) -> None:
        self.parm("vs_jointID").set(value)

    @property
    def vsJointPrimID(self) -> int:
        return self.parm("vs_jointPrimID").eval()
    
    @vsJointPrimID.setter
    def vsJointPrimID(self, value:int) -> None:
        self.parm("vs_jointPrimID").set(value)
    
    @property
    def vsJointPrimUVW(self) -> hou.Vector3:
        return self.getVector3Parm("vs_jointPrimUVW")
    
    @vsJointPrimUVW.setter
    def vsJointPrimUVW(self, value:hou.Vector3) -> None:
        self.setVector3Parm("vs_jointPrimUVW", value)

    @property
    def vsJointSelection(self) -> list[int]:
        selection = self.parm("vs_jointSelection").evalAsString()
        if(selection == ""):
            return []
        return [int(jointID) for jointID in selection.split(" ")]

    @vsJointSelection.setter
    def vsJointSelection(self, value:list[int]) -> None:
        selection = ""
        if(len(value) > 0):
            selection = " ".join([str(jointID) for jointID in value])
        self.parm("vs_jointSelection").set(selection)

    @property
    def vsJointParentID(self) -> int:
        return self.parm("vs_jointParentID").eval()
    
    @vsJointParentID.setter
    def vsJointParentID(self, value:int) -> None:
        self.parm("vs_jointParentID").set(value)

    @property
    def vsJointHighlight(self) -> int:
        return self.parm("vs_jointHighlight").eval()
    
    @vsJointHighlight.setter
    def vsJointHighlight(self, value:int) -> None:
        self.parm("vs_jointHighlight").set(value)

    @property
    def vsOrientPrim(self) -> int:
        return self.parm("vs_orientPrim").eval()
    
    @vsOrientPrim.setter
    def vsOrientPrim(self, value:int) -> None:
        self.parm("vs_orientPrim").set(value)

    @property
    def vsOrientTargetPrim(self) -> int:
        return self.parm("vs_orientTargetPrim").eval()
    
    @vsOrientTargetPrim.setter
    def vsOrientTargetPrim(self, value:int) -> None:
        self.parm("vs_orientTargetPrim").set(value)

    @property
    def vsOrientJointID(self) -> int:
        return self.parm("vs_orientJointID").eval()
    
    @vsOrientJointID.setter
    def vsOrientJointID(self, value:int) -> None:
        self.parm("vs_orientJointID").set(value)

    @property
    def vsOrientAxis(self) -> int:
        return self.parm("vs_orientAxis").eval()
    
    @vsOrientAxis.setter
    def vsOrientAxis(self, value:int) -> None:
        self.parm("vs_orientAxis").set(value)

    @property
    def vsSkinSelection(self) -> list[str]:
        selection       = self.parm("vs_skinSelection").evalAsString()
        if(selection == ""):
            return []
        
        return [skin.split("@path=")[-1] for skin in selection.split(" ")]

    @vsSkinSelection.setter
    def vsSkinSelection(self, value:list[str]) -> None:
        if(len(value) > 0):
            selection = ["@path={}".format(path) for path in value if path != ""]
            selection = " ".join(selection)
            self.parm("vs_skinSelection").set(selection)
        else:
            self.parm("vs_skinSelection").set("")

    @property
    def vsSkinHighlight(self) -> str:
        path = self.parm("vs_skinHighlight").evalAsString()
        if(path == ""):
            return []
        
        return path.split("@path=")[-1]
    
    @vsSkinHighlight.setter
    def vsSkinHighlight(self, value:str) -> None:
        if(value != ""):
            self.parm("vs_skinHighlight").set("@path={}".format(value))
        else:
            self.parm("vs_skinHighlight").set("")

    @property
    def vsSkinPointsSelection(self) -> list[int]:
        selection = self.parm("vs_skinPointsSelection").evalAsString()
        if(selection == ""):
            return []
        return [int(jointID) for jointID in selection.split(" ")]
    
    @vsSkinPointsSelection.setter
    def vsSkinPointsSelection(self, value:list[int]) -> None:
        selection = ""
        if(len(value) > 0):
            selection = " ".join([str(jointID) for jointID in value])
        self.parm("vs_skinPointsSelection").set(selection)

    @property
    def vsSkinPointHighlight(self) -> int:
        return self.parm("vs_skinPointHighlight").eval()

    @vsSkinPointHighlight.setter
    def vsSkinPointHighlight(self, value:int) -> None:
        self.parm("vs_skinPointHighlight").set(value)

    @property
    def vsOrientTargetJointID(self) -> int:
        return self.parm("vs_orientTargetJointID").eval()

    @vsOrientTargetJointID.setter
    def vsOrientTargetJointID(self, value:int) -> None:
        self.parm("vs_orientTargetJointID").set(value)

    @property
    def vsOrientTargetAxis(self) -> int:
        return self.parm("vs_orientTargetAxis").eval()
    
    @vsOrientTargetAxis.setter
    def vsOrientTargetAxis(self, value:int) -> None:
        self.parm("vs_orientTargetAxis").set(value)

    @property
    def vsLive(self) -> int:
        return self.parm("vs_live").eval()
    
    @vsLive.setter
    def vsLive(self, value:int) -> None:
        self.parm("vs_live").set(value)

    @property
    def vsJointPrimHighlight(self) -> int:
        return self.parm("vs_jointPrimHighlight").eval()
    
    @vsJointPrimHighlight.setter
    def vsJointPrimHighlight(self, value:int) -> None:
        self.parm("vs_jointPrimHighlight").set(value)

    @property
    def vsSkinPointID(self) -> int:
        return self.parm("vs_skinPointID").eval()
    
    @vsSkinPointID.setter
    def vsSkinPointID(self, value:int) -> None:
        self.parm("vs_skinPointID").set(value)

    @property
    def vsSkinPrimID(self) -> int:
        return self.parm("vs_skinPrimID").eval()
    
    @vsSkinPrimID.setter
    def vsSkinPrimID(self, value:int) -> None:
        self.parm("vs_skinPrimID").set(value)
    
    @property
    def vsSkinPrimUVW(self) -> hou.Vector3:
        return self.getVector3Parm("vs_skinPrimUVW")
    
    @vsSkinPrimUVW.setter
    def vsSkinPrimUVW(self, value:hou.Vector3) -> None:
        self.setVector3Parm("vs_skinPrimUVW", value)

    # ====================
    # GEOMETRY PARAMETERS.
    # ====================
    
    @property
    def geometryIsolateSelection(self) -> int:
        return self.parm("geometry_isolateSelection").eval()
    
    @geometryIsolateSelection.setter
    def geometryIsolateSelection(self, value:int) -> None:
        self.parm("geometry_isolateSelection").set(value)

    @property
    def geometrySkinToIsolate(self) -> list[str]:
        selection       = self.parm("geometry_skinToIsolate").evalAsString()
        if(selection == ""):
            return []
        
        return [skin.split("@path=")[-1] for skin in selection.split(" ")]        
    
    @geometrySkinToIsolate.setter
    def geometrySkinToIsolate(self, value:list[str]) -> None:
        if(len(value) > 0):
            selection = ["@path={}".format(path) for path in value if path != ""]
            selection = " ".join(selection)
            self.parm("geometry_skinToIsolate").set(selection)
        else:
            self.parm("geometry_skinToIsolate").set("")

    # =====================
    # SELECTION PARAMETERS.
    # =====================
    
    @property
    def selectionType(self) -> int:
        return self.parm("selection_type").eval()
    
    @selectionType.setter
    def selectionType(self, value:int) -> None:
        self.parm("selection_type").set(value)

    # ==================
    # COLOR PRARMETERS.
    # ==================        
    
    @property
    def colorMiddle(self) -> hou.Vector3:
        return self.getVector3Parm("color_middle")
    
    @colorMiddle.setter
    def colorMiddle(self, value:hou.Vector3) -> None:
        self.setVector3Parm("color_middle", value)

    @property
    def colorLeft(self) -> hou.Vector3:
        return self.getVector3Parm("color_left")
    
    @colorLeft.setter
    def colorLeft(self, value:hou.Vector3) -> None:
        self.setVector3Parm("color_left", value)

    @property
    def colorRight(self) -> hou.Vector3:
        return self.getVector3Parm("color_right")

    @colorRight.setter
    def colorRight(self, value:hou.Vector3) -> None:
        self.setVector3Parm("color_right", value)

    @property
    def colorSelected(self) -> hou.Vector3:
        return self.getVector3Parm("color_selected")
    
    @colorSelected.setter
    def colorSelected(self, value:hou.Vector3) -> None:
        self.setVector3Parm("color_selected", value)

    @property
    def colorHighlight(self) -> hou.Vector3:
        return self.getVector3Parm("color_highlight")
    
    @colorHighlight.setter
    def colorHighlight(self, value:hou.Vector3) -> None:
        self.setVector3Parm("color_highlight", value)

    @property
    def colorHelper(self) -> hou.Vector3:
        return self.getVector3Parm("color_helper")
    
    @colorHelper.setter
    def colorHelper(self, value:hou.Vector3) -> None:
        self.setVector3Parm("color_helper", value)

    @property
    def colorPlane(self) -> hou.Vector3:
        return self.getVector3Parm("color_plane")
    
    @colorPlane.setter
    def colorPlane(self, value:hou.Vector3) -> None:
        self.setVector3Parm("color_plane")

    @property
    def colorDisable(self) -> hou.Vector3:
        return self.getVector3Parm("color_disable")
    
    @colorDisable.setter
    def colorDisable(self, value:hou.Vector3):
        self.setVector3Parm("color_disable")

    # ==================
    # NAMING PARAMETERS.
    # ==================

    @property
    def namingBase(self) -> str:
        return self.parm("naming_base").evalAsString()
    
    @namingBase.setter
    def namingBase(self, value:str) -> None:
        self.parm("naming_base").set(value)

    @property
    def namingPart(self) -> str:
        return self.parm("naming_part").evalAsString()
    
    @namingPart.setter
    def namingPart(self, value:str) -> None:
        self.parm("naming_part").set(value)

    @property
    def namingPrefixLeft(self) -> str:
        return self.parm("naming_prefixLeft").evalAsString()
    
    @namingPrefixLeft.setter
    def namingPrefixLeft(self, value:str) -> None:
        self.parm("naming_prefixLeft").set(value)

    @property
    def namingPrefixRight(self) -> str:
        return self.parm("naming_prefixRight").evalAsString()
    
    @namingPrefixRight.setter
    def namingPrefixRight(self, value:str) -> None:
        self.parm("naming_prefixRight").set(value)

    @property
    def namingPrefixMiddle(self) -> str:
        return self.parm("naming_prefixMiddle").evalAsString()
    
    @namingPrefixMiddle.setter
    def namingPrefixMiddle(self, value:str) -> None:
        self.parm("naming_prefixMiddle").set(value)

    @property
    def namingSequence(self) -> int:
        return self.parm("naming_sequence").eval()
    
    @namingSequence.setter
    def namingSequence(self, value:int) -> None:
        self.parm("naming_sequence").set(value)

    @property
    def namingUseRules(self) -> int:
        return self.parm("naming_useRules").eval()
    
    @namingUseRules.setter
    def namingUseRules(self, value:int) -> None:
        self.parm("nameing_useRules").set(value)

    @property
    def jointNames(self) -> list[str]:
        names = self.parm("jointNames").evalAsString()
        if(names == ""):
            return []
        return names.split(" ")

    @jointNames.setter
    def jointNames(self, value:list[str]):
        names = ""
        if(len(value) > 0):
            names = " ".join(value)
        self.parm("jointNames").set(names)

    # =====================
    # SELECTION PARAMETERS.
    # =====================
    @property
    def selectionHierarchyBehavior(self) -> int:
        return self.parm("selection_hierarchyBehavior").eval()
    
    @selectionHierarchyBehavior.setter
    def selectionHierarchyBehavior(self, value:int) -> None:
        self.parm("selection_hierarchyBehavior").set(value)

    # ==================
    # INSERT PARAMETERS.
    # ==================
    @property
    def insertType(self) -> int:
        return self.parm("insert_type").eval()
    
    @insertType.setter
    def insertType(self, value:int) -> None:
        self.parm("insert_type").set(value)

    @property
    def insertSnapLocation(self) -> float:
        return self.parm("insert_snapLocation").eval()
    
    @insertSnapLocation.setter
    def insertSnapLocation(self, value:float) -> None:
        self.parm("insert_snapLocation").set(value)

    @property
    def insertMultiJointCount(self) -> int:
        return self.parm("insert_multiJointCount").eval()

    @insertMultiJointCount.setter
    def insertMultiJointCount(self, value:int) -> None:
        self.parm("insert_multiJointCount").set(value)

    # ==================
    # ORIENT PARAMETERS.
    # ==================
    @property
    def orientLockAxis(self) -> int:
        return self.parm("orient_lockAxis").eval()
    
    @orientLockAxis.setter
    def orientLockAxis(self, value:int) -> None:
        self.parm("orient_lockAxis").set(value)

    @property
    def orientSnapToJoint(self) -> int:
        return self.parm("orient_snapToJoint").eval()
    
    @orientSnapToJoint.setter
    def orientSnapToJoint(self, value:int) -> None:
        self.parm("orient_snapToJoint").set(value)

    @property
    def orientSnapToSkinPoint(self) -> int:
        return self.parm("orient_snapToSkinPoint").eval()
    
    @orientSnapToSkinPoint.setter
    def orientSnapToSkinPoint(self, value:int) -> None:
        self.parm("orient_snapToSkinPoint").set(value)

    @property
    def orientSnapToJointAxis(self) -> int:
        return self.parm("orient_snapToJointAxis").eval()
    
    @orientSnapToJointAxis.setter
    def orientSnapToJointAxis(self, value:int) -> None:
        self.parm("orient_snapToJointAxis").set(value)

    @property
    def orientRuleMainAxis(self) -> int:
        return self.parm("orient_ruleMainAxis").eval()
    
    @orientRuleMainAxis.setter
    def orientRuleMainAxis(self, value:int) -> None:
        self.parm("orient_ruleMainAxis").set(value)

    @property
    def orientRuleSecondaryAxis(self) -> int:
        return self.parm("orient_ruleSecondaryAxis").eval()
    
    @orientRuleSecondaryAxis.setter
    def orientRuleSecondaryAxis(self, value:int) -> None:
        self.parm("orient_ruleSecondaryAxis").set(value)

    @property
    def orientDisplayScale(self) -> float:
        return self.parm("orient_displayScale").eval()
    
    @orientDisplayScale.setter
    def orientDisplayScale(self, value:float) -> None:
        self.parm("orient_displayScale").set(value)
    
    # =================
    # CACHE PARAMETERS.
    # =================

    @property
    def skeletonCache(self) -> hou.Geometry:
        return self.parm("skeletonCache").eval()
    
    @skeletonCache.setter
    def skeletonCache(self, value:hou.Geometry) -> None:
        self.parm("skeletonCache").set(value)

    @property
    def toCache(self) -> hou.Node:
        return self._node.node("TO_CACHE")

    @property
    def fromCache(self) -> hou.Node:
        return self._node.node("FROM_CACHE")

    # =========================
    # DRAWABLE NODE GEOMETRIES.
    # =========================

    @property
    def constructionPlaneNode(self) -> hou.Node:
        return self.node("CONSTRUCTION_PLANE")

    @property
    def constructionPlane(self) -> hou.Geometry:
        return self.constructionPlaneNode.node("DRAWABLE_PLANE").geometry()
    
    @property
    def constructionPlaneBorder(self) -> hou.Geometry:
        return self.constructionPlaneNode.node("DRAWABLE_BORDER").geometry()
    
    @property
    def constructionPlaneLocation(self) -> hou.Geometry:
        return self.constructionPlaneNode.node("DRAWABLE_LOCATION").geometry()

    @property
    def drawableSkeletonPoints(self) -> hou.Geometry:
        return self.node("DRAWABLE_SKELETON_POINTS").geometry()

    @property
    def drawableSkeletonLines(self) -> hou.Geometry:
        return self.node("DRAWABLE_SKELETON_LINES").geometry()

    @property
    def skeletonCollision(self) -> hou.Geometry:
        return self.node("SKELETON_COLLISION").geometry()

    @property
    def drawableSkinForSelection(self) -> hou.Geometry:
        return self.node("DRAWABLE_SKIN_FOR_SELECTION").geometry()
    
    @property
    def drawableSkinCollision(self) -> hou.Geometry:
        return self.node("DRAWABLE_SKIN_COLLISION").geometry()

    @property
    def drawableSkinPoints(self) -> hou.Geometry:
        return self.node("DRAWABLE_SKIN_POINTS").geometry()

    @property
    def drawableJointOrientation(self) -> hou.Geometry:
        return self.node("DRAWABLE_JOINTS_ORIENTATION").geometry()

    @property
    def drawableOrientationHelper(self) -> hou.Geometry:
        return self.node("DRAWABLE_ORIENTATION_HELPER").geometry()

    @property
    def drawableSkeletonShapes(self) -> hou.Geometry:
        return self.node("DRAWABLE_SKELETON_SHAPES").geometry()
    

         



