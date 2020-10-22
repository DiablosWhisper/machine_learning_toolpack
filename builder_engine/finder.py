from utilities.code_analyzer import PackageAnalyzer
from hyperopt import Trials, STATUS_OK, tpe
from .core import ModelCore
from hyperas import optim
from typing import Dict

class ModelFinder(object):
    def __init__(self, config: Dict)->None:
        """
        Stores variable configuration of neural network
        :param config: configuration of neural network
        :return None
        """
        self._functions=PackageAnalyzer().get_functions(
        package="hyperas.distributions")
        self._config=config
