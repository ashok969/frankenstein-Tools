
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