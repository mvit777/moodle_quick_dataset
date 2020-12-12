import sys
import os
import json
import random



def load(config):
    print "using " + config  + "\n"
    with open(config) as f:
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
    config = "fullcourse.json"
    user_config = "users.csv"
    moodle_config = {}

    def __init__(self):
        self.CONFIGS = my_args
        if [] == self.CONFIGS:
            print "no config file specified falling back to default " + self.config + " file"
            print "with default " + self.user_config + " file"
        if len(self.CONFIGS) >= 1:
            self.config = self.CONFIGS[0]
        if len(self.CONFIGS)==2:
            self.user_config = self.CONFIGS[1]
        self.getArgs()

    def getArgs(self):
        print "moodle_confg file is " + self.config
        print "users list file is " + self.user_config
        #self.loadConfig()

    def loadConfig(self):
        self.moodle_config = load(self.config)
        self.moodle_config['general']['6'] = self.user_config
        #print self.moodle_config['general']['6']
        return self.moodle_config

    def getStudent(self):
        line = loadRandomLine(self.user_config).split(",")
        #print line
        return line

my_args = []
if len(sys.argv) == 2:
    my_args.append(sys.argv.pop())
elif len(sys.argv) == 3:
    my_args.append(sys.argv.pop(1))
    my_args.append(sys.argv.pop())

#print moodle_config['general']['1']
'''
#MOODLE_BASEURL= "http://moodle36.localhost/"
moodle_config = {
    'debug': False,
    'general': [MOODLE_BASEURL,
                "mymoodle36", # site title
                "Log in to the site", # login page title
                "Available courses", # Course List title
                "Log in", # login link
                "Ciao_777_", # default password for all users
                "users.csv", # user list file
                "Site home", # the title of the site home
                "Edit profile" # profile edit link
                ],
    'students': {'groups': 
                    {
                        'elite': {
                            'bonus' : 1, # to add at every dice result
                            'retry': 2 # number of re-tries
                        },
                        'intermediate': {
                            'bonus': 0,
                            'retry': 1
                        },
                        'problematic': {
                            'bonus': -1,
                            'retry': 0
                        }
                    },
                  'profpic_threeshold':
                    {
                      'elite': 3,
                      'intermediate': 3,
                      'problematic': 4
                    }
                },
    'courses': {
        'list': ['course1','course2'],
        'default_slide_delay': 5,
        'scorm':{
            'button_enter': "//input[@value='Enter']",
            'button_advance': "(//button[@type='button'])[7]"
        }
    },
    'course1':{
        'title': 'corso1', # link to enter course
        'url': MOODLE_BASEURL + 'course/view.php?id=2',
        'browsemethod': 'navigateByLinks', # navigateByLinks|navigateBySchema(not implemented)|navigateByMoodleapi(not implemented)
        'paths': {
                'programma':{
                    'res_title': 'Programma',
                    'res_type': 'reading',
                    'res_link': "//li[@id='module-3']/div/div/div[2]/div/a/span",
                    'res_link_type': 'by_xpath'
                },
                'introduzione':{
                    'res_title': 'Introduzione',
                    'res_type': 'scorm',
                    'res_link': "//li[@id='module-4']/div/div/div[2]/div/a/span",
                    'res_link_tipe': 'by_xpath',
                    'slides': 28, 
                    'slide_delay': 5
                },
                'modulo4':{
                    'res_title': 'Modulo 6',
                    'res_type': 'scorm',
                    'res_link': "//li[@id='module-8']/div/div/div[2]/div/a/span",
                    'res_link_tipe': 'by_xpath',
                    'slides': 80, 
                    'slide_delay': 5
                }
            }, # link to resources (scorm, pdf, quiz etc)
        'threeshold':{
            'elite': 2,
            'intermediate': 3,
            'problematic': 5
        }
    },
    'course2':{
        'title': 'corso2', # link to enter course,
        'url': MOODLE_BASEURL + 'course/view.php?id=3',
        'browsemethod': 'navigateByLinks', 
        'paths': {
            
        }, # link to resources (scorm, pdf, quiz etc)
        'threeshold':{
            'elite': 2,
            'intermediate': 3,
            'problematic': 5
        }
    }

}
'''