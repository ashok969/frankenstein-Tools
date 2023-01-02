
import hou



class FNKUtils(object):

    def __init__(self):
        pass

    @staticmethod
    def modelToScreenSpace(sceneViewer:hou.SceneViewer, position:hou.Vector3, offset:hou.Vector3) -> hou.Vector3:
        """ Convert a posittion from the geometry space to the screen space.

        Args:
            sceneViewer (hou.SceneViewer)   : The current scene viewer.
            position    (hou.Vector3)       : The position to convert.
            offset      (hou.Vector3)       : Offset the screen position in pixel.
        
        Returns:
            hou.Vector3 : The postion in screen space.
        """
        # Convert the position from vector3 to vector4.
        pos             = hou.Vector4(position.x(), position.y(), position.z(), 1.0)
        # Get the convertion matrices from the current viewport.
        currentViewport = sceneViewer.curViewport()
        camMatrix       = currentViewport.viewTransform()
        ndcMatrix       = currentViewport.ndcToCameraTransform()
        screenSize      = currentViewport.resolutionInPixels()
        # Convert to camera then ndc space.
        camPos          = pos * camMatrix.inverted()
        ndcPos          = camPos * ndcMatrix.inverted()
        # Normalize the ndcPos.
        ndcPos[0]       = (ndcPos[0] / ndcPos[3] + 1) * 0.5
        ndcPos[1]       = (ndcPos[1] / ndcPos[3] + 1) * 0.5
        # Convert the screen space.
        return hou.Vector3(
            int(round(ndcPos[0] * float(screenSize[0]))) + offset.x(),
            int(round(ndcPos[1] * float(screenSize[1]))) + offset.y(),
            0.0
        )

    @staticmethod
    def getJointPosition(geo:hou.Geometry, jointID:int) -> hou.Vector3:
        """ Get the position of a joint in a geometry from its id.

        Args:
            geo     (hou.Geometry)  : The geometry that contrain the rig.
            jointID (int)           : The index of the joint.

        Returns:
            hou.Vector3 or None : The position of the joint.
        """
        # Get the geometry points.
        points = geo.points()
        # Check if the index can be inside the geometry.
        if(jointID < len(points) - 1):
            return points[jointID].position()
        return None
    
    @staticmethod
    def getJointName(geo:hou.Geometry, attribName:str, jointID:int) -> str:
        """ Get the name of a joint in a geometry from its id.

        Args:
            geo         (hou.Geometry)  : The geometry that contain the rig.
            attribName  (str)           : The point attrbiute that contain the joint name.
            jointID     (int)           : the index of the joint.
        
        Returns:
            str or None : The name of the joint.
        """
        # Get the point attribute.
        pointAttrib = geo.findPointAttrib(attribName)
        if(pointAttrib):
            # Get the geometry points.
            points = geo.points()
            # Check if the index can be inside the geometry.
            if(jointID < len(points) - 1):
                return pointAttrib.strings()[jointID]
        return None

    @staticmethod
    def getJointID(geo:hou.Geometry, attribName:str, jointName:str) -> int:
        """ Get the id of the joint from its name.

        Args:
            geo         (hou.Geometry)  : The geometry that contain the rig.
            attribName  (str)           : The name of the joint to find.
            jointName   (str)           : The name of the joint.
        
        Returns:
            int or None : The index of the joint.
        """
        # Get the point attribute.
        pointAttrib  = geo.findPointAttrib(attribName)
        if(pointAttrib):
            jointNames = pointAttrib.strings()
            for index, value in enumerate(jointNames):
                if(value == jointName):
                    return index
        
        return None