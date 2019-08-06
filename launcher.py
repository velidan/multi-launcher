import threading
import subprocess

def executeFile(file_path):
    subprocess.call(file_path, shell=True)


def main():
    file = None

    try:
        file = open('./config.ini', 'r');
    except:
        # TODO: add alert widget
        print("cant find a file")

    pathes = [ path.strip() for path in file.readlines() ]

    try:
        for idx in range(len(pathes)):
            print(pathes[idx])
            file_path = pathes[idx];
            newThread = threading.Thread(target=executeFile, args=(file_path,))
            newThread.daemon = True
            newThread.start()
    except:
        print("cant start thread")


if __name__ == '__main__':
    main()
    input("Press enter to exit ;)")