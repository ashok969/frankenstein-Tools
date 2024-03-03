
import hou

from frankensteinTools.nodes                                    import SkeletonBuilderNode
from frankensteinTools.drawables                                import DrawableSkeleton
from frankensteinTools.drawables                                import DrawableSkin
from frankensteinTools.viewerStates                             import BaseEvent
from frankensteinTools.viewerStates.skeletonBuilder.constants   import SkeletonToolState
from frankensteinTools.viewerStates.skeletonBuilder.constants   import SkeletonSelectionType

class SelectJointEvent(BaseEvent):

    def __init__(self, viewerStates):
        super(SelectJointEvent, self).__init__(viewerStates)

    def selectJoint(self,
        uiEvent:hou.ViewerEvent) -> bool:
        """ Handle the joint selection behavior.
        """
        # Get the ray projection data.
        rayOrigin, rayDirection = uiEvent.ray()
        # Get the device and reason from the ui event.
        device  = uiEvent.device()      # type: hou.UIEventDevice 
        reason  = uiEvent.reason()      # type: hou.uiEventReason 

        node                = self.viewerStates.node                # type: SkeletonBuilderNode
        skeletonDrawable    = self.viewerStates.skeletonDrawable    # type: DrawableSkeleton
        sceneViewer         = self.viewerStates.sceneViewer         # type: hou.SceneViewer

        selection = []
        with(hou.undos.disabler()):
            jointID = skeletonDrawable.findJoint(rayOrigin, rayDirection, 0.005, forceDetection=True)
            node.vsJointHighlight = jointID

        if(skeletonDrawable.geometryCollision.hitPointID > -1):
            selection.append(skeletonDrawable.geometryCollision.hitPointID)

        if(reason == hou.uiEventReason.Picked):
            self.viewerStates.ignoreJointRename = True
            #sceneViewer.beginStateUndo("skeletionBuilder_selectJoints")

            if(device.isLeftButton() is True):
                if(device.isShiftKey() is True):
                    node.addToSelectedJointIDs(selection)            
                elif(device.isCtrlKey() is True):
                    node.removeFromJointIDs(selection)
                else:
                    node.vsJointSelection = selection

            node.updateJointsNameFromSelection()
            #sceneViewer.endStateUndo()
            self.viewerStates.ignoreJointRename = False


        if(reason == hou.uiEventReason.Start):
            self.viewerStates.ignoreJointRename = True
            #sceneViewer.beginStateUndo("skeletionBuilder_selectJoints")
            if(device.isLeftButton() is True):

                self.selectionBehavior = 0
                if(device.isShiftKey() is True):
                    self.selectionBehavior = 1                
                elif(device.isCtrlKey() is True):
                    self.selectionBehavior = 2


        if(reason == hou.uiEventReason.Changed):
            if(self.selectionBehavior == 0):
                node.vsJointSelection = selection
            elif(self.selectionBehavior == 1):
                node.addToSelectedJointIDs(selection)
            elif(self.selectionBehavior == 2):
                node.removeFromJointIDs(selection)

            node.updateJointsNameFromSelection()
            #sceneViewer.endStateUndo()
            self.viewerStates.ignoreJointRename = False

        if(reason == hou.uiEventReason.Active):
            with(hou.undos.disabler()):
                if(device.isLeftButton() is True):
                    if(self.selectionBehavior == 0):
                        node.vsJointSelection = selection
                    elif(self.selectionBehavior == 1):
                        node.addToSelectedJointIDs(selection)
                    elif(self.selectionBehavior == 2):
                        node.removeFromJointIDs(selection)



    def selectSkin(self,
        uiEvent:hou.ViewerEvent) -> bool:
        """ Handle the skin selection behavior.
        """

        # Get the ray projection data.
        rayOrigin, rayDirection = uiEvent.ray()
        # Get the device and reason from the ui event.
        device  = uiEvent.device()      # type: hou.UIEventDevice 
        reason  = uiEvent.reason()      # type: hou.uiEventReason 

        node                = self.viewerStates.node                # type: SkeletonBuilderNode
        skinDrawable        = self.viewerStates.skinSelectionDrawable        # type: DrawableSkin
        sceneViewer         = self.viewerStates.sceneViewer         # type: hou.SceneViewer

        selection = []
        with(hou.undos.disabler()):
            skinPath = skinDrawable.findGeometryPath(rayOrigin, rayDirection)
            selection.append(skinPath)
            node.vsSkinHighlight = skinPath

        if(reason == hou.uiEventReason.Picked):
            #sceneViewer.beginStateUndo("skeletionBuilder_selectSkin")

            if(device.isLeftButton() is True):
                if(device.isShiftKey() is True):
                    node.addSkinToSelection(selection)            
                elif(device.isCtrlKey() is True):
                    node.removeSkinFromSelection(selection)
                else:
                    node.vsSkinSelection = selection

            #sceneViewer.endStateUndo()

        if(reason == hou.uiEventReason.Start):
            #sceneViewer.beginStateUndo("skeletionBuilder_selectSkin")

            if(device.isLeftButton() is True):
                self.selectionBehavior = 0
                if(device.isShiftKey() is True):
                    self.selectionBehavior = 1
                elif(device.isCtrlKey() is True):
                    self.selectionBehavior = 2

        if(reason == hou.uiEventReason.Changed):
            
            if(self.selectionBehavior == 0):
                node.vsSkinSelection = selection
            elif(self.selectionBehavior == 1):
                node.addSkinToSelection(selection)
            elif(self.selectionBehavior == 2):
                node.removeSkinFromSelection(selection)

            #sceneViewer.endStateUndo()

        if(reason == hou.uiEventReason.Active):
            with(hou.undos.disabler()):
                if(device.isLeftButton() is True):
                    if(self.selectionBehavior == 0):
                        node.vsSkinSelection = selection
                    elif(self.selectionBehavior == 1):
                        node.addSkinToSelection(selection)
                    elif(self.selectionBehavior == 2):
                        node.removeSkinFromSelection(selection)



    def mouseEvent(self,
        uiEvent:hou.ViewerEvent):
        """ Call in onMouseEvent. 
        """

        node                = self.viewerStates.node                # type: SkeletonBuilderNode
        if(node.selectionType == SkeletonSelectionType.Joint):
            self.selectJoint(uiEvent)
            return False
        if(node.selectionType == SkeletonSelectionType.Skin):
            self.selectSkin(uiEvent)
            return False

    def keyEvent(self,
        uiEvent:hou.ViewerEvent):
        """ Call in onKeyEvent.
        """
        device  = uiEvent.device()          # type: hou.UIEventDevice
        reason  = uiEvent.reason()          # type: hou.uiEventReason

        node        = self.viewerStates.node    # type: SkeletonBuilderNode
        sceneViewer = self.viewerStates.sceneViewer         # type: hou.SceneViewer

        if(device.keyString() == "b"):
            #sceneViewer.beginStateUndo("skeletonBuilder_selectJoint_BKey")
            if(node.selectionHierarchyBehavior == 0):
                node.selectionHierarchyBehavior = 1
                #sceneViewer.endStateUndo()
                return True
            if(node.selectionHierarchyBehavior == 1):
                node.selectionHierarchyBehavior = 0
                #sceneViewer.endStateUndo()
                return True
            sceneViewer.endStateUndo()

        if(device.keyString() == "f"):
            node.selectionType = SkeletonSelectionType.Joint
            return True
        
        if(device.keyString() == "g"):
            node.selectionType = SkeletonSelectionType.Skin
            return True

        return False

    def mouseDoubleClickEvent(self,
        uiEvent:hou.ViewerEvent):
        """ Call in onMouseEvent. 
        """
        device  = uiEvent.device()

        node                = self.viewerStates.node                # type: SkeletonBuilderNode
        skeletonDrawable    = self.viewerStates.skeletonDrawable    # type: DrawableSkeleton
        sceneViewer         = self.viewerStates.sceneViewer         # type: hou.SceneViewer

        self.viewerStates.ignoreJointRename = True

        if(device.isLeftButton() is True):
            #sceneViewer.beginStateUndo("skeletonBuilder_selectJointDoubleClick")
            jointID = skeletonDrawable.geometryCollision.hitPointID
            if(jointID == -1):
                #sceneViewer.endStateUndo()
                return False
            selectedIDs = [jointID]

            multiChildrenStop = False
            if(node.selectionHierarchyBehavior == 1):
                multiChildrenStop = True

            skeletonDrawable.geometryCollision.getJointChildren(
                jointID, 
                selectedIDs, 
                recursive=True, 
                multiChildrenStop=multiChildrenStop)

            if(device.isShiftKey() is True):
                node.addToSelectedJointIDs(selectedIDs)
            
            elif(device.isCtrlKey() is True):
                node.removeFromJointIDs(selectedIDs)
            else:
                node.vsJointSelection = selectedIDs

            node.updateJointsNameFromSelection()
            self.viewerStates.ignoreJointRename = False
            #sceneViewer.endStateUndo()
            return False
                
        self.viewerStates.ignoreJointRename = False
