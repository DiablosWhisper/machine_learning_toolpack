from typing import Dict, List, TypeVar

Component=TypeVar("Component")
Instance=TypeVar("Instance")
Vertex=TypeVar("Vertex")

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
        Wraps component using its configuration
        :param component: built component
        :return wrapped component
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

class Vertex(object):
    def __init__(self, config: Dict, level: int,
    instances: Dict)->None:
        """
        Stores component configuration in node
        :param config: configuration of component
        :param nodes: nodes of node
        :return None
        """
        self._instances=instances
        self._config=config
        self._level=level
        self.children=[]
    def __ne__(self, other: Vertex)->bool:
        """
        Compares two nodes
        :param other: node to compare
        :return equivalence of nodes
        """
        assert isinstance(other, Vertex)
        return not (self._config is other._config)
    def __eq__(self, other: Vertex)->bool:
        """
        Compares two nodes
        :param other: node to compare
        :return equivalence of nodes
        """
        assert isinstance(other, Vertex)
        return (self._config is other._config)
    def __del__(self)->None:
        """
        Deletes node from graph
        :return None
        """
        ([child.remove(self)
        for child in self.children] 
        if self.children else None)
    
    def remove(self, child: Vertex)->None:
        """
        Deletes child from children
        :param child: node to delete
        :return None
        """
        assert isinstance(child, Vertex)
        self.children.remove(child)
    def append(self, child: Vertex)->None:
        """
        Adds child to children
        :param child: node to add
        :return None
        """
        assert isinstance(child, Vertex)
        self.children.append(child)
    def build(self)->Instance:
        """
        Builds component in node
        :return built component
        """
        return Component(config=self._config,
        instances=self._instances)