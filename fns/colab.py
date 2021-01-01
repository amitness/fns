import subprocess
import os
import time


def run_foreground(cmd):
    """from http://blog.kagesenshi.org/2008/02/teeing-python-subprocesspopen-output.html
    """
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:
        line = p.stdout.readline()
        print(line.strip())
        if line == '' and p.poll() != None:
            break
    return None


def run_background(command):
    subprocess.Popen(command, shell=True)


def jupyter():
    from google.colab import drive
    drive.mount('/content/drive')
    os.chdir('/content/drive/MyDrive/colab/')
    run_background('nohup pip install jupyterlab --upgrade -qqq &')
    command = 'nohup jupyter lab --notebook-dir="/content/drive/MyDrive/colab" --no-browser --allow-root --ip="0.0.0.0" --port="6006" &'
    run_background(command)
    time.sleep(5)
    run_foreground('npx localtunnel --port 6006')


def vscode(subdomain='amitness',
           port=9000,
           config_save_path='/content/drive/MyDrive/colab/.vscode'):
    from google.colab import drive
    drive.mount('/content/drive')
    subprocess.run(['curl', '-fsSL', 'https://code-server.dev/install.sh', '-O'])
    subprocess.run(['bash', 'install.sh', '--version', '3.5.0'])
    subprocess.run(['pip', 'install', 'pylint'])
    print(f'https://{subdomain}.loca.lt/?folder=/content/drive/MyDrive/colab')
    run_foreground(
        f'code-server --port {port} --auth none --disable-telemetry --force --user-data-dir {config_save_path} & npx localtunnel -p {port} -s {subdomain} --allow-invalid-cert')
