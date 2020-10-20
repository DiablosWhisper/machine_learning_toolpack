from utilities.code_analyzer import PackageAnalyzer
from tensorflow.keras.models import Sequential
from typing import Dict, TypeVar, List
from inspect import isclass
from copy import deepcopy

COMPONENTS_TO_LOAD=["Layers", "Callbacks", "Optimizers", "Metrics", "Losses"]
LOAD_PACKAGES=["custom_components", "tensorflow_addons", "tensorflow.keras"]

Instance=TypeVar("Instance")
History=TypeVar("History")

class ModelCore(object):
    def __init__(self, config: List)->None:
        """
        Builds model from configuration
        :param config: structure of neural network
        :return None
        """
        self._components=self.ComponentFactory().build()
        self._optimizers=self._components["Optimizers"]
        self._callbacks=self._components["Callbacks"]
        self._metrics=self._components["Metrics"]
        self._layers=self._components["Layers"]
        self._losses=self._components["Losses"]
        self.model=Sequential([self._layers(layer).build() 
        for layer in config])
    def compile(self, config: Dict)->Dict:
        """
        Builds "compile" block
        :param config: compile block
        :return built compile block
        """
        config["optimizer"]=self._optimizers(config["optimizer"]).build()
        if "metrics" in config:
            config["metrics"]=[self._metrics(metric).build()
            for metric in config["metrics"]]
        config["loss"]=self._losses(config["loss"]).build()
        return config
    def build(self, config: Dict)->Dict:
        """
        Builds "fit-like" blocks
        :param config: method block
        :return built method block
        """
        if "callbacks" in config:
            config["callbacks"]=[self._callbacks(callback).build()
            for callback in config["callbacks"]]
        return config
    class ComponentFactory(object):
        def __new__(cls)->Instance:
            """
            Defines singleton pattern
            :return instance of class
            """
            if not hasattr(cls, "_instance"):
                cls._instance=super(ModelCore.ComponentFactory, cls).__new__(cls)
                cls._existing_components={subclass.__name__: subclass
                for subclass in ModelCore.__dict__.values()
                if isclass(subclass)}
            return cls._instance
        def build(self)->Dict:
            """
            Builds dictionary of components
            :return dictionary of instances
            """
            return {component: type(component, (ModelCore.Component,), {})
            if component not in self._existing_components
            else self._existing_components[component]
            for component in COMPONENTS_TO_LOAD}
    class Component(object):
        @staticmethod
        def _unpack(packages: List[str], component: str)->Dict:
            """
            Unpacks list of packages with an appropriate component
            :param packages: list of packages to unpack
            :param component: component to get
            :return unpacked dictionaries
            """
            getter=PackageAnalyzer().get_classes_from_package
            packages=[getter(f"{package}.{component}") 
            for package in packages]
            return {item: packages[index][item]
            for index in range(len(packages))
            for item in packages[index]}
        def __new__(cls, config: Dict)->Instance:
            """
            Defines singleton pattern
            :param config: configuration of component
            :return instance of class
            """
            if not hasattr(cls, "_instance"):
                cls._instances={**cls._unpack(LOAD_PACKAGES, cls.__name__.lower())}
                cls._instance=super(ModelCore.Component, cls).__new__(cls)
            return cls._instance
        def __init__(self, config: Dict)->None:
            """
            Stores configuration of component
            :param config: configuration of component
            :return None
            """
            self._config=deepcopy(config)
            self._config.pop("cast", "")
            self._cast=config["cast"]
        def build(self)->Instance:
            """
            Builds component
            :return built component
            """
            try: component=self._instances[self._cast](**self._config)
            except: raise RuntimeError(f"{self.__name__} error occured")
            else: return component
    class Layer(Component):
        def build(self)->Instance:
            """
            Builds layer
            :return built layer
            """
            try: built_layer=self._instances[self._cast](**self._config)
            except: raise RuntimeError(f"{self.__name__} error occured")
            for layer, config in self._unfold()[::-1]:
                try: built_layer=self._instances[layer](
                **{**config, **dict(layer=built_layer)})
                except: raise RuntimeError(f"{self.__name__} error occured")
            return built_layer
        def _unfold(self)->List:
            """
            Unfolds nested layers
            :return layers and theirs configurations
            """
            unfolded_layers=[]
            while "layer" in self._config:
                pair=(self._cast, self._config.copy().pop("layer"))
                self._config=self._config["layer"]
                self._cast=self._config["cast"]
                unfolded_layers.append(pair)
            return unfolded_layers