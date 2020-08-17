import subprocess
#subprocess.check_output('git stash', shell=True)
direct_output = subprocess.check_output('cd /home/pi/Lights && git pull --all', shell=True)
#subprocess.check_output('git stash clear', shell=True)

if direct_output != b'Already up to date.\n' or direct_output != b'warning: redirecting to https://github.com/blurrydude/Lights.git/\nAlready up to date.\n':
    print('restarting')
    subprocess.check_output('reboot now', shell=True)
else:
    print('no restart required')