from typing import Dict, List, TypeVar

Instance=TypeVar("Instance")
Tree=TypeVar("Tree")
Node=TypeVar("Node")

class Node(object):
    def __new__(cls, config: Dict, instances: Dict,
    children: List[Node]=None)->Instance:
        """
        Stores layer configuration in node
        :param config: configuration of layer
        :param nodes: nodes of node
        :return None
        """
        """|Adds children to the current node|"""
        cls._children=([cls._add_child(child) 
        for child in children]
        if children else None)

        """|Saves parameters of layer|"""
        cls._parameters={key: config[key]
        for key in config
        if key!="cast"}

        """|Saves type of layer|"""
        cls._cast=config["cast"]

        return cls
    def _add_child(self, child: Node):
        """
        Adds child to children
        :param child: node to add
        :return None
        """
        assert isinstance(child, self)
        self._children.append(child)
    class _Builder(object):
        def __new__(cls, cast: str, parameters: Dict,
        instances: Dict)->Instance:
            """
            Build layer and returns its instance
            :param parameters: parameters of layer
            :param instances: instances of layers
            :param cast: cast of layer
            :return built layer
            """
            return instances[cast](**parameters)