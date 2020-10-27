from typing import Dict, List, TypeVar

Instance=TypeVar("Instance")
Layer=TypeVar("Layer")
Node=TypeVar("Node")

class Layer(object):
    def _wrap(self, layer: Layer, config: Dict,
    instances: Dict)->Instance:
        """
        Wraps layer and returns its instance
        :param config: configuration of layer
        :param instances: instances of layers
        :param layer: layer class instance
        :return built layer
        """
        return None
    def __new__(cls, type: str, config: Dict,
    instances: Dict)->Instance:
        """
        Build layer and returns its instance
        :param config: configuration of layer
        :param instances: instances of layers
        :param type: type of layer
        :return built layer
        """
        return None
class Node(object):
    def __init__(self, config: Dict, instances: Dict,
    level: int, children: List[Node]=None)->None:
        """
        Stores layer configuration in node
        :param config: configuration of layer
        :param nodes: nodes of node
        :return None
        """
        """|Saves parameters of layer|"""
        self.children=([self._add_child(child)
        for child in children]
        if children else None)

        """|Saves parameters of layer|"""
        self._parameters={key: config[key]
        for key in config
        if key!="type"}

        """|Saves parameters of node|"""
        self._instances=instances
        self._type=config["type"]
        self._level=level
    def _del_child(self, child: Node)->None:
        """
        Deletes child from children
        :param child: node to delete
        :return None
        """
        assert isinstance(child, self)
        self.children.remove(child)
    def _add_child(self, child: Node)->None:
        """
        Adds child to children
        :param child: node to add
        :return None
        """
        assert isinstance(child, self)
        self.children.append(child)
    def build(self)->Instance:
        """
        Builds layer in node
        :return built layer
        """
        return Layer(type=self._type,
        parameters=self._parameters,
        instances=self._instances)
    def __del__(self)->None:
        """
        Deletes node from graph
        :return None
        """
        ([child._del_child(self)
        for child in self.children] 
        if self.children else None)