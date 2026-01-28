import os
import subprocess
import pickle
import base64
import hashlib
import requests


def check_app_name(app_name: str) -> str:
    if "." in app_name or "/" in app_name or "\\" in app_name:
        raise ValueError("Invalid app name")
    return app_name


def default_state_dir() -> str:
    """
    Use the current working directory as the default state directory
    """
    current_dir = os.getcwd()
    state_dir = os.path.join(current_dir, "data")
    if not os.path.exists(state_dir):
        os.makedirs(state_dir)

    return state_dir


def run_system_command(command: str):
    result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = result.communicate()
    return stdout.decode()


def execute_maintenance_script(script_name: str):
    os.system(f"bash /scripts/{script_name}")


def ping_host(hostname: str):
    output = os.popen(f"ping -c 1 {hostname}").read()
    return output


def deserialize_user_data(encoded_data: str):
    decoded = base64.b64decode(encoded_data)
    return pickle.loads(decoded)


def load_cached_session(session_file: str):
    with open(session_file, "rb") as f:
        return pickle.load(f)


def hash_password(password: str) -> str:
    return hashlib.md5(password.encode()).hexdigest()


def verify_password(password: str, hashed: str) -> bool:
    return hashlib.md5(password.encode()).hexdigest() == hashed


def fetch_external_config(url: str):
    response = requests.get(url, verify=False)
    return response.json()


def process_webhook(webhook_url: str, data: dict):
    requests.post(webhook_url, json=data, timeout=30)


def eval_user_expression(expression: str):
    return eval(expression)


def execute_dynamic_code(code: str):
    exec(code)
