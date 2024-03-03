
import hou
import math
import viewerstate.utils as vs

from  frankensteinTools.geometries    import CollisionGeometry

class DrawableSkin(object):

    def __init__(self, 
        stateName:str, 
        sceneViewer:hou.SceneViewer,
        baseName:str):

        self.stateName             = stateName
        self.sceneViewer           = sceneViewer

        self._geometry              = hou.Geometry()
        self._geometryPoints        = hou.Geometry()

        self.drawableGeometry     = hou.GeometryDrawable(
            self.sceneViewer,
            hou.drawableGeometryType.Face,
            "{}_geometry".format(baseName),
            params={
                "use_cd"        : True,
                "color1"        : hou.Vector4(1.0, 1.0, 1.0, 0.4),
                "style"         : hou.drawableGeometryFaceStyle.Plain,
                "fade_factor"   : 0.0
            }
        )

        self.drawableGeometryLines = hou.GeometryDrawable(
            self.sceneViewer,
            hou.drawableGeometryType.Line,
            "{}_geometryLines".format(baseName),
            params={
                "use_cd"        : True,
                "color1"        : hou.Vector4(1.0, 1.0, 1.0, 0.8),
                "style"         : hou.drawableGeometryLineStyle.Plain,
                "fade_factor"   : 0.0,
                "line_width"    : 1
            }    
        )

        self.drawablePoints     = hou.GeometryDrawable(
            self.sceneViewer,
            hou.drawableGeometryType.Point,
            "{}_geometryPoint".format(baseName),
            params={
                "use_cd"        : True,
                "color1"        : hou.Vector4(1.0, 1.0, 1.0, 1.0),
                "style"         : hou.drawableGeometryPointStyle.SmoothCircle,
                "radius"        : 5,
                "fade_factor"   : 1.0
            }
        )


    def setDraw(self, handle) -> None:
        """ Set the joint name to display.

        Args:
            handle  () : The drawable handle.
        """
        self.drawablePoints.draw(handle)
        self.drawableGeometry.draw(handle)
        self.drawableGeometryLines.draw(handle)

    def onDraw(self, kwargs):
        self.setDraw(kwargs["draw_handle"])

    def onDrawInterrupt(self, kwargs):
        self.setDraw(kwargs["draw_handle"])

    def showGeometry(self):
        self.drawableGeometry.show(True)
        self.drawableGeometryLines.show(True)

    def hideGeometry(self):
        self.drawableGeometry.show(False)
        self.drawableGeometryLines.show(False)

    def showGeometryPoints(self):
        self.drawablePoints.show(True)

    def hideGeometryPoints(self):
        self.drawablePoints.show(False)

    def findGeometryPath(self,
        rayOrigin:hou.Vector3,
        rayDirection:hou.Vector3) -> str:
        """ Find the geometry path.

        :param rayOrigin: The ray origin.
        :type rayOrigin: hou.Vector3

        :param rayDirection: The ray direction.
        :type rayDirection: hou.Vector3
        
        :return: The path of the skin geometry.
        :rtype: str
        """

        self._geometry.surfaceIntersect(rayOrigin, rayDirection)

        if(self._geometry.hitPrimID > -1):
            prim = self._geometry.prim(self._geometry.hitPrimID)    # type: hou.Prim
            return prim.attribValue("path")

        return ""

    def findPoint(self,
        rayOrigin:hou.Vector3,
        rayDirection:hou.Vector3) -> int:
        """ Find the geometry point.

        :param rayOrigin: The ray origin.
        :type rayOrigin: hou.Vector3

        :param rayDirection: The ray direction.
        :type rayDirection: hou.Vector3

        :return: The point index under the ray or -1.
        :rtype: int
        """
        self._geometry.surfacePointIntersect(rayOrigin, rayDirection)
        return self._geometry.hitPointID

    @property
    def geometry(self) -> CollisionGeometry:
        return self._geometry
    
    @geometry.setter
    def geometry(self, value:CollisionGeometry) -> None:
        self._geometry      = value
        self.drawableGeometry.setGeometry(value.houGeometry)
        self.drawableGeometryLines.setGeometry(value.houGeometry)

    @property
    def pointsGeometry(self) -> hou.Geometry:
        return self._geometryPoints

    @pointsGeometry.setter
    def pointsGeometry(self, value:hou.Geometry) -> None:
        self._geometryPoints = value
        self.drawablePoints.setGeometry(value)