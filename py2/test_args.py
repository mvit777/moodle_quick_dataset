import unittest
import sys
import os
import time
import random
import string
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
import config

class MoodleLogin(unittest.TestCase):
    CONFIGS = []
    config = "fullcourse.json"
    user_config = "users.cvs"
    moodle_config = {}

    def setUp(self):
        self.CONFIGS = my_args
        if len(self.CONFIGS) >= 1:
            self.config = self.CONFIGS[0]
        if len(self.CONFIGS)==2:
            self.user_config = self.CONFIGS[1]

    def test_args(self):
        print "moodle_confg file is " + self.config
        print "users list file is " + self.user_config
        self.loadConfig()

    def loadConfig(self):
        self.moodle_config = config.load(self.config)
        self.moodle_config['general']['6'] = self.user_config
        print self.moodle_config['general']['6']
        line = config.loadRandomLine(self.user_config).split(",")
        print line
        return self.moodle_config
        

        
    def tearDown(self):
        pass

if __name__ == "__main__":
    my_args = []
    if len(sys.argv) == 2:
        my_args.append(sys.argv.pop())
    elif len(sys.argv) == 3:
        my_args.append(sys.argv.pop(1))
        my_args.append(sys.argv.pop())

    unittest.main()