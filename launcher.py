import os
import subprocess
import time


def manageprocs(proclist):
    """Check a list of subprocesses for processes that have
       ended and remove them from the list.

    :param proclist: list of Popen objects
    """
    for pr in proclist:
        if pr.poll() is not None:
            proclist.remove(pr)
    # since manageprocs is called from a loop,
    # keep CPU usage down.
    time.sleep(0.5)


def main():

    # Read config file
    try:
        with open('./config.ini', 'r') as f:
            pathes = [path.strip() for path in f.readlines()]
    except FileNotFoundError:
        print("cant find config file")
        exit(1)

    # List of subprocesses
    procs = []
    # Do not launch more processes concurrently than your
    # CPU has cores.  That will only lead to the processes
    # fighting over CPU resources.
    maxprocs = os.cpu_count()
    # Launch all subprocesses.
    for path in pathes:
        while len(procs) == maxprocs:
            manageprocs(procs)
        procs.append(subprocess.Popen(path, shell=True))
    # Wait for all subprocesses to finish.
    while len(procs) > 0:
        manageprocs(procs)


if __name__ == '__main__':
    main()