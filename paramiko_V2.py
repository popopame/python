import paramiko
import time

#Ask the user all the ID , and command to launch
user =input("Please enter user name: ")
ipv4 = input("Please enter the IP of the server: ")
pem_path=input("Please enter the Path to the pem key: ")
pem = paramiko.RSAKey.from_private_key_file(pem_path)
command=input("What is the command you wan to launch , type exit when you want to exit the script  : ")

while command != "exit" :
    #Create a connection and execute a command
    session = paramiko.SSHClient()
    session.set_missing_host_key_policy(paramiko.AutoAddPolicy()) #Auto add policy to avoid error on connection
    session.connect(hostname=ipv4, username=user ,pkey=pem)
    stdin, stdout, stderr = session.exec_command(command)

    #Store the stdout in a variable , so it can be used several times , the .decode and .strip make the result more readable and writable in a file by decoding in utf-8
    result=str(stdout.read().decode('utf-8').strip("\n"))


    #Write all the results in a file , the name of the file will be command + time we also test if the string has a \ or / in it , if so , we modify the name of the file to avoid errors
    if '/' in command:
        out_file = open("c:\python\output\command %s.txt" % (time.strftime("%m%d-%H%M")), "w+")
    else:
        out_file= open("c:\python\output\%s %s.txt"%(command , time.strftime("%m%d-%H%M")),"w+")


    out_file.write(result)
    out_file.close()

    command = input("What is the command you wan to launch , type exit when you want to exit the script  : ")

print("GoodBye!")