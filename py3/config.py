import sys
import os
import json
from  jsonmerge import merge
import random

banner = '''
                           _                   _             _    
                          (_)                 | |           | |   
         ___  ___  ___ ___ _  ___  _ __    ___| |_ __ _ _ __| |_  
        / __|/ _ \/ __/ __| |/ _ \| '_ \  / __| __/ _` | '__| __| 
        \__ \  __/\__ \__ \ | (_) | | | | \__ \ || (_| | |  | |_  
        |___/\___||___/___/_|\___/|_| |_| |___/\__\__,_|_|   \__| 
                                                                  
                                                                  
        '''


CONFIG_DIR = "configs/"

def load(config, preserve_path=False):
    fullpath = config
    if preserve_path==False:
        fullpath = CONFIG_DIR + config
        
    print("using " + fullpath  + "\n")
    with open(fullpath) as f:
        _config = json.load(f)
        f.close()
        return _config

def loadRandomLine(user_file):
    fp = open(user_file) 
    line = random.choice(fp.readlines())
    fp.close()
    return line

class MoodleConfig(object):
    CONFIGS = []
    general_config = "general.json"
    config = "fullcourse.json"
    user_config = "users.csv"
    header_config = {}
    course_config = {}
    moodle_config = {}

    def __init__(self):
        self.CONFIGS = my_args
        if [] == self.CONFIGS:
            print("no config file specified falling back to default " + CONFIG_DIR + self.config + " file")
            print("with default " + CONFIG_DIR + self.user_config + " file")
        if len(self.CONFIGS) >= 1:
            self.config = self.CONFIGS[0]
        if len(self.CONFIGS)==2:
            self.user_config = self.CONFIGS[1]
        self.getArgs()

    def getArgs(self):
        print("moodle_confg file is " + CONFIG_DIR + self.config)
        print("users list file is " + CONFIG_DIR + self.user_config)

    def loadConfig(self):
        self.header_config = load(self.general_config)
        self.course_config = load(self.config)
        self.moodle_config = merge(self.header_config, self.course_config)
        self.moodle_config['general']['6'] = CONFIG_DIR + self.user_config
        #print(self.moodle_config)
        return self.moodle_config

    def getStudent(self):
        line = loadRandomLine(CONFIG_DIR + self.user_config).split(",")
        return line

my_args = []
if len(sys.argv) == 2:
    my_args.append(sys.argv.pop())
elif len(sys.argv) == 3:
    my_args.append(sys.argv.pop(1))
    my_args.append(sys.argv.pop())