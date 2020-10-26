from typing import Dict, TypeVar, List

Instance=TypeVar("Instance")
Node=TypeVar("Node")

class Graph(object):
    pass

class Layer(object):
    pass

class Node(object):
    def __init__(self, config: Dict, instances: Dict,
    level: int, children: List[Node]=None)->None:
        """
        Stores layer configuration in node
        :param config: configuration of layer
        :param nodes: nodes of node
        :return None
        """
        self.children=([self._add_child(child)
        for child in children]
        if children else None)

        self._parameters={key: config[key]
        for key in config
        if key!="type"}

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