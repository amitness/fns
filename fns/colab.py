import subprocess
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
    p = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    while True:
        line = p.stdout.readline()
        print(line.strip())
        if line == "" and p.poll() is not None:
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


def jupyter(subdomain: str, port: int = 9003) -> None:
    """
    Start a jupyter notebook server using localtunnel.

    Returns:
        None
    """
    command = f"jupyter-notebook --ip='*' --no-browser --allow-root --port 9003 & npx localtunnel -p {port} -s {subdomain} --allow-invalid-cert"
    run_foreground(command)


def vscode(
    subdomain: str = "amitness",
    port: int = 9000,
    config_save_path: str = "/content/drive/MyDrive/colab/.vscode",
) -> None:
    """
    Start VSCode server which persists all settings and extensions.

    Args:
        subdomain: Subdomain for localtunnel.
        port: Port for running code-server
        config_save_path: Path in Google Drive to save VSCode settings

    Returns:
        None
    """
    drive = import_module("google.colab.drive")
    drive.mount("/content/drive")
    subprocess.run(["curl", "-fsSL", "https://code-server.dev/install.sh", "-O"])
    subprocess.run(["bash", "install.sh", "--version", "3.10.2"])
    subprocess.run(["pip3", "install", "flake8", "--user"])
    subprocess.run(["pip3", "install", "black", "--user"])
    print(f"https://{subdomain}.loca.lt/?folder=/content/drive/MyDrive/colab")
    run_foreground(
        f"code-server --port {port} --auth none --disable-telemetry --force --user-data-dir {config_save_path} & npx localtunnel -p {port} -s {subdomain} --allow-invalid-cert"
    )


def expose_port(port: int, path: str = "/") -> None:
    """
    Expose port as an external URL.

    The URL is only accessible to you and available till the notebook runs.

    Args:
        port: Port a service is running on
        path: Path the service is running on

    Returns:
        None
    """
    output = import_module("google.colab.output")
    output.serve_kernel_port_as_window(port, path=path)
