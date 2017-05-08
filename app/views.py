import socket
from importlib import import_module
import logging as log

from app import app


@app.route('/')
@app.route('/index')
def index():
    return 'Hello, World!'


@app.route('/test')
def test():
    return 'Test'


@app.route('/<operation>/<action>', methods=['GET', 'POST'])
def do_action(operation=None, action=None):
    module_name = 'app.operations.%s.operation' % operation
    operation_name = '%sOperation' % operation
    try:
        imported_module = import_module(module_name)
        imported_class = getattr(imported_module, operation_name)
        _instance = imported_class()
        return getattr(_instance, action)()
    except (ImportError, AttributeError) as e:
        log.warn('Are you sure you have created the method/Class %s' %e)
        return '<i>404: Invalid URL</i>'
