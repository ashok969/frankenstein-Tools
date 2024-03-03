
import hou


class HNode(object):

    def __init__(self, node:hou.OpNode):

        self._node = node

    def getVector3Parm(self,
        parmName:str) -> hou.Vector3:
        """ Get a float 3 parameters values.

        :param parmName: The parameter name.
        :type parmName: str
        :return: The parameter value.
        :rtype: hou.Vector3
        """
        return hou.Vector3(
            self._node.parm("%sx" % parmName).eval(),
            self._node.parm("%sy" % parmName).eval(),
            self._node.parm("%sz" % parmName).eval()
        )

    def setVector3Parm(self,
        parmName:str,
        value:hou.Vector3) -> None:
        """ Set a float 3 parameters values.

        :param parmName: The parameter name.
        :type parmName: str
        :param value: The parameter value.
        :type value: hou.Vector3
        """
        self._node.parm("%sx" % parmName).set(value.x())
        self._node.parm("%sy" % parmName).set(value.y())
        self._node.parm("%sz" % parmName).set(value.z())

    @property
    def parm(self) -> hou.Parm:
        return self._node.parm
    
    @property
    def node(self) -> hou.Node:
        return self._node.node
    
    @node.setter
    def node(self, value:hou.Node):
        self._node = value

    @property
    def addParmCallback(self) -> hou.OpNode.addParmCallback:
        return self._node.addParmCallback

    @property
    def removeAllEventCallbacks(self) -> hou.OpNode.removeAllEventCallbacks:
        return self._node.removeAllEventCallbacks