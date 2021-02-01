from jinja2 import Environment, FileSystemLoader, StrictUndefined


def render_file(template_path, template, **kwargs):

    env = Environment(
        loader=FileSystemLoader(template_path),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True
    )

    template = env.get_template(template)
    return template.render(**kwargs)
