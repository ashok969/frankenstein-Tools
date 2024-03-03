
import hou

from .collisionGeometry      import CollisionGeometry

class SkeletonGeometry(CollisionGeometry):

    def __init__(self, 
        geo=hou.Geometry):
        super(SkeletonGeometry, self).__init__(geo)

        # Define the private points list to optimize the recurcive loop.
        self._points = None


    def getJointChildren(self,
        jointID:int,
        childrenIDs:list[int],
        recursive:bool=False,
        multiChildrenStop:bool=False,
        recursiveDepth:int=0) -> None:
        """ Get all the children joints from the current joint.

        :param jointID: The current joint.
        :type jointID: int
        
        :param childrenIDs: The list to store the children IDs.
        :type childrenIDs: list[int]

        :param recursive: Allow to do a recurcive loop to get all the hierarchy children, defaults to False
        :type recursive: bool, optional

        :param multiChildrenStop: Allow to stop the recursion if the joint have more than one children.
        :type multiChildrenStop: bool, optional

        :param recursiveDepth: Don't use it. Just an iterative arg for know the depth of the recursion.
        :type recursiveDepth: int, optional.
        """
        
        # Optimize the recursion.
        # We get the points list of the geometry if we are at the recursion depth 0.
        if(recursiveDepth == 0):
            self._points = self._geometry.points()
            if(len(self._points) == 0):
                return 0
        
        # Get the point and its primitive to kwnow its children.
        point       = self._points[jointID]     # type: hou.Point

        # To avoid to get some parent primitive.
        # Get the point's primitive that the last point is not the current point.
        pointPrims = [prim for prim in point.prims() if prim.points()[-1].number() != jointID]

        # Ignore the point if no primtive.
        if(len(pointPrims) == 0):
            return 0
        
        # Stop the recursion if the joint have more than one child.
        if(multiChildrenStop is True and len(pointPrims) > 1):
            return 0

        # Loop over the point primitive to get the children.
        for prim in pointPrims:
            primPoints = prim.points()
            # Ignore primitive if the prim point count is greate than 2.
            if(len(primPoints) != 2):
                continue

            childID = primPoints[-1].number()

            # Ignore chid point if is already in the children ID list.
            if(childID in childrenIDs):
                continue
            
            childrenIDs.append(childID)
            
            if(recursive is True):
                self.getJointChildren(
                    childID,
                    childrenIDs,
                    recursive=recursive,
                    multiChildrenStop=multiChildrenStop,
                    recursiveDepth=recursiveDepth+1
                )
        
        # Clear the point list.
        if(recursiveDepth == 0):
            self._points = None

    def getJointName(self, 
        jointID:int) -> str:
        """ Get the joint name.

        :param jointID: The joint ID.
        :type jointID: int

        :return: The joint name.
        :rtype: str or None
        """
        # Get the point attribute.
        pointAttrib = self.findPointAttrib("name")
        if(not pointAttrib):
            return None
        
        # Get the geometry points.
        points = self.points()
        # Check if the index can be inside the geometry.
        if(jointID > len(points) - 1):
            return None
        
        return self.pointStringAttribValues("name")[jointID]
    
    def getJointPosition(self,
        jointID:int) -> hou.Vector3:
        """ Get the joint position.

        :param jointID: The joint ID.
        :type jointID: int

        :return: The joint position in 3D space.
        :rtype: hou.Vector3 or None
        """
        # Get the geometry points.
        points = self.points()
        # Check if the index can be inside the geometry.
        if(jointID > len(points) - 1):
            return None
        
        return points[jointID].position()

    def getJointIDFromName(self,
        jointName:str) -> int:
        """ Get the joint ID from its name.

        :param jointName: The joint name.
        :type jointName: str
        
        :return: The joint ID.
        :rtype: int or None
        """
        # Get the point attribute.
        pointAttrib  = self.findPointAttrib("name")
        if(not pointAttrib):
            return None
        # Loop over the joints names
        jointNames = pointAttrib.strings()
        for index, value in enumerate(jointNames):
            if(value == jointName):
                return index
            
        return None
