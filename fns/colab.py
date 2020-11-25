import subprocess


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
    command = 'nohup jupyter notebook --no-browser --allow-root --ip="127.0.0.1" --port="6006" &'
    run_background(command)
    run_foreground('npx localtunnel --port 6006')
