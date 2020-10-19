from utilities.code_analyzer import PackageAnalyzer
from hyperopt import Trials, STATUS_OK, tpe
from .core import ModelCore
from hyperas import optim
from typing import Dict

class ModelFinder(object):
    def __init__(self, configuration: Dict)->None:
        """
        Stores variable configuration of neural network
        :param configuration: configuration of neural network
        :return None
        """
        getter=PackageAnalyzer().get_functions_from_package
        self._functions=getter("hyperas.distributions")
        self._configuration=configuration