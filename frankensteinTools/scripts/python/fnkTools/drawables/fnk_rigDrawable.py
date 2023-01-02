
import hou
import math
import viewerstate.utils as vs

from fnkTools       import FNKUtils  


class FNKRigDrawable(object):

    def __init__(self, stateName, sceneViewer):


        self._rigColor              = hou.Color(0.0, 0.85, 0.0)
        self._highlightColor        = hou.Color(0.0, 1.0, 1.0)
        self._selectedColor         = hou.Color(1.0, 0.6, 0.0)
        self._textColor             = hou.Color(1.0, 1.0, 1.0)

        self._stateName             = stateName
        self._sceneViewer           = sceneViewer

        self._drawableJointName     = hou.TextDrawable(
            self._sceneViewer,
            "fnk_rig_jointName"
        )

        self._drawableRigLines      = hou.GeometryDrawable(
            self._sceneViewer,
            hou.drawableGeometryType.Line,
            "fnk_rig_rigLines"
        )
        self._drawableRigLines.setParams(
            {
                "color1"        : self._rigColor,
                "use_cd"        : False,
                "fade_factor"   : 1.0
            }
        )

        self._drawableRigPoints     = hou.GeometryDrawable(
            self._sceneViewer,
            hou.drawableGeometryType.Point,
            "fnk_rig_rigPoints"
        )
        self._drawableRigPoints.setParams(
            {
                "color1"        : self._rigColor,
                "radius"        : 7,
                "style"         : hou.drawableGeometryPointStyle.SmoothCircle,
                "use_cd"        : False,
                "fade_factor"   : 1.0
            }
        )

        self._drawableLineH         = hou.GeometryDrawable(
            self._sceneViewer,
            hou.drawableGeometryType.Line,
            "fnk_rig_lineH"
        )
        self._drawableLineH.setParams(
            {
                "color1"        : self._highlightColor,
                "line_width"    : 2,
                "use_cd"        : False,
                "fade_factor"   : 1.0
            }
        )

        self._drawablePointH        = hou.GeometryDrawable(
            self._sceneViewer,
            hou.drawableGeometryType.Point,
            "fnk_rig_pointH"
        )
        self._drawablePointH.setParams(
            {
                "color1"        : self._highlightColor,
                "use_cd"        : False,
                "radius"        : 7,
                "style"         : hou.drawableGeometryPointStyle.SmoothCircle,
                "fade_factor"   : 1.0
            }
        )

        self._drawablePointRing     = hou.GeometryDrawable(
            self._sceneViewer,
            hou.drawableGeometryType.Point,
            "fnk_rig_pointRing"
        )
        self._drawablePointRing.setParams(
            {
                "color1"        : self._textColor,
                "radius"        : 5,
                "style"         : hou.drawableGeometryPointStyle.Ring,
                "fade_factor"   : 1.0
            }
        )

        self._drawablePointSel      = hou.GeometryDrawable(
            self._sceneViewer,
            hou.drawableGeometryType.Point,
            "fnk_rig_pointSel"
        )
        self._drawablePointSel.setParams(
            {
                "color1"        : self._selectedColor,
                "use_cd"        : False,
                "radius"        : 9,
                "style"         : hou.drawableGeometryPointStyle.SmoothCircle,
                "fade_factor"   : 1.0
            }
        )

        self._drawableMirrorLines   = hou.GeometryDrawable(
            self._sceneViewer,
            hou.drawableGeometryType.Line,
            "fnk_rig_mirrorLines"
        )
        self._drawableMirrorLines.setParams(
            {
                "color1"        : self._rigColor,
                "line_width"    : 2,
                "use_cd"        : False,
                "fade_factor"   : 1.0
            }
        )

        self._pointGeometry         = hou.Geometry()
        self._lineGeometry          = hou.Geometry()
        self._selectedPointGeometry = hou.Geometry()
        self._rigGeometry           = hou.Geometry()
        self._mirrorGeometry        = hou.Geometry()
        self._jointName             = ""
        self._jointNameScreenPos    = hou.Vector3()
        self._selectedJointID       = -1
        self._jointNameTextColor    = hou.Color(1,1,1)

    def setRigGeometry(self, geometry:hou.Geometry) -> None:
        """ Set the rig geometry to use for drawables.

        Args:
            geometry (hou.Geometry) : The geometry that contain the rig description.
        """
        self._drawableRigLines.setGeometry(geometry)
        self._drawableRigPoints.setGeometry(geometry)

    def setMirrorGeometry(self, geometry:hou.Geometry) -> None:
        """ Set the mirror geometry to use for drawable.

        Args:
            geometry (hou.Geometry) : The geometry that contain the mirror description.
        """
        self._drawableMirrorLines.setGeometry(geometry)
    
    def buildLineGeometry(self, p0pos:hou.Vector3, p1pos:hou.Vector3) -> None:
        """ Build the line and point highlight geometry from the current selection location.

        Args:
            p0pos (hou.Vector3) : The first point of the line.
            p1pos (hou.Vector3) : The second point of the line.

        Returns:
            hou.Geometry : The geometry that contain the line.
        """
        geometry = hou.Geometry()
        # Buidl the line geometry.
        linePrim    = geometry.createPolygon(is_closed=False)
        linePoints  = geometry.createPoints((p0pos, p1pos))
        linePrim.addVertex(linePoints[0])
        linePrim.addVertex(linePoints[1])
    
        return geometry

    def buildPointGeometry(self, p0pos:hou.Vector3) -> None:
        """ Build the point selected geometry from the selection.

        Args:
            p0pos (hou.Vector3) : The point position.

        Returns:
            hou.Geometry : The geometry that contain the point.
        """
        geometry = hou.Geometry()
        # Build the point geometry.
        point = geometry.createPoint()
        point.setPosition(p0pos)

        return geometry

    def setDraw(self, handle) -> None:
        """ Set the joint name to display.

        Args:
            handle  () : The drawable handle.
        """
        self._drawableRigLines.draw(handle)
        self._drawableRigPoints.draw(handle)
        self._drawableLineH.draw(handle)
        self._drawablePointH.draw(handle)
        self._drawablePointRing.draw(handle)
        self._drawablePointSel.draw(handle)
        self._drawableMirrorLines.draw(handle)
        self._drawableMirrorLines.draw(handle)


        params = {
            "text"      : "<b>%s</b>" % self._jointName,
            "color1"    : self._jointNameTextColor,
            "origin"    : hou.drawableTextOrigin.LeftCenter,
            "translate" : self._jointNameScreenPos
        }

        self._drawableJointName.draw(handle, params)

    def setLocatedSelection(self, kwargs):
        """ Use this function in the onLocatedSelection of the state to build the highlight line and point geometry and display them.
        """
        # Update the highlight and joint name display.
        self.hideHightlight
        self.hideJointName

        # Get the drawable selection datas.
        if("drawable_selection" in kwargs):

            # Init the joint point ID.
            pointID = -1
            # Init the joint line point IDs.
            linePointIDs = None

            # Get the selection datas.
            for k, v in kwargs["drawable_selection"].items():

                if(k == "fnk_rig_rigLines"):
                    # Check if we have some data from the rig line geometry.
                    if("line" in v):
                        pointID = v["line"][0]
                        linePointIDs = v["line"]
                        break
                elif(k == "fnk_rig_rigPoints"):
                    # Check if we have some datas from the rig point geometry.
                    if("point" in v):
                        pointID = v["point"][0]
                        break
            # Check if some point need to be highlighted.            
            if(pointID > -1):
                # Get the point position.
                jointPos        = FNKUtils.getJointPosition(self.rigGeometry, pointID)
                print(pointID)
                print(jointPos)
                # Build the point geometry.
                pointGeo        = self.buildPointGeometry(jointPos)
                # Update the point drawable point highlight geometry.
                self._drawablePointH.setGeometry(pointGeo)
                self._drawablePointH.show(True)
                # Update the joint name.
                self._jointName             = FNKUtils.getJointName(self.rigGeometry, "name", pointID)
                self._jointNameScreenPos    = FNKUtils.modelToScreenSpace(self._sceneViewer, jointPos, hou.Vector3(15,0,0)) 
                self._drawableJointName.show(True)
                # Update the point drawable point ring geometry.
                self._drawablePointRing.setGeometry(pointGeo)
                self._drawablePointRing.show(True)
            
            # Check if some line need to be highlighted.
            if(linePointIDs):
                # Get the line's point position.
                p0pos   = FNKUtils.getJointPosition(self.rigGeometry, linePointIDs[0])
                p1pos   = FNKUtils.getJointPosition(self.rigGeometry, linePointIDs[1])
                lineGeo = self.buildLineGeometry(p0pos, p1pos)

                self._drawableLineH.setGeometry(lineGeo)

                self._drawableLineH.show(True)

    def setSelection(self, kwargs):
        """ Execute this function in the onSelection.
        """
        self._drawablePointSel.show(False)
        self.hideHightlight
        # Get the current drawable selection datas.
        if("drawable_selection" in kwargs):
            drawableDatas = kwargs["drawable_selection"]
            jointID = -1
            if("fnk_rig_rigPoints" in drawableDatas):
                pointGeo = drawableDatas["fnk_rig_rigPoints"]
                if("point" in pointGeo):
                    jointID = pointGeo["point"][0]
            elif("fnk_rig_rigLines" in drawableDatas):
                lineGeo = drawableDatas["fnk_rig_rigLines"]
                if("line" in lineGeo):
                    jointID = lineGeo["line"][0]

            if(jointID > -1):

                # Set and display the drawable selected geometry.
                self._drawablePointSel.setParams({"indices":[jointID]})
                self._drawablePointSel.show(True)


                self._selectedJointID = jointID

                return jointID

        return None

    def setStopSelection(self, kwargs):
        """ Execute this function in the onStopSelection.
        """
        selector_name = kwargs["name"]

        if(selector_name == "my_drawable_selector"):
            self.hideHightlight

    @property
    def rigGeometry(self) -> hou.Geometry:
        return self._rigGeometry

    @rigGeometry.setter
    def rigGeometry(self, rigGeometry:hou.Geometry) -> None:
        self._rigGeometry = rigGeometry
        self._drawableRigLines.setGeometry(self._rigGeometry)
        self._drawableRigPoints.setGeometry(self._rigGeometry)
        self._drawablePointSel.setGeometry(self._rigGeometry)

    @property
    def showJointName(self):
        self._drawableJointName.show(True)
    
    @property
    def hideJointName(self):
        self._drawableJointName.show(False)

    @property
    def showHighlight(self):
        self._drawableLineH.show(True)
        self._drawablePointH.show(True)
        self._drawablePointRing.show(True)
        self._drawableJointName.show(True)
    
    @property
    def hideHightlight(self):
        self._drawableLineH.show(False)
        self._drawablePointH.show(False)
        self._drawablePointRing.show(False)
        self._drawableJointName.show(False)
    
    @property
    def showRig(self):
        self._drawableRigLines.show(True)
        self._drawableRigPoints.show(True)
    
    @property
    def hideRig(self):
        self._drawableRigLines.show(False)
        self._drawableRigPoints.show(False)
    
    @property
    def showMirror(self):
        self._drawableMirrorLines.show(True)

    @property
    def hideMirror(self):
        self._drawableMirrorLines.show(False)
    
    @property
    def showSel(self):
        self._drawablePointSel.show(True)
    
    @property
    def hideSel(self):
        self._drawablePointSel.show(False)