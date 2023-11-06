from fastapi import Request
from fastapi.templating import Jinja2Templates


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
