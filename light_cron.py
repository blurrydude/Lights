import subprocess
#subprocess.check_output('cd /home/pi/Lights', shell=True)
subprocess.check_output('git stash', shell=True)
direct_output = subprocess.check_output('git pull', shell=True)
subprocess.check_output('git stash clear', shell=True)

if direct_output!=b'Already up to date.\n':
    print('restarting')
    #subprocess.check_output('reboot', shell=True)