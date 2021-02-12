import subprocess
import os
import time
from importlib import import_module


def run_foreground(cmd: str) -> None:
    """
    Run a bash command in foreground.

    Reference: http://blog.kagesenshi.org/2008/02/teeing-python-subprocesspopen-output.html

    Args:
        cmd: Bash command

    Returns:
        None
    """
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:
        line = p.stdout.readline()
        print(line.strip())
        if line == '' and p.poll() != None:
            break
    return None


def run_background(command: str) -> None:
    """
    Run a bash command in background.

    Args:
        command: Bash command

    Returns:
        None
    """
    subprocess.Popen(command, shell=True)


def jupyter() -> None:
    """
    Start a jupyter lab server using localtunnel.

    Returns:
        None
    """
    from google.colab import drive
    drive.mount('/content/drive')
    os.chdir('/content/drive/MyDrive/colab/')
    run_background('nohup pip install jupyterlab --upgrade -qqq &')
    command = 'nohup jupyter lab --notebook-dir="/content/drive/MyDrive/colab" --no-browser --allow-root --ip="0.0.0.0" --port="6006" &'
    run_background(command)
    time.sleep(5)
    run_foreground('npx localtunnel --port 6006')


def vscode(subdomain: str = 'amitness',
           port: int = 9000,
           config_save_path: str = '/content/drive/MyDrive/colab/.vscode') -> None:
    """
    Start VSCode server which persists all settings and extensions.

    Args:
        subdomain: Subdomain for localtunnel.
        port: Port for running code-server
        config_save_path: Path in Google Drive to save VSCode settings

    Returns:
        None
    """
    drive = import_module('google.colab.drive')
    drive.mount('/content/drive')
    subprocess.run(['curl', '-fsSL', 'https://code-server.dev/install.sh', '-O'])
    subprocess.run(['bash', 'install.sh', '--version', '3.5.0'])
    subprocess.run(['pip', 'install', 'pylint'])
    print(f'https://{subdomain}.loca.lt/?folder=/content/drive/MyDrive/colab')
    run_foreground(
        f'code-server --port {port} --auth none --disable-telemetry --force --user-data-dir {config_save_path} & npx localtunnel -p {port} -s {subdomain} --allow-invalid-cert')


def expose_port(port: int, path: str = '/') -> None:
    """
    Expose port as an external URL.

    The URL is only accessible to you and available till the notebook runs.

    Args:
        port: Port a service is running on
        path: Path the service is running on

    Returns:
        None
    """
    output = import_module('google.colab.output')
    output.serve_kernel_port_as_window(port, path=path)
