from typing import Dict, List, TypeVar

Instance=TypeVar("Instance")
Layer=TypeVar("Layer")
Node=TypeVar("Node")

class NetworkCore(object):
    def __init__(self, network: Dict)->None:
        """
        """
        pass
class Builder(object):
    def _wrap(self, layer: Layer)->Instance:
        """
        Wraps layer using its configuration
        :param layer: 
        :return wrapped layer
        """
        type=self._wrapper.pop(key="type")
        return self._instances[type](
        layer=layer, **self._wrapper)
    def __new__(cls, config: Dict, 
    instances: Dict)->Instance:
        """
        Stores layer configuration
        :param config: configuration of layer
        :param instances: layers instances
        :return built layer
        """
        """|Divides config into subconfigs|"""
        cls._wrapper=config.copy().pop(
        key="layer", default=None)
        cls._layer=config.copy()
        cls._instances=instances

        if not cls._wrapper: return cls._layer()
        else: return cls._wrap(cls._layer())
    def _layer(self)->Instance:
        """
        Builds layer using its configuration
        :return built layer
        """
        type=self._layer.pop(key="type")
        return self._instances[type](
        **self._layer)
class Node(object):
    def __init__(self, config: Dict, instances: Dict,
    level: int, children: List[Node]=None)->None:
        """
        Stores layer configuration in node
        :param config: configuration of layer
        :param nodes: nodes of node
        :return None
        """
        """|Saves children of the current node|"""
        self.children=([self._add_child(child)
        for child in children]
        if children else None)

        """|Saves parameters of node|"""
        self._instances=instances
        self._config=config
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
        return Builder(self._config,
        self._instances)
    def __del__(self)->None:
        """
        Deletes node from graph
        :return None
        """
        ([child._del_child(self)
        for child in self.children] 
        if self.children else None)