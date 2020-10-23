from typing import Dict, List, TypeVar

Instance=TypeVar("Instance")
Graph=TypeVar("Graph")
Node=TypeVar("Node")

class Graph(object):
    def _traverse(self, graph: Graph, root: Node):
        """
        Traverses graph using breadth first search
        :param graph: collection of nodes
        :param root: root of graph
        """
        """|Initializing container for algorithm|"""
        visited, queue=[], []
        visited.append(root)
        queue.append(root)

        """|Starting traversing|"""
        while queue: 
            [(visited.append(child), queue.append(child))
            for child in graph[queue.pop(0)]
            if child not in visited]
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
            cls.children=([cls._add_child(child) 
            for child in children]
            if children else None)

            """|Saves parameters of layer|"""
            cls._parameters={key: config[key]
            for key in config
            if key!="cast"}

            """|Saves instances of layers|"""
            cls._instances=instances

            """|Saves type of layer|"""
            cls._cast=config["cast"]

            return cls
        def _del_child(self, child: Node):
            """
            Deletes child from children
            :param child: node to delete
            :return None
            """
            assert isinstance(child, self)
            self.children.remove(child)
        def _add_child(self, child: Node):
            """
            Adds child to children
            :param child: node to add
            :return None
            """
            assert isinstance(child, self)
            self.children.append(child)
        def build(self)->Instance:
            """
            Builds layer in the current node
            :return built layer instance
            """
            return self._Builder(cast=self._cast,
            parameters=self._parameters,
            instances=self._instances)
        def __del__(self):
            """
            Deletes node and its connections
            :return None
            """
            [child._del_child(self)
            for child in self.children]
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