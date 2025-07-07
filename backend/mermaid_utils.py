import subprocess

def is_mermaid_installed():
    try:
        result = subprocess.run(['mmdc', '-h'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode == 0
    except FileNotFoundError:
        return False 