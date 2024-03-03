
import hou
import math
import viewerstate.utils as vs




class FNKBrushDrawable(object):

    def __init__(self, stateName, sceneViewer):

        self.stateName      = stateName
        self.sceneViewer    = sceneViewer

        self.innerSize      = 0.1
        self.outerSize      = 0.2
        self.innerColor     = hou.Color(0.8, 0.0, 0.0)
        self.outerColor     = hou.Color(1.0, 0.0, 0.0)


        geo     = hou.Geometry()
        verb    = hou.sopNodeTypeCategory().nodeVerb("circle")
        verb.setParms(
            {
                "type"  : 1,
                "divs"  : 50
            }
        )

        verb.execute(geo, [])


        geoPoint = hou.Geometry()
        geoPoint.createPoint()

        self.centerBrush = hou.GeometryDrawable(
            sceneViewer,
            hou.drawableGeometryType.Point,
            stateName + "_brushCenter"
        )
        self.centerBrush.setGeometry(geoPoint)
        self.centerBrush.setParams(
            {
                "color1"        : self.innerColor,
                "fade_factor"   : 1.0,
                "radius"        : 5,
                "style"         : hou.drawableGeometryPointStyle.LinearSquare,
            }
        )
        

        self.innerBrush = hou.GeometryDrawable(
            sceneViewer,
            hou.drawableGeometryType.Line,
            stateName + "_brushInner"
        )

        self.innerBrush.setParams(
            {
                "color1"        : self.innerColor,
                "fade_factor"   : 1.0,
                "line_width"    : 1,
                "style"         : hou.drawableGeometryLineStyle.Dash2,

            }
        )

        self.outerBrush = hou.GeometryDrawable(
            sceneViewer,
            hou.drawableGeometryType.Line,
            stateName + "_brushOuter"
        )

        self.outerBrush.setParams(
            {
                "color1"        : self.outerColor,
                "fade_factor"   : 1.0,
                "line_width"    : 2,
            }
        )

        self.innerBrush.setGeometry(geo)
        self.outerBrush.setGeometry(geo)


    def transformFromRayDatas(self, position:hou.Vector3, normal:hou.Vector3) -> None:
        """ Compute the inner and outer transform from the ray projection datas.
            For the scale of the transform we use the inner and outer size.
            We need to assign their value before using this function.

        Args:
            position    (hou.Vector3)   : The position of the ray intersection.
            normal      (hou.Vector3)   : The normal of the ray intersection face.
        """
        axisY               = hou.Vector3(0.0, 0.0, 1.0)

        rotAngle            = math.degrees(math.acos(axisY.dot(normal)))
        rotAxis             = axisY.cross(normal)
        rotAxis             = rotAxis.normalized()

        mainTransform       = hou.hmath.buildRotateAboutAxis(rotAxis, rotAngle)
        positionOffseted    = position + normal * 0.001
        mainTransform.setAt(3,0,positionOffseted.x())
        mainTransform.setAt(3,1,positionOffseted.y())
        mainTransform.setAt(3,2,positionOffseted.z())

        self.centerBrush.setTransform(mainTransform)

        innerTransform = self.setMatrixScale(mainTransform, self.innerSize)
        outerTransform = self.setMatrixScale(mainTransform, self.outerSize)

        self.innerBrush.setTransform(innerTransform)
        self.outerBrush.setTransform(outerTransform)

    def enable(self) -> None:
        self.innerBrush.enable(True)
        self.outerBrush.enable(True)

    def disable(self) -> None:
        self.innerBrush.enable(False)
        self.outerBrush.enable(False)

    def hide(self) -> None:
        self.innerBrush.show(False)
        self.outerBrush.show(False)
        self.centerBrush.show(False)

    def show(self) -> None:
        self.innerBrush.show(True)
        self.outerBrush.show(True)
        self.centerBrush.show(True)

    def setColor(self, innerColor:hou.Color, outerColor:hou.Color) -> None:
        """ Set the wireframe color of the inner and outer brush.

        Args:
            innerColor  (hou.Color) : The inner color.
            outerColor  (hou.Color) : The outer color.
        """
        self.innerBrush.setWireframeColor(innerColor)
        self.outerBrush.setWireframeColor(outerColor)

    def getTransform(self) -> hou.Matrix4:
        return self.innerBrush.transform()

    def setTransform(self, transform:hou.Matrix4) -> None:
        self.innerBrush.setTransform(transform)
        self.outerBrush.setTransform(transform)
        self.centerBrush.setTransform(transform)

    def setMatrixScale(self, matrix:hou.Matrix4, scale:float) -> hou.Matrix4:
        """ Set the scale in a matrix 4.

        Args:
            matrix  (hou.Matrix4)   : The orginal matrix to scale.
            scale   (float)         : The scale value to set in the matrix.

        Returns:
            hou.Matrix4 : The updated matrix with scale.
        """

        axisX = hou.Vector3(matrix.at(0,0), matrix.at(0,1), matrix.at(0,2))
        axisY = hou.Vector3(matrix.at(1,0), matrix.at(1,1), matrix.at(1,2))
        axisZ = hou.Vector3(matrix.at(2,0), matrix.at(2,1), matrix.at(2,2))

        axisX = axisX.normalized() * scale
        axisY = axisY.normalized() * scale
        axisZ = axisZ.normalized() * scale

        transform = hou.Matrix4()

        transform.setAt(0,0,axisX.x())
        transform.setAt(0,1,axisX.y())
        transform.setAt(0,2,axisX.z())
        transform.setAt(0,3,0.0)

        transform.setAt(1,0,axisY.x())
        transform.setAt(1,1,axisY.y())
        transform.setAt(1,2,axisY.z())
        transform.setAt(1,3,0.0)

        transform.setAt(2,0,axisZ.x())
        transform.setAt(2,1,axisZ.y())
        transform.setAt(2,2,axisZ.z())
        transform.setAt(2,3,0.0)

        transform.setAt(3,0,matrix.at(3,0))
        transform.setAt(3,1,matrix.at(3,1))
        transform.setAt(3,2,matrix.at(3,2))
        transform.setAt(3,3,1.0)

        return transform


    def onDraw(self, kwargs):
        
        handle = kwargs["draw_handle"]

        self.centerBrush.draw(handle)
        self.innerBrush.draw(handle)
        self.outerBrush.draw(handle)

    def onDrawInterrupt(self, kwargs):
   
        handle = kwargs["draw_handle"]

        self.centerBrush.draw(handle)
        self.innerBrush.draw(handle)
        self.outerBrush.draw(handle)

    '''
    @property
    def innerSize(self) -> float:
        return self.innerSize
    
    @innerSize.setter
    def innerSize(self, value:float) -> None:
        self.innerSize = value
        #scaledTransform = self.setMatrixScale(self.innerBrush.transform(), self.innerSize)
        #self.innerBrush.setTransform(scaledTransform)

    @property
    def outerSize(self) -> float:
        return self.outerSize

    @outerSize.setter
    def outerSize(self, value:float) -> None:
        self.outerSize = value
        #scaledTransform = self.setMatrixScale(self.outerBrush.transform(), self.outerSize)
        #self.outerBrush.setTransform(scaledTransform)
    '''