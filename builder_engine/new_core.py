from typing import Dict, List, TypeVar

Instance=TypeVar("Instance")
Tree=TypeVar("Tree")
Node=TypeVar("Node")

class Node(object):
    def __new__(cls, configuration: Dict,
    children: List[Node]=None)->Instance:
        """
        Stores layer configuration in node
        :param configuration: configuration of layer
        :param nodes: nodes of node
        :return None
        """
        """|Saves parameters of layer|"""
        replace=["layer", "type", "args", "kwargs"]
        cls._parameters={key: configuration[key]
        for key in configuration
        if key not in replace}
        """|Adds children to node|"""
        cls._children=([cls._add_child(child) 
        for child in children]
        if children else None)
        """|Saves type of layer|"""
        cls._type=configuration["type"]
        return cls
    def _add_child(self, child: Node):
        """
        Adds child to children
        :param child: node to add
        :return None
        """
        assert isinstance(child, self)
        self._children.append(child)
    def __repr__(self)->str:
        """
        Returns type of layer
        :return type of layer
        """
        return self._type