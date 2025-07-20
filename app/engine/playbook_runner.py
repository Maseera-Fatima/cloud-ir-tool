import yaml, json
from jinja2 import Template
from app.cloud_actions import azure_actions

ACTION_MAP = {
    "isolate_vm": azure_actions.isolate_vm,
    "snapshot_disk": azure_actions.snapshot_disk,
    "revoke_user_access": azure_actions.revoke_user_access
}

def load_playbook(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def load_incident(path):
    with open(path, 'r') as f:
        return json.load(f)

def render_param(template_str, context):
    return Template(template_str).render(incident=context)

def run_playbook(playbook_path, incident):
    playbook = load_playbook(playbook_path)
    steps = playbook['steps']
    for step in steps:
        action = step['action']
        params = {
            key: render_param(value, {"incident": incident})
            for key, value in step['parameters'].items()
        }
        func = ACTION_MAP.get(action)
        if func:
            func(**params)
        else:
            print(f"[ERROR] Unknown action: {action}")
