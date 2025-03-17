from jinja2 import Environment, FileSystemLoader


class TemplateHandler:
    """Клас для роботи з шаблонами Jinja2."""

    def __init__(self, template_path):
        self.env = Environment(loader=FileSystemLoader("."))
        self.template = self.env.get_template(template_path)

    def render(self, **kwargs):
        output = self.template.render(**kwargs)
        return output.encode("utf-8")
