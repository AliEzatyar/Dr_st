import multiprocessing as mps
import subprocess


def start_server(domain, port):
    # calling the system to run the manage.py
    command = f" D:\\Tutorials\\PROGRAMMING\\Python\\django\\django_envir\\Scripts\\python.exe manage.py runserver {domain}:{port}"
    command = command.split()
    subprocess.run(command)
    print("function was called")


if __name__ == '__main__':
    # making processes
    for i in range(1, 2):
        domain_port = input("enter domain:port -> ").split(":")
        process = mps.Process(target=start_server, args=(domain_port[0], int(domain_port[1])))
        process.start()
        print(f"Server {i} has been started")
#
