#!/usr/bin/env python

from flask import Flask
from flask_socketio import SocketIO
import os
import importlib.util
import json
import html


class Plugins:
    def __init__(self):
        plugin_names = os.listdir('plugins')
        self._plugins = {}
        for plugin_name in plugin_names:
            if plugin_name == '__init__.py':
                continue
            file_path = os.path.join('plugins', plugin_name)
            module_name = os.path.splitext(plugin_name)[0]
            spec = importlib.util.spec_from_file_location(module_name,
                                                          file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            plugin_name = module.plugin_name
            self._plugins[plugin_name] = module.__getattribute__(plugin_name)()


with open('blns.json') as f:
    strings = json.load(f)

app = Flask("nutty_string")
app.config["SECRET_KEY"] = "secret"
socketio = SocketIO(app)
plugins = Plugins()


@socketio.on("request-test-suites")
def handle_request_test_suites(data):
    plugin_text = ''.join(f'<option id="suite" value="{k}">{html.escape(v.name, True)}</option>' for k, v in plugins._plugins.items())
    socketio.emit("test-suites", {"data": plugin_text})


@socketio.on("request-tests")
def handle_request_tests(data):
    tests = ''.join(f'<option id="test" value="{k}">{html.escape(k)}</option>' for k in plugins._plugins[data["data"]].tests)
    socketio.emit("tests", {"data": tests})


@socketio.on('request-strings')
def handle_get_strings(data):
    result = ''.join(f'''<tr id="srow" value="{i}">
                        <th style="width: min-content">{i}</th>
                        <td style="width: auto"><p class="text-truncate">{html.escape(s, True)}</p></td>
                        <td style="width: min-content">
                            <div class="btn-group">
                                <button id="spass" id="{i}" type="button" class="btn btn-success">Pass</button>
                                <button id="sfail" id="{i}" type="button" class="btn btn-danger">Fail</button>
                            </div>
                        </td>
                     </tr>''' for i, s in enumerate(strings))
    socketio.emit('strings', {'data': result})


@socketio.on('run')
def handle_run(data):
    plugins._plugins[data['suite']].tests[data['test']](strings[int(data['id'])])


@socketio.on('start')
def handle_start(data):
    plugins._plugins[data['suite']].setup()


if __name__ == "__main__":
    socketio.run(app)
