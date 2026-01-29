#!/usr/bin/env python3
"""
Utility functions for unit and integration tests
"""
from typing import Mapping, Sequence, Any, Callable
import requests
from functools import wraps


def access_nested_map(nested_map: Mapping, path: Sequence) -> Any:
    """
    Access a value in a nested map using a sequence of keys.

    Raises KeyError if a key is missing or path is invalid.
    """
    for key in path:
        if not isinstance(nested_map, dict):
            raise KeyError(key)
        if key not in nested_map:
            raise KeyError(key)
        nested_map = nested_map[key]
    return nested_map


def get_json(url: str) -> Any:
    """
    Get JSON response from a URL.
    """
    response = requests.get(url)
    return response.json()


def memoize(method: Callable) -> Callable:
    """
    Decorator to memoize a method.
    """
    attr_name = "_{}".format(method.__name__)

    @wraps(method)
    def wrapper(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, method(self))
        return getattr(self, attr_name)

    return wrapper