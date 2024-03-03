
import hou

from frankensteinTools.geometries   import SkeletonGeometry
from frankensteinTools              import FNKUtils

class DrawableSkeleton(object):

    def __init__(self, 
        stateName:str, 
        sceneViewer:hou.SceneViewer,
        baseName:str):

        self.stateName             = stateName
        self.sceneViewer           = sceneViewer

        # Define the geometries.
        self.geometryCollision      = SkeletonGeometry()
        self._geometryJointLines    = hou.Geometry()
        self._geometryJointPoints   = hou.Geometry()
        self._geometryJointShapes   = hou.Geometry()

        # Define the drawable object to display the skeleton.
        self.drawableJointPoints    = hou.GeometryDrawable(
            self.sceneViewer,
            hou.drawableGeometryType.Point,
            "{}_jointPoints".format(baseName),
            params={
                "color1"        : hou.Vector4(1.0, 1.0, 1.0, 1.0),
                "radius"        : 8,
                "style"         : hou.drawableGeometryPointStyle.SmoothCircle,
                "use_cd"        : True,
                "fade_factor"   : 1.0
            }    
        )

        self.drawableJointLines     = hou.GeometryDrawable(
            self.sceneViewer,
            hou.drawableGeometryType.Line,
            "{}_jointLines".format(baseName),
            params={
                "color1"        : hou.Vector4(1.0, 1.0, 1.0, 1.0),
                "line_width"    : 2,
                "style"         : hou.drawableGeometryLineStyle.Plain,
                "use_cd"        : True,
                "fade_factor"   : 1.0
            }
        )

        self.drawableJointShapes    = hou.GeometryDrawable(
            self.sceneViewer,
            hou.drawableGeometryType.Face,
            "{}_jointShapes".format(baseName),
            params={
                "color1"        : hou.Vector4(1.0, 1.0, 1.0, 0.3),
                "use_cd"        : True,
                "style"         : hou.drawableGeometryFaceStyle.Plain,
                "fade_factor"   : 1.0
            }
        )
 
        self.drawableJointRing      = hou.GeometryDrawable(
            self.sceneViewer,
            hou.drawableGeometryType.Point,
            "{}_jointRing".format(baseName),
            params={
                "color1"        : hou.Vector4(1.0, 1.0, 1.0, 1.0),
                "use_cd"        : False,
                "style"         : hou.drawableGeometryPointStyle.Ring,
                "fade_factor"   : 1.0,
                "radius"        : 5
            }
        )

        self.drawableJointName      = hou.TextDrawable(
            self.sceneViewer,
            "{}_jointName".format(baseName),
            params={
                "color1"    : hou.Color(1.0, 1.0, 1.0),
                "origin"    : hou.drawableTextOrigin.LeftCenter,
            }
        )

        # Define the variable to store the differents geometries to display.
        self._jointName             = ""
        self._jointID               = -1
        self._jointNameScreenPos    = hou.Vector3()


    def setDraw(self, handle) -> None:
        """ Set the joint name to display.

        Args:
            handle  () : The drawable handle.
        """
        # Define the diplay order of the drawables.
        #self.drawableJointLines.draw(handle)
        #self.drawableJointPoints.draw(handle)
        self.drawableJointRing.draw(handle)
        self.drawableJointShapes.draw(handle)

        params = {
            "text"      : "<font size=5><b>{}</b></font>".format(self._jointName),
            "translate" : self._jointNameScreenPos,
        }

        self.drawableJointName.draw(handle, params)

    def onDraw(self, kwargs):
        
        self.setDraw(kwargs["draw_handle"])

    def onDrawInterrupt(self, kwargs):
   
        self.jointHighlight()
        self.setDraw(kwargs["draw_handle"])

    def showSkeletonJoints(self) -> None:

        self.drawableJointPoints.show(True)
        self.drawableJointLines.show(True)

    def hideSkeletonJoints(self) -> None:

        self.drawableJointPoints.show(False)
        self.drawableJointLines.show(False)

    def showSkeletonShapes(self) -> None:

        self.drawableJointShapes.show(True)

    def hideSkeletonShapes(self) -> None:

        self.drawableJointShapes.show(False)

    def showJoint(self) -> None:

        self.drawableJointRing.show(True)
        self.drawableJointName.show(True)

    def hideJoint(self) -> None:

        self.drawableJointRing.show(False)
        self.drawableJointName.show(False)

    def jointHighlight(self,
        jointID:int=None) -> None:
        """ Use the joint ID to create the geometry for joint highlight ring.

        :param jointID: The joint ID or None. If None we use the previous stored joint ID
        :type jointID: int, optional
        """
        # Store the joint ID to reuse it when we are in Interrup Draw.
        if(jointID is not None):
            self._jointID = jointID

        geometry            = hou.Geometry()
        self._jointName     = ""    

        # Reset the drawable joint ring geometry if joint ID is -1.
        if(self._jointID == -1):
            self.drawableJointRing.setGeometry(geometry)
            self.hideJoint()
            return None
        
        # Get the joint point and extract the datas for the joint name and geometry.
        point                       = self.geometryCollision.point(self._jointID)  # type: hou.Point
        if(jointID is None):
            point                   = self.geometryJointPoints.point(self._jointID)  # type: hou.Point
        jointPos                    = point.position()
        self._jointName             = point.attribValue("name")
        self._jointNameScreenPos    = FNKUtils.modelToScreenSpace(
            self.sceneViewer,
            jointPos,
            hou.Vector3(10, 10, 0)
        )
        geoPoint    = geometry.createPoint()    # type: hou.Point
        geoPoint.setPosition(jointPos)
        self.drawableJointRing.setGeometry(geometry)
        self.showJoint()

    def findJoint(self,
        rayOrigin:hou.Vector3,
        rayDirection:hou.Vector3,
        maxRadius:float,
        forceDetection:bool=False) -> int:

        self.geometryCollision.linePointIntersect(rayOrigin, rayDirection, forceDetection=forceDetection)
        if(self.geometryCollision.hitPointID == -1):
            self.geometryCollision.pointIntersect(rayOrigin, rayDirection, maxRadius, forceDetection=forceDetection)

        self.jointHighlight(jointID=self.geometryCollision.hitPointID)

        return self.geometryCollision.hitPointID

    def showGeometry(self) -> None:
        self.showSkeletonShapes()
        self.showSkeletonJoints()

    def hideGeometry(self) -> None:
        self.hideSkeletonShapes()
        self.hideSkeletonJoints()


    @property
    def geometryJointPoints(self) -> hou.Geometry:
        return self._geometryJointPoints

    @geometryJointPoints.setter
    def geometryJointPoints(self, value:hou.Geometry) -> None:
        self._geometryJointPoints = value
        self.drawableJointPoints.setGeometry(value)

    @property
    def geometryJointLines(self) -> hou.Geometry:
        return self._geometryJointLines
    
    @geometryJointLines.setter
    def geometryJointLines(self, value:hou.Geometry) -> None:
        self._geometryJointLines = value
        self.drawableJointLines.setGeometry(value)

    @property
    def geometryJointShapes(self) -> hou.Geometry:
        return self._geometryJointShapes
    
    @geometryJointShapes.setter
    def geometryJointShapes(self, value:hou.Geometry) -> None:
        self._geometryJointShapes = value
        self.drawableJointShapes.setGeometry(value)
