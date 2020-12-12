import sys
import time
import multiprocessing
import subprocess

'''
ogni x minuti o x processi
killall /opt/google/chrome/chrome
killall chromedriver
per scaricare la macchina
'''
MAX_NEW_PROCS=1 #formerly 3
MAX_PROCS=50
RED_CODE_SIGNAL = 20 #formerly 12, 10
RED_CODE_PROCS = 66 #formerly 57, 100

def browse(config, user_config):
        global MAX_NEW_PROCS
        procs =  subprocess.check_output("ps -C chrome --no-headers | wc -l", shell=True)
        try:
                procs = int(procs)
        except:
                procs = 0

        print "chrome processes: " + str(procs) + "\n"

        #memory leaks try to fix it
        if procs > RED_CODE_PROCS:
                killAll()
        
        if procs > RED_CODE_SIGNAL:
                MAX_NEW_PROCS = 1

        if procs < MAX_PROCS:
                #print "max n. of chrome processes " + str(MAX_PROCS) + " reached...killing all"
                #subprocess.call("killall /opt/google/chrome/chrome", shell=True)
                #subprocess.call("killall chromedriver", shell=True)
                for x in range(0, MAX_NEW_PROCS):
                        subprocess.Popen(['python', 'test_login.py', config, user_config])
        else:
                print "waiting for next free process...\n"

        #try to speed up <--probably a bad idea
        if procs == 0:
                MAX_NEW_PROCS += 1

        print "MAX_NEW_PROCS is now " + str(MAX_NEW_PROCS) +"\n" 

def killAll():
        global MAX_NEW_PROCS
        MAX_NEW_PROCS = 1
        print "max n. of chrome processes " + str(RED_CODE_PROCS) + " reached or exit signal given...killing all"
        subprocess.call("killall /opt/google/chrome/chrome", shell=True)
        subprocess.call("killall chromedriver", shell=True)

starttime=time.time()

try:
        config = "fullcourse.json"
        user_config = "users.csv"
        if len(sys.argv) == 2:
                config = sys.argv.pop()
        elif len(sys.argv) == 3:
                config = sys.argv.pop(1)
                user_config = sys.argv.pop()
        print '''
                   _                   _             _    
                  (_)                 | |           | |   
 ___  ___  ___ ___ _  ___  _ __    ___| |_ __ _ _ __| |_  
/ __|/ _ \/ __/ __| |/ _ \| '_ \  / __| __/ _` | '__| __| 
\__ \  __/\__ \__ \ | (_) | | | | \__ \ || (_| | |  | |_  
|___/\___||___/___/_|\___/|_| |_| |___/\__\__,_|_|   \__| 
                                                          
                                                          
'''
        
        while True:
                browse(config, user_config)
                time.sleep(60.0 - ((time.time() - starttime) % 60.0))
except (KeyboardInterrupt, SystemExit):
        killAll()
        raise
except:
        print "interupt signal...exiting as requested"

