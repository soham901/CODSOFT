from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

import importlib as ilib

import os

routes = []
nav_links = []


def get_submodules(module: str):
    files = os.listdir(module)
    modules = []

    for file in files:
        if file not in ['__pycache__', '__init__.py'] and not file.endswith('.py'):
            modules.append(file)

    return modules


def remove_num_pre(module_name: str):
    try:
        module_name = module_name.split("_")[1]
    except Exception as e:
        pass
    return module_name


def load_sub_apps(app: FastAPI):
    global routes
    modules = get_submodules('src')

    try:
        for module in modules:
            sub_app = ilib.import_module(f'src.{module}.app')
            nav_links.append(module)
            module = remove_num_pre(module)
            app.mount(f'/{module}', sub_app.app)
            # app.add_api_route(f'/{module}', ilib.import_module(f'src.{module}.app').app, methods=['GET', 'POST'])
            routes.append(f'{module}')
            print(module, 'app mounted at', f'/{module}')

    # except ImportError:
    #     print('Error: Include an app.py file inside your own app.')

    except AttributeError:
        print('Error: Initialize a app object of FastAPI class from fastapi')


class Template:
    def __init__(self, package_name: str):
        if package_name and len(package_name.split(".")) >= 2:
            self.sub_template_path = package_name.split(".")[1]
        else:
            self.sub_template_path = ''
        self.templates = Jinja2Templates(directory='templates')

    def render(self, path: str, context: {'request': Request}):
        path = f'{self.sub_template_path}/{path}' if self.sub_template_path else path
        return self.templates.TemplateResponse(path, context=context)


def get_routes():
    global routes, nav_links
    links = sorted(nav_links)
    for idx in range(len(links)):
        links[idx] = remove_num_pre(links[idx])
    return links
