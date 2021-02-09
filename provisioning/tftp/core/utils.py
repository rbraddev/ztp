import os
import time

from jinja2 import Environment, FileSystemLoader, StrictUndefined
from ruamel.yaml import YAML


def render_file(template_path, template, **kwargs):
    env = Environment(
        loader=FileSystemLoader(template_path), undefined=StrictUndefined, trim_blocks=True, lstrip_blocks=True
    )
    template = env.get_template(template)
    return template.render(**kwargs)


def is_online(ip) -> bool:
    attempts = 0
    online = False
    while True:
        pingtest = os.popen(f'ping -c 3 {ip}')
        pingres = pingtest.read()
        if ', 0% packet loss' in pingres:
            online = True
            break
        elif attempts > 600:
            break
        time.sleep(1)
        attempts += attempts
    return online


def load_yaml(yaml_file: str):
    yaml = YAML(typ="safe")
    with open(yaml_file, "r") as f:
        data = yaml.load(f.read())
    return data
