
import hou

from frankensteinTools.geometries       import CollisionGeometry

class DrawableAxis(object):

    def __init__(self, 
        stateName:str, 
        sceneViewer:hou.SceneViewer,
        baseName:str):

        self.stateName              = stateName
        self.sceneViewer            = sceneViewer

        self._geometry              = hou.Geometry()
        self._helperGeometry        = hou.Geometry()

        self.drawableGeometry       = hou.GeometryDrawable(
            self.sceneViewer,
            hou.drawableGeometryType.Line,
            "{}_axis".format(baseName),
            params={
                "line_width"    : 3,
                "use_cd"        : True,
                "style"         : hou.drawableGeometryLineStyle.Plain,
                "fade_factor"   : 1.0,
                "color1"        : hou.Vector4(1.0, 1.0, 1.0, 1.0)
            }
        )

        self.drawableHelper         = hou.GeometryDrawable(
            self.sceneViewer,
            hou.drawableGeometryType.Line,
            "{}.axisHelper".format(baseName),
            params={
                "line_width"    : 5,
                "use_cd"        : True,
                "style"         : hou.drawableGeometryLineStyle.Dash1,
                "fade_factor"   : 1.0,
                "color1"        : hou.Vector4(1.0, 1.0, 1.0, 1.0)
            }
        )

    def setDraw(self, drawHandle) -> None:

        self.drawableGeometry.draw(drawHandle)
        self.drawableHelper.draw(drawHandle)

    def onDraw(self, kwargs):

        self.setDraw(kwargs["draw_handle"])

    def onDrawInterrupt(self, kwargs) -> None:

        self.setDraw(kwargs["draw_handle"])

    def showGeometry(self) -> None:

        self.drawableGeometry.show(True)

    def hideGeometry(self) -> None:

        self.drawableGeometry.show(False)

    def showHelper(self) -> None:

        self.drawableHelper.show(True)

    def hideHelper(self) -> None:

        self.drawableHelper.show(False)

    def findAxis(self,
        rayOrigin:hou.Vector3,
        rayDirection:hou.Vector3) -> None:

        self._geometry.surfaceIntersect(rayOrigin, rayDirection)

        if(self._geometry.hitPrimID > -1):
            prim = self._geometry.prim(self._geometry.hitPrimID)
            locked = prim.attribValue("locked")
            if(locked == 1):
                self._geometry.hitPrimID    = -1
                self._geometry.hitPointID   = -1

    @property
    def geometry(self) -> CollisionGeometry:
        return self._geometry

    @geometry.setter
    def geometry(self, value: CollisionGeometry) -> None:
        self._geometry = value
        self.drawableGeometry.setGeometry(value.houGeometry)

    @property
    def helperGeometry(self) -> CollisionGeometry:
        return self._helperGeometry

    @helperGeometry.setter
    def helperGeometry(self, value:CollisionGeometry) -> None:
        self._helperGeometry = value
        self.drawableHelper.setGeometry(value.houGeometry)