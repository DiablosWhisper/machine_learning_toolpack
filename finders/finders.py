from kerastuner.tuners import RandomSearch, BayesianOptimization, Hyperband
from kerastuner import HyperParameters, HyperModel

from networks import ModelCore
from typing import Dict, TypeVar

Method=TypeVar("Method")
Model=TypeVar("Model")

class ModelFinder(object) :
    def _set_value(self, value: object, path: str, dictionary: Dict)->None :
        """
        Sets values to dictionary
        :param dictionary: where to set value 
        :param values: values to set
        :param path: "a.b.c ..."
        """
        divided_keys=path.split(".")[::-1]
        pair=dictionary[divided_keys.pop()]
        for _ in divided_keys[:-1] : pair=pair[divided_keys.pop()]
        pair[divided_keys.pop()]=value
    def search(self, algorithm: str="HyperBand", **kwargs: Dict)->Dict :
        """
        Returns the best configuration
        :return the best configuration
        """
        builder_arguments={"configuration": self._configuration, "decode": self._decode, "encode": self._encode}
        tuner=self._searchers[algorithm](self._ModelBuilder(**builder_arguments), **kwargs)
        tuner.search(**ModelCore().build(self._configuration["fit"]))
        configuration=tuner.get_best_hyperparameters()[0].values
        return self._get_optimal_configuration(configuration)
    def _get_optimal_configuration(self, configuration: Dict)->Dict :
        """
        Fills configuration with optimal parameters
        :param configuration: optimal values
        :return optimal configuration
        """
        self._configuration=self._encode(self._configuration)
        [self._set_value(configuration[layer], layer, self._configuration)
        for layer in configuration]
        return self._decode(self._configuration)
    def __init__(self, configuration: Dict)->None :
        """
        Stores configuration of deep neural network
        :return None
        """
        self._searchers={
        "BayesianOptimization": BayesianOptimization,
        "RandomSearch": RandomSearch,
        "Hyperband": Hyperband}
        self._configuration=configuration
    def _decode(self, configuration: Dict)->Dict :
        """
        Decodes configuration to an appropriate format
        :param configuration: configuration to untransform
        :return None
        """
        configuration["structure"]=[configuration["structure"][field]
        for field in configuration["structure"]]
        return configuration
    def _encode(self, configuration: Dict)->Dict :
        """
        Encodes configuration to an appropriate format
        :param configuration: configuration to transform
        :return transformed configuration
        """
        configuration["structure"]={f"{index}": configuration["structure"][index]
        for index in range(len(configuration["structure"]))}
        return configuration
    class _ModelBuilder(HyperModel) :
        def __init__(self, configuration: Dict, encode: Method, decode: Method)->None :
            """
            Stores encoded configuration
            :param decode: method for decode configuration
            :param encode: mathod for encode configuration
            :param configuration: encoded configuration
            :return None
            """
            self._configuration=configuration
            self._decode=decode
            self._encode=encode
        def build(self, parameters: HyperParameters)->Model :
            """
            Builds configuration for searching
            :param parameters: hyperparameters class object
            :return compiled deep network model
            """
            self._encode(self._configuration)
            structure=self._configuration["structure"]
            for layer in structure :
                for field in structure[layer] :
                    if isinstance(structure[layer][field], list) :
                        structure[layer][field]=parameters.Choice(f"structure.{layer}.{field}", structure[layer][field])
            core=ModelCore(self._decode(self._configuration)["structure"])
            core.model.compile(**core.compile(self._configuration["compile"]))
            return core.model