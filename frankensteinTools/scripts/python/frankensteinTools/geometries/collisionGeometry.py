
import hou


class CollisionGeometry(object):

    def __init__(self, geometry:hou.Geometry):

        self._geometry       = geometry

        self.hitPrimID      = -1
        self.hitPosition    = hou.Vector3()
        self.hitNormal      = hou.Vector3()
        self.hitPrimUV      = hou.Vector3() 
        self.hitPointID     = -1

    def resetHit(self):
        """ Reset the hit datas.
        """
        self.hitPrimID  = -1
        self.hitPointID = -1

    def surfaceIntersect(self,
        rayOrigin:hou.Vector3,
        rayDirection:hou.Vector3) -> bool:
        """ Get the intersected surface location.

        :param rayOrigin: The origin of the ray.
        :type rayOrigin: hou.Vector3
        
        :param rayDirection: The ray direction.
        :type rayDirection: hou.Vector3

        :return: True if intersect.
        :rtype: bool
        """
        self.resetHit()

        self.hitPrimID = self.intersect(
            rayOrigin,
            rayDirection,
            self.hitPosition,
            self.hitNormal,
            self.hitPrimUV,
        )

        if(self.hitPrimID > -1):
            toPos = self.hitPosition - rayOrigin  # type: hou.Vector3
            dist = toPos.length()

            if(dist <= 0.5):
                self.hitPrimID = self.intersect(
                    rayOrigin,
                    rayDirection,
                    self.hitPosition,
                    self.hitNormal,
                    self.hitPrimUV,
                    tolerance = 0.001
                )

        if(self.hitPrimID > -1):
            return True

        return False
    
    def pointIntersect(self,
        rayOrigin:hou.Vector3,
        rayDirection:hou.Vector3,
        radius:float,
        forceDetection:bool=False) -> bool:
        """ Get the closest point from the ray line.

        :param rayOrigin: The origin of the ray.
        :type rayOrigin: hou.Vector3
        
        :param rayDirection: The ray direction.
        :type rayDirection: hou.Vector3

        :param radius: The max radius to find points.
        :type radius: float

        :return: True if intersect, otherwise False.
        :rtype: bool
        """
        geoRayCache = hou.GeometryRayCache()
        points = geoRayCache.findAllInTube(
            geo=self._geometry,
            rayorig=rayOrigin,
            dir=rayDirection,
            radius=radius
        )

        disableAttrib = self._geometry.findPointAttrib("disable")
        disable = 0

        if(len(points) > 0):
            if(disableAttrib):
                disable = points[0].attribValue("disable")
            if(forceDetection is True):
                disable = 0
            if(disable == 0):
                self.hitPointID = points[0].number()
                return True

        self.hitPointID = -1
        return False

    def linePointIntersect(self,
        rayOrigin:hou.Vector3,
        rayDirection:hou.Vector3,
        forceDetection:bool=False) -> bool:
        """ Get the intersected point ID.

        :param rayOrigin: The origin of the ray.
        :type rayOrigin: hou.Vector3
        
        :param rayDirection: The ray direction.
        :type rayDirection: hou.Vector3

        :return: True if intersect, otherwise False.
        :rtype: bool
        """
        disableAttrib = self._geometry.findPointAttrib("disable")

        intersected = self.surfaceIntersect(rayOrigin, rayDirection)
        if(intersected is False):
            return -1
        
        rootPoint   = self.prim(self.hitPrimID).points()[0]     # type:hou.Point
        disable     = 0
        if(disableAttrib):
            disable     = rootPoint.attribValue("disable")

        if(forceDetection is True):
            disable = 0

        if(disable == 0): 
            self.hitPointID = rootPoint.number()
            if(self.hitPrimUV.x() > 0.95):
                tipPoint = self.prim(self.hitPrimID).points()[-1]
                if(disableAttrib):
                    disable = tipPoint.attribValue("disable")
                if(forceDetection is True):
                    disable = 0
                if(disable == 0):
                    self.hitPointID = tipPoint.number()

        if(self.hitPointID > -1):
            return True

        return False

    def surfacePointIntersect(self,
        rayOrigin:hou.Vector3,
        rayDirection:hou.Vector3,
        forceDetection:bool=False) -> bool:
        """ Get the intersected point ID.

        :param rayOrigin: The origin of the ray.
        :type rayOrigin: hou.Vector3
        
        :param rayDirection: The ray direction.
        :type rayDirection: hou.Vector3

        :return: True if intersect, otherwise False.
        :rtype: bool
        """

        disableAttrib = self._geometry.findPointAttrib("disable")

        intersected = self.surfaceIntersect(rayOrigin, rayDirection)
        if(intersected is False):
            return -1
        
        minDist     = 1+10
        disable     = 0
        for point in self.prim(self.hitPrimID).points():
            if(disableAttrib):
                disable     = point.attribValue("disable")
            if(forceDetection is True):
                disable = 0
            if(disable == 0):
                pointPos    = point.position()
                dist        = pointPos.distanceTo(self.hitPosition)
                if(dist < minDist):
                    minDist = dist
                    self.hitPointID = point.number()
        
        if(self.hitPointID > -1):
            return True

        return False
        
    def findPointAttrib(self, *args, **kwargs):
        return self._geometry.findPointAttrib(*args, **kwargs)
    
    def pointStringAttribValues(self, *args, **kwargs):
        return self._geometry.pointStringAttribValues(*args, **kwargs)

    def intersect(self, *args, **kwargs):
        return self._geometry.intersect(*args, **kwargs)
    
    def prim(self, primID:int) -> hou.Prim:
        return self._geometry.prim(primID)
    
    def point(self, pointID:int) -> hou.Point:
        return self._geometry.point(pointID)
    
    def points(self, *args, **kwargs) -> tuple[hou.Point]:
        return self._geometry.points(*args, **kwargs)

    def prims(self, *args, **kwargs) -> tuple[hou.Prim]:
        return self._geometry.prims(*args, **kwargs)
    
    @property
    def houGeometry(self) -> hou.Geometry:
        return self._geometry
    
    @houGeometry.setter
    def houGeometry(self, value:hou.Geometry) -> None:
        self._geometry = value
    
