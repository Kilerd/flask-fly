from flask import Flask
from flask_fly import *
from typing import List, get_type_hints, Union, Optional

import inspect


class TestBaseHttpMethod:

    def test_get(self):

        flask = Flask(__name__)
        fly = Fly(flask)
        resource = Resource()

        @resource.get('/')
        def index():
            return 'hello world'

        fly.add_resource(resource)

        with flask.test_client() as client:
            res = client.get('/')
            assert res.status_code == 200
            assert res.data == b'hello world'

    def test_post(self):

        flask = Flask(__name__)
        fly = Fly(flask)
        resource = Resource()

        @resource.post('/')
        def index():
            return 'hello world'

        fly.add_resource(resource)

        with flask.test_client() as client:
            res = client.post('/')
            assert res.status_code == 200
            assert res.data == b'hello world'

    def test_patch(self):
        flask = Flask(__name__)
        fly = Fly(flask)
        resource = Resource()

        @resource.patch('/')
        def index():
            return 'hello world'

        fly.add_resource(resource)

        with flask.test_client() as client:
            res = client.patch('/')
            assert res.status_code == 200
            assert res.data == b'hello world'

    def test_put(self):
        flask = Flask(__name__)
        fly = Fly(flask)
        resource = Resource()

        @resource.put('/')
        def index():
            return 'hello world'

        fly.add_resource(resource)

        with flask.test_client() as client:
            res = client.put('/')
            assert res.status_code == 200
            assert res.data == b'hello world'

    def test_delete(self):
        flask = Flask(__name__)
        fly = Fly(flask)
        resource = Resource()

        @resource.delete('/')
        def index():
            return 'hello world'

        fly.add_resource(resource)

        with flask.test_client() as client:
            res = client.delete('/')
            assert res.status_code == 200
            assert res.data == b'hello world'


class TestParameterLocation:

    def test_http_basic_method_with_url_parameter(self):

        flask = Flask(__name__)
        fly = Fly(flask)
        resource = Resource()

        @resource.get("/<id>")
        def get_id(id):

            return 'get id with value {}'.format(id)

        fly.add_resource(resource)

        with flask.test_client() as client:
            res = client.get('/123')
            assert res.status_code == 200
            assert res.data == b'get id with value 123'

            res = client.get('/hello-world')
            assert res.status_code == 200
            assert res.data == b'get id with value hello-world'

    def test_get_extra_parameter(self):

        flask = Flask(__name__)
        fly = Fly(flask)
        resource = Resource()

        @resource.get("/hello")
        def get_id(name):
            return 'hello {}'.format(name)

        fly.add_resource(resource)

        with flask.test_client() as client:
            res = client.get('/hello?name=world')
            assert res.status_code == 200
            assert res.data == b'hello world'

    def test_get_extra_parameter_without_specific_location(self):

        flask = Flask(__name__)
        fly = Fly(flask)
        resource = Resource()

        @resource.post("/hello")
        def get_id(name):
            return 'hello {}'.format(name)

        fly.add_resource(resource)

        with flask.test_client() as client:
            res = client.post('/hello?name=world')
            assert res.status_code == 200
            assert res.data == b'hello world'

            res = client.post('/hello', data={'name': 'world'})
            assert res.status_code == 200
            assert res.data == b'hello world'

            res = client.post('/hello', json={'name': 'world'})
            assert res.status_code == 200
            assert res.data == b'hello world'

    def test_get_extra_parameter_from_header(self):
        flask = Flask(__name__)
        fly = Fly(flask)
        resource = Resource()

        @resource.post("/hello")
        def get_id(name: Header[str]):
            return 'hello {}'.format(name)

        fly.add_resource(resource)

        with flask.test_client() as client:
            res = client.post('/hello', headers={'name': 'world'})
            assert res.data == b'hello world'
            assert res.status_code == 200

    def test_get_extra_parameter_from_query(self):

        flask = Flask(__name__)
        fly = Fly(flask)
        resource = Resource()

        @resource.post("/hello")
        def get_id(name: Query[str]):
            return 'hello {}'.format(name)

        fly.add_resource(resource)

        with flask.test_client() as client:
            res = client.post('/hello?name=Alice')
            assert res.status_code == 200
            assert res.data == b'hello Alice'

    def test_get_extra_parameter_from_form(self):

        flask = Flask(__name__)
        fly = Fly(flask)
        resource = Resource()

        @resource.post("/hello")
        def get_id(name: Form[str]):
            return 'hello {}'.format(name)

        fly.add_resource(resource)

        with flask.test_client() as client:
            res = client.post('/hello', data={'name': 'Bob'})
            assert res.data == b'hello Bob'
            assert res.status_code == 200

    def test_get_extra_parameter_from_cookie(self):

        flask = Flask(__name__)
        fly = Fly(flask)
        resource = Resource()

        @resource.post("/hello")
        def get_id(name: Cookie[str]):
            return 'hello {}'.format(name)

        fly.add_resource(resource)

        with flask.test_client() as client:

            client.set_cookie('localhost', 'name', 'Daniel')
            res = client.post('/hello')
            assert res.data == b'hello Daniel'
            assert res.status_code == 200

    def test_get_extra_parameters(self):

        flask = Flask(__name__)
        fly = Fly(flask)
        resource = Resource()

        @resource.post("/")
        def get_id(all_location,
                   from_query: Query[str],
                   from_form: Form[str],
                   header: Header[str],
                   from_cookie: Cookie[str]):
            return '{} {} {} {} {}'.format(all_location, from_query, from_form, header, from_cookie)

        fly.add_resource(resource)

        with flask.test_client() as client:
            client.set_cookie('localhost', 'from_cookie', 'hello')
            res = client.post('/?all_location=hello&from_query=world',
                              data={'from_form': 'here'},
                              headers={'header': 'woo'})
            assert res.data == b'hello world here woo hello'
            assert res.status_code == 200


class TestOptionalParameter:


    def test_optional_parameter(self):

        flask = Flask(__name__)
        fly = Fly(flask)
        resource = Resource()

        @resource.get("/hello")
        def get_id(name="world"):
            return 'hello {}'.format(name)

        fly.add_resource(resource)

        with flask.test_client() as client:
            res = client.get('/hello?name=world')
            assert res.status_code == 200
            assert res.data == b'hello world'
            res = client.get('/hello')
            assert res.status_code == 200
            assert res.data == b'hello world'


class TestParameterTypeValidation:

    pass