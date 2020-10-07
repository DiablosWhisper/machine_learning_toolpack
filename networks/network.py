from tensorflow.keras.models import load_model, save_model
from typing import Dict, TypeVar, NewType
from core.core import ModelCore
from os.path import isdir
import logging, numpy

logging.basicConfig(format="%(asctime)s.%(msecs)06d : %(message)s",
datefmt="%Y-%m-%d %H:%M:%S",
level=logging.ERROR)

Numpy=NewType("Numpy", numpy)
History=TypeVar("History")

class DeepNetwork(object) :
    def load_model(self, path: str, name: str, **kwargs)->bool :
        """
        Loads model from file
        :param path: path for loading model
        :param name: name of model
        :return status of loading
        """
        if not isdir(path) :
            logging.error(f"Directory {path} doesn't exist")
            return False
        self._model=load_model(f"{path}/{name}.h5", **kwargs)
        return True
    def save_model(self, path: str, name: str, **kwargs)->bool :
        """
        Saves model into file
        :param path: path for saving model
        :param name: name of model
        :return status of saving
        """
        if not isdir(path) :
            logging.error(f"Directory {path} doesn't exist")
            return False
        save_model(self._model, f"{path}/{name}.h5", **kwargs)
        return True
    def compile(self, configuration: Dict)->bool :
        """
        Builds and compiles model from configuration
        :param configuration: configuration of deep neural network
        :return None
        """
        try :
            self._core=ModelCore(configuration["structure"])
            self._core.model.compile(**self._core.compile(configuration["compile"]))
            self._model=self._core.model
        except : 
            logging.error("Network building error occurred")
            return False
        else : return True
    def predict(self, inputs: Numpy)->Numpy :
        """
        Makes prediction using inputs
        :param inputs: numpy class object
        :return prediction
        """
        return self._model.predict(inputs)
    def fit(self, fit: Dict)->History :
        """
        Fits data into deep network
        :param fit: fit configuration
        :return history of learning
        """
        return self._model.fit(**self._core.build(fit))
    def __init__(self)->None :
        """
        Stores model object
        :return None
        """
        self._model=None
    def info(self)->None :
        """
        Prints information about the current neural network
        :return None
        """
        self._model.summary()