from utilities.code_analyzer import PackageAnalyzer
from tensorflow.keras.models import Sequential
from typing import Dict, TypeVar, List
from copy import deepcopy
from inspect import isclass

LOAD_PACKAGES=["custom", "tensorflow.keras", "tensorflow_addons"]

Instance=TypeVar("Instance")
History=TypeVar("History")

class ModelCore(object) :
    def __init__(self, structure: List)->None :
        """
        Builds model from structure
        :param structure: structure of deep neural network
        :return None
        """
        self._components=self.ComponentFactory().build()
        try :  self.model=Sequential([self._components["Layers"](layer).build() 
        for layer in structure])
        except : raise RuntimeError("Layer building error occurred")
    def compile(self, compile: Dict)->Dict :
        """
        Builds "compile" block
        :param compile: compile block
        :return built compile block
        """
        configuration=deepcopy(compile)
        try :
            configuration["optimizer"]=self._components["Optimizers"](configuration["optimizer"]).build()
            configuration["loss"]=self._components["Losses"](configuration["loss"]).build()
            if "metrics" in configuration :
                configuration["metrics"]=[self._components["Metrics"](metric).build() 
                for metric in configuration["metrics"]]
        except : raise RuntimeError("Core compiling error occurred")
        else : return configuration
    def build(self, method: Dict)->Dict :
        """
        Builds "fit-like" blocks
        :param method: method block
        :return built method block
        """
        configuration=deepcopy(method)
        try :
            if "callbacks" in configuration :
                configuration["callbacks"]=[self._components["Callbacks"](callback).build()
                for callback in configuration["callbacks"]]
        except : raise RuntimeError("Core method error occurred")
        else : return configuration
    class ComponentFactory(object) :
        def __new__(cls)->Instance :
            """
            Defines singleton pattern
            :return instance of class
            """
            if not hasattr(cls, "_instance") :
                cls._components=["Layers", "Callbacks", "Optimizers", "Metrics", "Losses"]
                cls._instance=super(ModelCore.ComponentFactory, cls).__new__(cls)
                cls._existing_components={subclass.__name__: subclass
                for subclass in ModelCore.__dict__.values()
                if isclass(subclass)}
            return cls._instance
        def build(self)->Dict :
            """
            Builds dictionary of components
            :return dictionary of instances
            """
            return {component: type(component, (ModelCore.Component,), {})
            if component not in self._existing_components
            else self._existing_components[component]
            for component in self._components}
    class Component(object) :
        @staticmethod
        def _unpack(packages: List[str], component: str)->Dict :
            """
            Unpacks list of packages with an appropriate component
            :param packages: list of packages to unpack
            :param component: component to get
            :return unpacked dictionaries
            """
            packages=[PackageAnalyzer.get_classes_from_package(f"{package}.{component}") 
            for package in packages]
            return {item: packages[index][item]
            for index in range(len(packages))
            for item in packages[index]}
        def __new__(cls, configuration: Dict)->Instance :
            """
            Defines singleton pattern
            :param configuration: configuration of component
            :return instance of class
            """
            if not hasattr(cls, "_instance") :
                cls._instances={**cls._unpack(LOAD_PACKAGES, cls.__name__.lower())}
                cls._instance=super(ModelCore.Component, cls).__new__(cls)
            return cls._instance
        def __init__(self, configuration: Dict)->None :
            """
            Stores configuration of component
            :param configuration: configuration of component
            :return None
            """
            self._configuration=deepcopy(configuration)
            self._cast=self._configuration["cast"]
            self._configuration.pop("cast", "")
        def build(self)->Instance :
            """
            Builds component
            :return built instance of class
            """
            return self._instances[self._cast](**self._configuration)
    class Layers(Component) :
        def _get_wrapper(self, configuration: Dict)->None :
            """
            Gets wrapper parameters
            :param configuration: configuration from wrapper to get
            :return None
            """
            self._wrapper_configuration=deepcopy(configuration["wrapper"])
            self._wrapper_cast=configuration["wrapper"]["cast"]
            self._wrapper_configuration.pop("cast", "")
        def __init__(self, configuration: Dict)->None :
            """
            Stores configuration of layer
            :param configuration: configuration of layer
            :return None
            """
            self._clear_wrapper()
            if "wrapper" in configuration : self._get_wrapper(configuration)
            self._configuration=deepcopy(configuration)
            self._configuration.pop("wrapper", "")
            self._cast=self._configuration["cast"]
            self._configuration.pop("cast", "")
        def _wrap(self, layer: Instance)->Instance :
            """
            Wraps layer
            :param layer: keras class object
            :return instance of wrapped layer
            """
            return self._instances[self._wrapper_cast](layer, **self._wrapper_configuration)
        def _clear_wrapper(self)->None :
            """
            Removes class fields
            :return None
            """
            self.__dict__.pop("_wrapper_configuration", "")
            self.__dict__.pop("_wrapper_cast", "")
        def build(self)->Instance :
            """
            Builds layer
            :return built instance of layer
            """
            layer=self._instances[self._cast](**self._configuration)
            return (self._wrap(layer) if hasattr(self, "_wrapper_cast")
            else layer)