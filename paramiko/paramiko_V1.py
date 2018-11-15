import paramiko

#Ask the user all the ID , but the 
user =input("Please enter user name: ")
ipv4 = input("Please enter the IP of the server: ")
pem_path=input("Please enter the Path to the pem key: ")
pem = paramiko.RSAKey.from_private_key_file(pem_path)


#Create a connection and execute a command
session = paramiko.SSHClient()
session.set_missing_host_key_policy(paramiko.AutoAddPolicy()) #Auto add policy to avoid error on connection
session.connect(hostname=ipv4, username=user ,pkey=pem)
stdin, stdout, stderr = session.exec_command("docker container ls")

#Store the stdout in a variable , so it can be used several times , the .decode and .strip make the result more readable and writable in a file by decoding in utf-8
result=str(stdout.read().decode('utf-8').strip("\n"))


#Write all the results in a file
out_file= open("c:\python\output\V2.txt","r+")
out_file.write(result)
out_file.close()


print(result)