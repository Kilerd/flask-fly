from flask import Flask, request
from functools import wraps
from werkzeug.datastructures import MultiDict
import inspect

from typing import Generic, TypeVar


class Fly(object):

    def __init__(self, app=None):
        self.app: 'Flask' = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        pass

    def add_resource(self, resources: 'Resource'):

        for resource in resources.resources:
            setattr(resource, 'methods', [resource.__fly_method__])

            self.app.add_url_rule(resource.__fly_url__, view_func=Fly.view_wrapper(resource))

    @staticmethod
    def view_wrapper(func):

        @wraps(func)
        def wrapper(**kwargs):

            call_dict = {}
            url_parameters = kwargs.keys()

            call_dict.update(kwargs)
            parameters = inspect.signature(func)
            for name, param in parameters.parameters.items():
                if name not in url_parameters:

                    specific_location = getattr(param.annotation, '_gorg', None)

                    if specific_location is Header:
                        limited_locations = ['headers']
                    elif specific_location is Query:
                        limited_locations = ['args']
                    elif specific_location is Form:
                        limited_locations = ['form', 'json']
                    elif specific_location is Cookie:
                        limited_locations = ['cookies']
                    else:
                        limited_locations = ['args', 'form', 'json']

                    for location in limited_locations:
                        value = Fly.get_parameter(name, location)
                        if value:
                            call_dict[name] = value

            return func(**call_dict)

        return wrapper

    @staticmethod
    def get_parameter(name, limited_location='args'):
        if limited_location == 'json':
            if request.is_json:
                return request.get_json().get(name, None)
            else:
                return None

        elif limited_location in 'headers':
            location = getattr(request, limited_location, MultiDict())
            return location.get(name.capitalize(), None)

        location = getattr(request, limited_location, MultiDict())
        return location.get(name, None)


class Resource:

    def __init__(self):

        self.resources = []

    def request(self, url, method):

        def decorator(func):

            setattr(func, '__fly_method__', method)
            setattr(func, '__fly_url__', url)
            self.resources.append(func)

        return decorator

    def get(self, url):

        return self.request(url, "get")

    def post(self, url):

        return self.request(url, "post")

    def patch(self, url):

        return self.request(url, "patch")

    def put(self, url):

        return self.request(url, "put")

    def delete(self, url):

        return self.request(url, "delete")


T = TypeVar('T')


class Query(Generic[T]):

    pass


class Form(Generic[T]):

    pass


class Header(Generic[T]):

    pass


class Cookie(Generic[T]):

    pass
