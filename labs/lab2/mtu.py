import click
import subprocess
import platform

MINIMAL_MTU = 68
MAXIMAL_MTU = 1500

def ping_mtu(destination, size):
    if platform.system().lower() == "windows":
        command = ['ping', destination, '-n', '1', '-M', 'do', '-s', str(size - 28)]
    if platform.system().lower() == "darwin":
        command = ['ping', destination, '-c', '1', '-D', '-s', str(size - 28)]
    else:
        command = ['ping', destination, '-c', '1', '-M', 'do', '-s', str(size - 28)]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.returncode == 0

@click.command()
@click.argument('destination', type=str, required=True)
def find_mtu(destination):
    if not ping_mtu(destination, MINIMAL_MTU):
        print("Can't ping destination service with minimal mtu")
        exit(1)

    l = MINIMAL_MTU
    r = MAXIMAL_MTU + 1
    while r - l > 1:
        mid = (r + l) // 2
        print(f"Checking {mid}...", end=' ', flush=True)
        if ping_mtu(destination, mid):
            print("Success")
            l = mid
        else:
            print("Failure")
            r = mid

    print(f'MTU is {l}')

if __name__ == '__main__':
    find_mtu()
