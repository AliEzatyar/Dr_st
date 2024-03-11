import multiprocessing as mps
import os
import subprocess
import tkinter as tk

processes = {}
# labels and entries to take servers
x = tk.Tk()
# buttons
start1 = tk.Button(x, text="Start", command=lambda: add(en1.get(),"s1"))
start1.grid(row=1, column=2)
start2 = tk.Button(x, text="Start", command=lambda: add(en2.get(),"s2"))
start2.grid(row=2, column=2)
startall = tk.Button(x, text="Stop all", command=lambda: stop())


def start_server(domain, port):
    # calling the system to run the manage.py
    command = f" D:\\Tutorials\\PROGRAMMING\\Python\\django\\django_envir\\Scripts\\python.exe manage.py runserver {domain}:{port}"
    command = command.split()
    x = subprocess.run(command)


def add(domain_port,s_number):
    # making processes
    domain_port = domain_port.split(":")
    process = mps.Process(target=start_server, args=(domain_port[0], int(domain_port[1])))
    process.start()
    processes[str(process)] = process.pid
    if s_number == "s1":
        start1.config(command=lambda : stop(process=process,s_number="s1"),text="Stop")
    if s_number == "s2":
        start2.config(command=lambda : stop(process=process,s_number="s2"),text="Stop")

def stop(s_number="none",process=None, all=True):
    if all:
        for pro in processes:
            os.kill(processes[pro], 0)
    else:
        processes[process].kill()
        print("process was finished")
        if s_number == "s1":
            start1.config(command=lambda: stop(process=process), text="Start")
        if s_number == "s2":
            start2.config(command=lambda: stop(process=process), text="Start")


# labels
wlcm = tk.Label(x, text="Weclome, you can run several servers")
wlcm.grid(row=0, columnspan=3)
ser1 = tk.Label(x, text="server1")
ser1.grid(row=1, column=0)
ser2 = tk.Label(x, text="server2")
ser2.grid(row=2, column=0)

# entries
en1 = tk.Entry(x, )
en1.insert(0, "127.0.0.1:8080")
en1.grid(row=1, column=1)
en2 = tk.Entry(x, )
en2.insert(0, "192.168.43.137:8080")
en2.grid(row=2, column=1)

startall.grid(row=3, columnspan=3)

if __name__ == "__main__":
    x.mainloop()
