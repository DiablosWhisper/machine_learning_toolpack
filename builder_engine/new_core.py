from typing import Dict, List, TypeVar

Component=TypeVar("Component")
Instance=TypeVar("Instance")
Node=TypeVar("Node")

class NetworkCore(object):
    def compile(self, compile: Dict)->Dict:
        """
        """
        return None
    def process(self, process: Dict)->Dict:
        """
        """
        return None
    
    def __init__(self, network: Dict, 
    backend: str)->None:
        """
        """
        return None
class Component(object):
    def _wrap(self, component: Component)->Instance:
        """
        Wraps layer using its configuration
        :param layer: 
        :return wrapped layer
        """
        type=self._wrapper.pop(key="type")
        return self._instances[type](
        component, **self._wrapper)
    def _component(self)->Instance:
        """
        Builds component using its configuration
        :return built component
        """
        type=self._component.pop(key="type")
        return self._instances[type](
        **self._component)

    def __new__(cls, config: Dict, 
    instances: Dict)->Instance:
        """
        Stores component configuration
        :param config: configuration of component
        :param instances: component instances
        :return built component
        """
        """Divides config into subconfigs"""
        class_type=cls.__name__.lower()
        cls._wrapper=config.copy().pop(
        key=class_type, default=None)
        cls._component=config.copy()
        cls._instances=instances

        if not cls._wrapper: return cls._component()
        else: return cls._wrap(cls._component())
class Node(object):
    def __init__(self, config: Dict, instances: Dict,
    level: int, children: List[Node]=None)->None:
        """
        Stores component configuration in node
        :param config: configuration of component
        :param nodes: nodes of node
        :return None
        """
        """Saves children of the current node"""
        self.children=([self._add_child(child)
        for child in children]
        if children else None)

        """Saves parameters of node"""
        self._instances=instances
        self._config=config
        self._level=level
    def __ne__(self, other: Node)->bool:
        """
        Compares two nodes
        :param other: node to compare
        :return equivalence of nodes
        """
        assert isinstance(other, Node)
        return not (self._config is other._config)
    def __eq__(self, other: Node)->bool:
        """
        Compares two nodes
        :param other: node to compare
        :return equivalence of nodes
        """
        assert isinstance(other, Node)
        return (self._config is other._config)
    def __del__(self)->None:
        """
        Deletes node from graph
        :return None
        """
        ([child._del_child(self)
        for child in self.children] 
        if self.children else None)
    
    def _del_child(self, child: Node)->None:
        """
        Deletes child from children
        :param child: node to delete
        :return None
        """
        assert isinstance(child, Node)
        self.children.remove(child)
    def _add_child(self, child: Node)->None:
        """
        Adds child to children
        :param child: node to add
        :return None
        """
        assert isinstance(child, Node)
        self.children.append(child)
    def build(self)->Instance:
        """
        Builds component in node
        :return built component
        """
        return Component(config=self._config,
        instances=self._instances)