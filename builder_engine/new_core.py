from typing import Dict, List, TypeVar

Instance=TypeVar("Instance")

class Graph(object):
    def __new__(cls)->Instance:
        """
        """
        return
    class _Branch(object):
        def __new__(cls, configs: List[Dict],
        level: int)->Instance:
            """
            """
            return cls
        class _Node(object):
            def __new__(cls, config: Dict, 
            instances: Dict)->Instance:
                """
                Stores layer configuration in node
                :param config: configuration of layer
                :param nodes: nodes of node
                :return None
                """
                """|Saves parameters of layer|"""
                cls._parameters={key: config[key]
                for key in config
                if key!="cast"}

                """|Saves instances of layers|"""
                cls._instances=instances

                """|Saves type of layer|"""
                cls._cast=config["cast"]

                """|Builds layer(s)|"""
                return cls._Builder(cast=cls._cast,
                parameters=cls._parameters,
                instances=cls._instances)
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

branch_1=[
    dict(type="Input"),
    dict(type="TimeDistributed", layer=dict(type="Dense")),
    dict(type="Dense")
]
branch_2=[
    dict(type="Input"),
    dict(type="Bidirectional", layer=dict(type="Dense")),
    dict(type="Dense")
]
root=[
    dict(type="Concatenate", layer=[branch_1, branch_2]),
    dict(type="Dense"),
    dict(type="Dense")
]