# Flask-Fly (WIP)

Yet Another Restful Router For Flask Based On Type Hints.

## Quick look
```python
from flask import Flask
from flask_fly import Fly, Resource
flask = Flask(__name__)
fly = Fly(flask)
resource = Resource()

@resource.get("/hello")
def get_id(name: str):

    return "hello {}".format(name)

fly.add_resource(resource)
```

## Motivation
On Python 3.6 and newer, it has an perfect type hints system, which can specify the type of parameter and return value. This System is very useful for developer to take a quick look about the information of params.

Meanwhile, those annotations of parameters contain enough context for application to judge whether the variable passing in meets its type. And annotations can be used to generate the document of API.

Separating definition of parameters and the logic of controllers is important to the application's structure, and it's very useful to reuse codes and refactor them.

- [*] allow to specify where the parameter comes
- [ ] allow to specify the type of parameters
- [ ] allow to customize types(validator and transducer)
- [ ] marshall the return content
- [ ] blueprint for better project structure
- [ ] generate api document automatically
- [ ] support customized template of api document


## License
this project is under MIT license.