from inspect import getmembers, isclass
from importlib import import_module
from typing import List, TypeVar, Dict

Function=TypeVar("Function")
Instance=TypeVar("Instance")

class FunctionAnalyzer(object) :
    @staticmethod
    def get_function_kwargs(function: Function, ignore: List[str]=[]) -> List[str] :
        """
        Returns kwargs of function
        :param function: function to analyze
        :return kwargs
        """
        parameters=list(function.__code__.co_varnames)
        ([parameters.remove(kwarg) for kwarg in ignore
        if kwarg in parameters] if ignore != [] else "")
        return parameters
class PackageAnalyzer(object) :
    @staticmethod
    def get_class_from_package(package: str, name: str) -> Instance :
        """
        Returns class from package
        :param package: package where to search
        :param name: name of class to analyze
        """
        presumably_instance=getmembers(import_module(package))[name]
        return (presumably_instance
        if isclass(presumably_instance)
        else None)
    @staticmethod
    def get_classes_from_package(package: str) -> Dict :
        """
        Returns dictionary of package classes
        :param package: package where to search
        :return dictionary of instances
        """
        return {name:instance
        for name, instance in getmembers(import_module(package)) 
        if isclass(instance)}
class ClassAnalyzer(object) :
    @staticmethod
    def get_function(instance: Instance, name: str) -> Function :
        """
        Returns function by its name
        :param instance: class instance to analyze
        :param name: name of function to analyze
        :return function
        """
        presumably_function=instance.__dict__[name]
        return (presumably_function
        if callable(presumably_function) 
        else None)
    @staticmethod
    def get_functions(instance: Instance) -> Dict :
        """
        Returns dictionary of pairs like name:function
        :param instance: class instance to analyze
        :return dictionary of values
        """
        return {name:function
        for name, function in instance.__dict__.items() 
        if callable(function)}