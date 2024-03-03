
import hou

from frankensteinTools.geometries       import CollisionGeometry

class DrawableConstructionPlane(object):

    def __init__(self, 
        stateName:str, 
        sceneViewer:hou.SceneViewer,
        baseName:str):

        self.stateName              = stateName
        self.sceneViewer            = sceneViewer

        self.planeColor             = hou.Vector4(1.0, 1.0, 1.0, 0.1)
        self.planeWireColor         = hou.Vector4(1.0, 1.0, 1.0, 0.5)
        self.planeLocationColor     = hou.Vector4(1.0, 1.0, 1.0, 0.8)

        self._planeGeometry         = hou.Geometry()
        self._locationGeometry      = hou.Geometry()
        self._borderGeometry        = hou.Geometry()

        self.drawablePlane          = hou.GeometryDrawable(
            self.sceneViewer,
            hou.drawableGeometryType.Face,
            "{}_plane".format(baseName),
            params={
                "color1"        : self.planeColor,
                "style"         : hou.drawableGeometryFaceStyle.Plain,
                "use_cd"        : True,
                "fade_factor"   : 0.5,
            }
        )

        self.drawablePlaneWire      = hou.GeometryDrawable(
            self.sceneViewer,
            hou.drawableGeometryType.Line,
            "{}_wire".format(baseName),
            params={
                "color1"        : self.planeWireColor,
                "style"         : hou.drawableGeometryLineStyle.Plain,
                "fade_factor"   : 0.5,
                "use_cd"        : True,
                "line_width"    : 1
            }
        )

        self.drawablePlaneBorder    = hou.GeometryDrawable(
            self.sceneViewer,
            hou.drawableGeometryType.Line,
            "{}_border".format(baseName),
            params={
                "color1"        : self.planeLocationColor,
                "style"         : hou.drawableGeometryLineStyle.Plain,
                "fade_factor"   : 0.5,
                "use_cd"        : True,
                "line_width"    : 4
            }
        )

        self.drawablePlaneLocation  = hou.GeometryDrawable(
            self.sceneViewer,
            hou.drawableGeometryType.Line,
            "{}_location".format(baseName),
            params={
                "color1"        : self.planeLocationColor,
                "style"         : hou.drawableGeometryLineStyle.Dash2,
                "fade_factor"   : 0.5,
                "use_cd"        : True,
                "line_width"    : 3
            }
        )


    def setDraw(self, drawHandle) -> None:

        self.drawablePlaneBorder.draw(drawHandle)
        self.drawablePlaneWire.draw(drawHandle)
        self.drawablePlaneLocation.draw(drawHandle)
        self.drawablePlane.draw(drawHandle)

    def onDraw(self, kwargs) -> None:

        self.setDraw(kwargs["draw_handle"])

    def onDrawInterrupt(self, kwargs) -> None:

        self.setDraw(kwargs["draw_handle"])

    def showPlane(self) -> None:

        self.drawablePlane.show(True)
        self.drawablePlaneWire.show(True)
        self.drawablePlaneLocation.show(True)
        self.drawablePlaneBorder.show(True)
    
    def hidePlane(self) -> None:

        self.drawablePlane.show(False)
        self.drawablePlaneWire.show(False)
        self.drawablePlaneLocation.show(False)
        self.drawablePlaneBorder.show(False)

    @property
    def planeGeometry(self) -> CollisionGeometry:
        return self._planeGeometry
    
    @planeGeometry.setter
    def planeGeometry(self, value:CollisionGeometry) -> None:

        self._planeGeometry = value
        self.drawablePlane.setGeometry(value.houGeometry)
        self.drawablePlaneWire.setGeometry(value.houGeometry)

    @property
    def locationGeometry(self) -> CollisionGeometry:
        return self._locationGeometry
    
    @locationGeometry.setter
    def locationGeometry(self, value:CollisionGeometry) -> None:

        self._locationGeometry = value
        self.drawablePlaneLocation.setGeometry(value.houGeometry)
    
    @property
    def borderGeometry(self) -> CollisionGeometry:
        return self._borderGeometry
    
    @borderGeometry.setter
    def borderGeometry(self, value:CollisionGeometry) -> None:
        self._borderGeometry = value
        self.drawablePlaneBorder.setGeometry(value.houGeometry)