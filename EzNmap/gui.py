#!/bin/env python

from tkinter import *
from subprocess import PIPE, Popen, check_output
import sys

frame = Tk()
frame.geometry("1400x800")
frame.title("EzNmap")

scanType = IntVar()
fileType = IntVar()
verbosity = IntVar()

ipLabel = Label(
    text="Please enter the IP(s) you wish to scan \n • Input can be single IP address or a network using CIDR notation \n • Ex. 192.168.1.105 or 192.168.1.0/24",
    font=("Helvetica",14),
    bd=1, 
    justify="left"
).grid(row=0, column=0)

ip = Entry(frame, width=50)
ip.insert(0,"Ip Address")
ip.grid(row=1,column=0, pady=(10,10))

portLabel = Label(
    text="Which port(s) would you like to scan? Leave blank for top 1000 ports \n • Input can be a single port or a range of ports \n • Ex. 20 or 0-100\n",
    font=("Helvetica",13),
    bd=1, 
    justify="left"
).grid(row=0, column=1, padx=(10,10),pady=(25,10))

port = Entry(frame, width=50)
port.insert(0,"Ports")
port.grid(row=1, column=1, pady=(10,10))

scanLabel = Label(
    text="Run a version scan, operating system scan, or both? \n NOTE: You must have root permissions to run OS scan ",
    font=("Helvetica",14),
    bd=1, 
    justify="left"
).grid(row=2, column=0, pady=(10,10))

Radiobutton(frame, text="Version Scan", variable=scanType, value=1).grid(row=3, column=0)
Radiobutton(frame, text="OS Scan", variable=scanType, value=2).grid(row=4, column=0)
Radiobutton(frame, text="Both", variable=scanType, value=3).grid(row=5, column=0, pady=(0,15))

speed = Scale(frame,label="Scan Speed", from_=0, to=5, orient=HORIZONTAL)
speed.set(3)
speed.grid(row=2,column=1, pady=(20,10))

fileLabel = Label(
    text="Save output to a file? Leave blank if no",
    font=("Helvetica",14),
    bd=1, 
    justify="left"
).grid(row=6, column=0, pady=(10,10))

fileName = Entry(frame, width=50)
fileName.insert(0,"File Name (if saving output)")
fileName.grid(row=7, column=0, pady=(10,10))

typeLabel = Label(
    text="Save as a text file or XML file?",
    font=("Helvetica",14),
    bd=1, 
    justify="left"
).grid(row=6, column=1, pady=(10,10))

Radiobutton(frame, text="Text File", variable=fileType, value=1).grid(row=7, column=1)
Radiobutton(frame, text="XML File", variable=fileType, value=2).grid(row=8, column=1)
verboseLabel = Label(

text="Select verbosity level",
    font=("Helvetica",14),
    bd=1, 
    justify="left"
).grid(row=9,column=0, pady=(10,10))
Radiobutton(frame, text="Default", variable=verbosity, value=1).grid(row=10,column=0)
Radiobutton(frame, text="Verbose", variable=verbosity, value=2).grid(row=11, column=0)
Radiobutton(frame, text="Very Verbose", variable=verbosity, value=3).grid(row=12, column=0)

def clearip(e):
    ip.delete(0, END)
def clearPort(e):
    port.delete(0, END)
def clearFile(e):
    fileName.delete(0, END)

ip.bind("<Button-1>", clearip)
port.bind("<Button-1>", clearPort)
fileName.bind("<Button-1>", clearFile)


command=""

def getFlags():
    return {
        1 : "-sV",
        2 : "-O",
        3 : "-sV -O"
    }.get(scanType.get())

def getVerbose():
    return {
        1: "",
        2: "-v",
        3: "-vv"
    }.get(verbosity.get())

def getSpeed():
    return "-T"+str(speed.get())

def getFile():
    name = fileName.get()
    ftype = ""
    if(name=="" or name=="File Name (if saving output)"):
        return ""
    if(fileType==1):
        ftype = "-oN"
    if(fileType==2):
        ftype = "-oX"
    return ftype+" "+name

def myClick():
    global command
    command += ip.get()+" "
    ports = port.get()
    if(ports=="" or ports=="Ports"):
        command+=""
    else:
        command += ports+" "
    command += getFlags()+" "
    command += getSpeed()+" "
    command += getVerbose()+" "
    command += getFile()+" "
    print(command)
    nmap = Popen(["nmap",command], stdout=PIPE)
    res = check_output(["cat"], stdin=nmap.stdout).decode("utf-8")
    print(res)
    for widget in frame.winfo_children():
        widget.destroy()
    results = Label(
    text=res,
    font=("Helvetica",16),
    bd=1, 
    justify="left"
    ).pack()
    nmap.terminate()
    

b = Button(frame, text="Scan", command=myClick, padx=20, pady=20).grid(row=13, column=1)

frame.mainloop()