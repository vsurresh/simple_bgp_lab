
from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_configure
from nornir_utils.plugins.functions import print_result
from nornir_jinja2.plugins.tasks import template_file

def render_config(task):
    template = 'config.j2'
    result = task.run(task=template_file, template=template, path='config_templates/', **task.host)
    rendered_config = result[0].result
    task.host['rendered_config'] = rendered_config

def napalm_send_config(task):
    host = task.host
    config = host['rendered_config']
    task.run(task=napalm_configure, configuration=config, dry_run=False)

nr = InitNornir(config_file='config.yml')
result = nr.run(task=render_config)
result1 = nr.run(task=napalm_send_config)

print_result(result1)