#!/bin/env python

import os

#Creates global variables used to craft command
ip = None
ports =  None
flags = None
output = None

#asks user for IP address input and saves it to the ip variable
def askIP():
   global ip 
   ip = input("Please enter the IP(s) you wish to scan \n • Input can be single IP address or a network using CIDR notation \n • Ex. 192.168.1.105 or 192.168.1.0/24 \n")
   return

#asks user for port input and saves it to the port variable
def askPort():
    global ports
    answer = input("Which port(s) would you like to scan? Leave blank for top 1000 ports \n • Input can be a single port, a range of ports, top 100 ports, or all ports. \n • Ex. 20 or 0-100 or top or all \n")
    ports = portInput(answer)
    return

#asks user for service, os, and scan speed input. Parses the input and stores in flags variable
def askFlag():
    global flags
    answers= []

    answers.append(input("Scan for Services and Versions? y/n \n"))
    answers.append(input("Scan for Operating System? y/n \n NOTE: You must have root permissions to run OS scan \n"))
    answers.append(input("Choose a scan speed \n • Input must be a number between 0 and 5 \n • The faster the scan the more likely it will be detected \n"))
    flags = flagInput(answers)
    return

#asks user if they want to save the output. If yes, prompts user to choose file type, file name, and verbosity. then stores answers into output variable
def askFileName():
    global output

    answer = input("Would you like to save the output? y/n \n")
    if(answer == "y"):
        fileType = input("What type of file would you like to create? \n • Options are: txt or xml \n")
        fileName = input("Enter a name for the file \n")
        fileVerbose = input("how verbose would you like the output to be? \n • Input must be 'v' for verbose, 'vv' for very verbose, or blank for default \n")
        output = fileInput(fileType, fileName, fileVerbose)
    else:
        output=""
    return

#converts user input regarding ports into nmap flags
def portInput(x):
    return {
        'top': '-F',
        'all': '-p-',
        '': ''
    }.get(x.lower(), "-p "+x)

#converts user input regarding flags into nmap flags
def flagInput(x):
    flags=""
    if(x[0] == 'y'):
        flags+= '-sV '
    if(x[1] == 'y'):
        flags+= '-O '
    flags += "-T"+x[2]
    return flags

#converts user input regarding output options into nmap flags
def fileInput(ftype, name, verb):
    if(verb !=""):
        verb = "-"+verb

    if(ftype == "txt"):

        return verb + " -oN "+name+" "

    if(ftype == "xml"):

        return verb + " -oX "+name+" "

 #runs the program by calling other functions, retrieving input from global variables, and crafting the command before feeding it to nmap   
def main():
    os.system("cat art.txt")
    command = "nmap "
    print("Welcome to EzNmap! \n")
    askIP()
    command += ip
    askPort()
    command += " "+ports
    askFlag()
    command += " "+flags
    askFileName()
    command += " "+output
    print("Running command: "+command+" ... \n")


    os.system(command)




    print("Finished")
if __name__=="__main__":
	main()