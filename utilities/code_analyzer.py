from inspect import getmembers, isclass, isfunction
from types import FunctionType as Function
from importlib import import_module
from typing import List, TypeVar, Dict

Function=TypeVar("Function")
Instance=TypeVar("Instance")

class GetItemFrom(object) :
    def _get_item_from(self, get_from: Dict, condition: object, name: str)->object :
        """
        Retursn dictionary of item and their names
        :param get_from: object from where item will be got
        :param condition: condition for getting item
        :param name: name of item to get
        :return item with their names
        """
        try: item=get_from[name]
        except: raise AttributeError(f"Item with name: {name} doesn't exist")
        if not condition(item): raise TypeError(f"{name} with such type doesn't exist")
        return item
    def _get_items_from(self, get_from: Dict, condition: object)->Dict :
        """
        Retursn dictionary of objects and their names
        :param get_from: object from where other objects will be got
        :param condition: condition for getting object
        :return objects with their names
        """
        return {name: item for name, item in get_from.items() if condition(item)}
class PackageAnalyzer(GetItemFrom) :
    def get_function_from_package(self, package: str, name: str)->Function :
        """
        Returns function from package
        :param package: package where to search
        :param name: name of function to get
        """
        return self._get_item_from(get_from=dict(getmembers(import_module(package))),
        condition=isfunction, name=name)
    def get_class_from_package(self, package: str, name: str)->Instance :
        """
        Returns class from package
        :param package: package where to search
        :param name: name of class to get
        """
        return self._get_item_from(get_from=dict(getmembers(import_module(package))), 
        condition=isclass, name=name)
    def get_functions_from_package(self, package: str)->Dict :
        """
        Returns dictionary of package functions
        :param package: package where to search
        :return dictionary of functions
        """
        return self._get_items_from(get_from=dict(getmembers(import_module(package))),
        condition=isfunction)
    def get_classes_from_package(self, package: str)->Dict :
        """
        Returns dictionary of package classes
        :param package: package where to search
        :return dictionary of instances
        """
        return self._get_items_from(get_from=dict(getmembers(import_module(package))),
        condition=isclass)
class ClassAnalyzer(GetItemFrom) :
    def get_function(self, instance: Instance, name: str)->Function :
        """
        Returns function by its name
        :param instance: class instance to analyze
        :param name: name of function to analyze
        :return function
        """
        return self._get_item_from(get_from=instance.__dict__,
        condition=isfunction, name=name)
    def get_functions(self, instance: Instance)->Dict :
        """
        Returns dictionary of pairs like name:function
        :param instance: class instance to analyze
        :return dictionary of values
        """
        return self._get_items_from(get_from=instance.__dict__,
        condition=isfunction)
class FunctionAnalyzer(object) :
    @staticmethod
    def get_function_kwargs(function: Function, ignore: List[str]=[])->List[str] :
        """
        Returns kwargs of function
        :param function: function to analyze
        :return kwargs
        """
        parameters=list(function.__code__.co_varnames)
        ([parameters.remove(kwarg) for kwarg in ignore
        if kwarg in parameters] if ignore != [] else "")
        return parameters