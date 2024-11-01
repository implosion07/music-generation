import paramiko

import subprocess

# server1
#command = "ssh -A bath"
#result = subprocess.run(command, shell=True, capture_output=True, text=True)

# Check the command output
#if result.returncode == 0:
 #   print("Command executed successfully.")
  #  print("Command output:")
   # print(result.stdout)
#else:
 #   print("Command failed.")
  #  print("Error message:")
   # print(result.stderr)

"""# Server 1 details
server1_ip = 'server1_ip_address'
server1_username = 'server1_username'
server1_password = 'server1_password'

# Server 2 details
server2_ip = 'server2_ip_address'
server2_username = 'server2_username'
server2_password = 'server2_password'
"""
"""# Connect to Server 1 via SSH
server1_ssh = paramiko.SSHClient()
server1_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
server1_ssh.connect(server1_ip, username=server1_username, password=server1_password)

# Execute script1.py on Server 1
stdin, stdout, stderr = server1_ssh.exec_command('python3 /path/to/script1.py')
print(stdout.read().decode())
print(stderr.read().decode())

# Close SSH connection to Server 1
server1_ssh.close()"""

print("Starting processes.......")
print("Current server: bath")
# server1
command = "python music_gen_model_s1.py"
result = subprocess.run(command, shell=True, capture_output=True, text=True)
#if result.returncode == 0:
 #   print("Command executed successfully.")
  #  print("Command output:")
   # print(result.stdout)
#else:
 #   print("Command failed.")
  #  print("Error message:")
   # print(result.stderr)

# server2
#command = "ssh -A dorchester"
#result = subprocess.run(command, shell=True, capture_output=True, text=True)

# Check the command output
#if result.returncode == 0:
 #   print("Command executed successfully.")
  #  print("Command output:")
   # print(result.stdout)
#else:
 #   print("Command failed.")
  #  print("Error message:")
   # print(result.stderr)

print("Current server : dorchester")

# server2
#command = "python music_gen_model_s2.py"
#result = subprocess.run(command, shell=True, capture_output=True, text=True)
#if result.returncode == 0:
 #   print("Command executed successfully.")
  #  print("Command output:")
   # print(result.stdout)
#else:
 #   print("Command failed.")
  #  print("Error message:")
   # print(result.stderr)
"""
# Connect to Server 2 via SSH
server2_ssh = paramiko.SSHClient()
server2_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
server2_ssh.connect(server2_ip, username=server2_username, password=server2_password)

# Execute script2.py on Server 2
stdin, stdout, stderr = server2_ssh.exec_command('python3 /path/to/script2.py')
print(stdout.read().decode())
print(stderr.read().decode())

# Close SSH connection to Server 2
server2_ssh.close()"""
