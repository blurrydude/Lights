import subprocess
#subprocess.check_output('cd /home/pi/Lights', shell=True)
subprocess.check_output('git stash', shell=True)
direct_output = subprocess.check_output('git pull', shell=True)
subprocess.check_output('git stash clear', shell=True)
#subprocess.check_output('reboot', shell=True)
print(direct_output)