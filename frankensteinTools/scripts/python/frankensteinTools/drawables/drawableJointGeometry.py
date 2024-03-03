
import hou

from frankensteinTools.geometries       import CollisionGeometry
from frankensteinTools.geometries       import SkeletonGeometry

class DrawableJointGeometry(object):

    def __init__(self, 
        stateName:str, 
        sceneViewer:hou.SceneViewer,
        geometryType:hou.drawableGeometryType,
        baseName:str,
        params:dict):

        self.stateName              = stateName
        self.sceneViewer            = sceneViewer

        self._defaultGeometry       = hou.Geometry()
        self._highlightGeometry     = hou.Geometry()
        self._selectedGeometry      = hou.Geometry()

        self.drawableDefault        = hou.GeometryDrawable(
            self.sceneViewer,
            geometryType,
            "{}_default".format(baseName)
        )
        if("default" in params):
            self.drawableDefault.setParams(params["default"])

        self.drawableHighlight      = hou.GeometryDrawable(
            self.sceneViewer,
            geometryType,
            "{}_highlight".format(baseName)
        )
        if("highlight" in params):
            self.drawableHighlight.setParams(params["highlight"])

        self.drawableSelected       = hou.GeometryDrawable(
            self.sceneViewer,
            geometryType,
            "{}._selected".format(baseName)
        )
        if("selected" in params):
            self.drawableSelected.setParams(params["selected"])

    def setDraw(self, drawHandle) -> None:

        self.drawableDefault.draw(drawHandle)
        self.drawableSelected.draw(drawHandle)
        self.drawableHighlight.draw(drawHandle)

    def onDraw(self, **kwargs) -> None:

        self.setDraw(kwargs["draw_handle"])

    def onDrawInterrupt(self, kwargs) -> None:

        self.setDraw(kwargs["draw_handle"])

    def showDefault(self) -> None:
        
        self.drawableDefault.show(True)
    
    def showHighlight(self) -> None:

        self.drawableHighlight.show(True)

    def showSelected(self) -> None:

        self.drawableSelected.show(True)

    def hideDefault(self) -> None:

        self.drawableDefault.show(False)
    
    def hideHighlight(self) -> None:

        self.drawableHighlight.show(False)
    
    def hideSelected(self) -> None:

        self.drawableSelected.show(False)

    def hide(self) -> None:

        self.drawableDefault.show(False)
        self.drawableSelected.show(False)
        self.drawableHighlight.show(False)

    def buildSelectedPointsGeometry(self,
        pointIDs:list[int]) -> None:
        """ Build the selected point geometry.

        :param pointIDs: The list of selected point IDs.
        :type pointIDs: list[int]
        """
        selectedGeo = hou.Geometry()

        for pointID in pointIDs:
            pointPos    = self.defaultGeometry.getJointPosition(pointID)
            point       = selectedGeo.createPoint()                         # type: hou.Point
            point.setPosition(pointPos)

        self.selectedGeometry = CollisionGeometry(selectedGeo)

    @property
    def defaultGeometry(self) -> SkeletonGeometry:
        return self._defaultGeometry

    @defaultGeometry.setter
    def defaultGeometry(self, value:SkeletonGeometry) -> None:
        self._defaultGeometry = value
        self.drawableDefault.setGeometry(self._defaultGeometry.houGeometry)

    @property
    def highlightGeometry(self) -> CollisionGeometry:
        return self._highlightGeometry
    
    @highlightGeometry.setter
    def highlightGeometry(self, value:CollisionGeometry) -> None:
        self._highlightGeometry = value
        self.drawableHighlight.setGeometry(self._highlightGeometry.houGeometry)
    
    @property
    def selectedGeometry(self) -> CollisionGeometry:
        return self._selectedGeometry
    
    @selectedGeometry.setter
    def selectedGeometry(self, value:CollisionGeometry) -> None:
        self._selectedGeometry = value
        self.drawableSelected.setGeometry(self._selectedGeometry.houGeometry)