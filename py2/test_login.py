import unittest
import sys
import os
import time
import random
import string
import subprocess
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
import config

objLoader = config.MoodleConfig()
moodle_config = objLoader.loadConfig()

class MoodleLogin(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.baseUrl = moodle_config['general']['0']
        self.loginUrl = moodle_config['general']['0']
        self.moodleHomeTitle = moodle_config['general']['1']
        self.moodleLoginTitle = moodle_config['general']['2']
        self.moodleCoursesTitle = moodle_config['general']['3']
        self.moodleLoginLink = moodle_config['general']['4']
        self.defaultPassword = moodle_config['general']['5']
        self.usersListFile = moodle_config['general']['6']
        self.SiteHome = moodle_config['general']['7']
        self.editProfileLink = moodle_config['general']['8']
        self.debug = moodle_config["debug"]
        self.courses = moodle_config['courses']['list']
        self.defaultDelay = moodle_config['courses']['default_slide_delay']
        self.pickStudent()

    def pickStudent(self):
        #fp = open(self.usersListFile) 
        #line = random.choice(fp.readlines())
        #fp.close()
        #student = line.split(",")
        student = objLoader.getStudent()
        self.group = student[3].strip()
        self.username = student[0]
        self.profilePicture = int(student[4].strip())
        self.userId = int(student[5].strip())
        self.password = self.defaultPassword
        self.userdirectory = "screenshot/" + self.username
        self.bonus = moodle_config["students"]["groups"][self.group]["bonus"]
        self.retry = moodle_config["students"]["groups"][self.group]["retry"]
        self.profpicThreeShold = moodle_config["students"]["profpic_threeshold"][self.group]
        self.triedCourses = []
        self.isUsingResource = False
        self.browsedResources = []
        try:
            os.makedirs(self.userdirectory)
        except OSError as e:
            pass

    def test_login(self):
        try:
            driver = self.driver
            driver.get(self.loginUrl)
            self.assertIn(self.moodleHomeTitle, driver.title)
            self.takePicture('home_notLogged.png')
            elem = driver.find_element_by_link_text(self.moodleLoginLink)
            elem.click()
            self.assertIn(self.moodleLoginTitle, driver.title)
            username = driver.find_element_by_name('username')
            username.send_keys(self.username)
            password = driver.find_element_by_name('password')
            password.send_keys(self.password)
            self.takePicture('login_form.png')
            loginbtn = driver.find_element_by_id('loginbtn')
            loginbtn.click()
            myElem = WebDriverWait(driver, self.defaultDelay).until(EC.presence_of_element_located((By.LINK_TEXT, "Dashboard")))
            if self.profilePicture == 0:
                self.uploadProfilePicture()
            else: 
                self.courseList()
        except Exception, e:
            self.debug = True
            self.takePicture("error_occurred.png")
            self.debug = False
            raise e
    
    def uploadProfilePicture(self):
        print "trying to upload profile picture for user " + self.username + "\n"
        dice = self.rollDice()
        if dice < self.profpicThreeShold: # set proper threeshold
            print "dice said no to profile picture\n"
            self.courseList()
            return

        if os.path.isfile(self.userdirectory+"/" + self.username + ".jpeg"):
            print "userpicture " + self.username + ".jpeg already exists in " + self.userdirectory +"/n"
            self.courseList()
            return
        else:
            print "tryin to upload picture " + self.userdirectory+"/" + self.username + ".jpeg/n"

        driver = self.driver
        picUploadUrl = self.baseUrl + "user/profile.php?id=" + str(self.userId)
        print picUploadUrl
        try:
            driver.get(picUploadUrl)
            myElem = WebDriverWait(driver, self.defaultDelay).until(EC.presence_of_element_located((By.LINK_TEXT, self.editProfileLink)))
            elem = driver.find_element_by_link_text(self.editProfileLink)
            #xpath = "//img[@alt='Add file']"
            #myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, xpath)))
            #elem = driver.find_element_by_xpath(xpath)
            #elem.click()
            #myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.LINK_TEXT, "Upload a file")))
            #elem = driver.find_element_by_link_text("Upload a file")
            #elem.click()
            #myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.NAME, "repo_upload_file")))
            #apparentemente il valore del campo di sotto dovrebbe essere c:\fakeroot\002.jpeg vedi fuck.side
            #elem = driver.find_element_by_name("repo_upload_file").send_keys(os.getcwd()+"/userpics/002.jpeg") 
            #elem = driver.find_element_by_tag_name("button") # <---broken
            #ActionChains(driver).move_to_element(elem).click().perform() # <---broken
            #Keys.ENTER # <-- does 
            #//*["contains(text(), 'Upload this file')]  #no error but does not click //div[2]/div/div[2]/div[2]/div/div/div/button
            #buttonUpload = driver.find_element_by_xpath("//div[2]/div/div[2]/div[2]/div/div/div/button")
            #driver.implicitly_wait(2)
            #ActionChains(driver).move_to_element(buttonUpload).click(buttonUpload)
            #driver.implicitly_wait(200)
            #cerca il bottone id=id_submit
            dice = self.rollDice(1, 22)
            args = self.username + " " + str(dice)
            #wd = os.getcwd()
            #os.chdir('./scripts/')
            subprocess.call(["/usr/bin/php ./scripts/moodle_upload.php " + args] , shell=True)
            #os.chdir(wd)
            driver.implicitly_wait(2)
            driver.get(picUploadUrl)
            driver.implicitly_wait(2)
            #drv.find_element_by_id("yui_3_17_2_1_1546449852648_1527").send_keys(os.getcwd()+"/image.png")
            #find button and submit
        except Exception, e:
            print "call to uploadProfilePicture exception: \n"
            print e
        finally:
            print "redirecting " + self.username +" to course list\n"
            driver.get(self.baseUrl)
            self.courseList()

        return True
        
    
    def courseList(self):
        driver = self.driver
        siteHomebtn = driver.find_element_by_link_text(self.SiteHome)
        siteHomebtn.click()
        self.assertIn(self.moodleCoursesTitle, driver.page_source)
        self.takePicture('courselist_logged.png')
        self.tryParticipate(1)
        #assert "No results found." not in driver.page_source
    
    def tryParticipate(self , att):
        self.hasEnteredCourse = False
        attempt = att
        maxAttempt = self.retry + 1
        print "attempt " + str(attempt) + " of " + str(maxAttempt) + "\n"
        driver = self.driver
        #dice = self.rollDice() + self.bonus
        # for course in self.courseList self.currentCourse = course
        for course in self.courses:
            dice = self.rollDice() + self.bonus
            if self.hasEnteredCourse == True:
                print self.username + " is already attending a course and cannot access course " + course
                return False
            currentCourse = moodle_config[course]
            if currentCourse in self.triedCourses:
                continue
            self.currentThreeshold = currentCourse['threeshold'][self.group]
            print "threeshold is: " + str(self.currentThreeshold)
            print "dice is :" + str(dice) + " for " + self.username + " in attempt " + str(attempt) + " on max attempts " + str(maxAttempt)
            if dice > self.currentThreeshold and attempt <= maxAttempt:
                self.hasEnteredCourse = True
                self.enterCourse(currentCourse)
            else :
                print self.username + " of group " + self.group + " missed entrance for course " + course + " and has " + str(maxAttempt - attempt) + " retries\n"
                if attempt < maxAttempt:
                    if self.hasEnteredCourse == False:
                        self.tryParticipate(attempt + 1)


    def enterCourse(self, course):
        self.triedCourses.append(course['title'])
        func = course['browsemethod']
        print func
        print self.username + " of group " + self.group  + " is entering course " + course["title"] + "\n"
        try:
            getattr(self, func)(course)
            print self.username + " of group " + self.group  + " exited course " + course["title"] + "\n"
            self.hasEnteredCourse = False
            self.isUsingResource = False
        except Exception, e:
            print "method MoodleLogin->" + func + " is not implemented...or..\n"
            print " some other error occurred....exiting..."
            #self.takePicture("error_occurred.png")
            raise e
        
        
    '''
    manually crawl every resource in the course that is mapped in xxxconfig.json
    '''   
    def navigateByLinks(self, course):
            driver = self.driver
            driver.get(self.baseUrl + course['url'])
            self.takePicture("entered_" + course['title'] + ".png")     
            resources = course['paths']        
            for resource in resources:
                if resource not in self.browsedResources and self.isUsingResource == False:
                    currentResource = course['paths'][resource]
                    self.isUsingResource = True
                    self.browsedResources.append(currentResource['res_title'].lower())
                    self.clickResource(course, currentResource)
        
    '''
    Should implement navigation by an xml save from webide
    '''
    def navigateBySchema(self, course):
        print "Navigation by schema is not implemented yet, falling back to navigateByLinks"
        self.navigateByLinks(course)

    '''
    Calls moodle rest api
    '''
    def navigateByMoodleapi(self, course):
        course_contents = {}
        # Apparently rolling enrollment courses are not a good idea
        # https://docs.moodle.org/36/en/Analytics#Evaluate - see paragraph limitations
        # just kept for a few days to check how fast the script works, which is not fast enough
        # Have to revert to coohort enrolment soon usign script mv_bulkcoorthenrol.php
        # 564 users were enroled in course 3 as 17/02/2019 (gonna check one more 1 hour session)
        if 'force_enrol' in course:
            print "trying to enrol student " + self.username + " in course " + course['title']
            enrol = course['force_enrol']
            args = self.buildArgs(enrol)
            #print subprocess.check_output("/usr/bin/php ./scripts/moodle_restclient.php " + args, shell=True)
            #print self.callRestClient(args) <--commented as not needed anymore
            print "skipping enrolment, everybody is already in"

        driver = self.driver
        driver.get(self.baseUrl + course['url'])
        self.takePicture("entered_" + course['title'] + ".png") 
        course_contents_config_file = 'scripts/course_contents_' + str(course['id'])+'.json'
        if os.path.isfile(course_contents_config_file):
            print "course contents found at " + course_contents_config_file
            course_contents = config.load(course_contents_config_file)
            #print course_contents
        else:
            res = dict()
            res['call'] = 'core_course_get_contents'
            res['params'] = " " + str(course['id']) + " "
            args = self.buildArgs(res)
            self.callRestClient(args)
            time.sleep(1)
            self.navigateByMoodleapi(course)


        for resource in course_contents:
            for module in resource['modules']:
                #print str(module['id']) + module['name'] + " " + module['modname'] +" " + module['url'] + "\n"
                if module['modname'] == 'quiz':
                    module['id'] = module['instance']
                    print "PRE-CHECK: " + module['name'] + " is a quiz switching to instance(id)"

                if str(module['id']) in course['paths'] and module['uservisible'] == True:
                    print "found mapped resource " +str(module['id']) + '\n'
                    path = course['paths'][str(module['id'])]
                    path['res_title'] = module['name']
                    path['res_type'] = module['modname']
                    path['url'] = module['url']
                    path['res_link'] = '//a[@href="' + module['url'] + '"]'

        #print course['paths']
        resources = course['paths']
        for resource in resources:
            if resource not in self.browsedResources and self.isUsingResource == False:
                currentResource = course['paths'][resource]
                if "configure" in currentResource:
                    print "resource id " + str(resource) + " is an oublog"
                    currentResource = getattr(self, currentResource['configure'])(course, currentResource)
                    
                self.isUsingResource = True
                self.browsedResources.append(currentResource['res_title'].lower())
                self.clickResource(course, currentResource)

    def buildArgs(self, resource):   
        try:
            restcall = resource['call']
            args = " "
            #add args
            if "helper" in resource:
                args = getattr(self, resource['helper'])(resource)
            else:
                args = resource['params']

            return restcall + args
        except Exception, e:
            raise e

    def helperEnrol(self, resource):
        print "helperEnrol Called"
        params = resource['params']   
        args = params.replace(':userid:', str(self.userId))
        return args

    '''args = ws_call + params'''
    def callRestClient(self, args):
        return subprocess.check_output("/usr/bin/php ./scripts/moodle_restclient.php " + args, shell=True)

    def clickResource(self, course, resource):
        func = resource['res_type']   
        try:
            func = resource['res_type']
            result = getattr(self, func)(course, resource)
            print result
            self.isUsingResource = False
            self.driver.get(self.baseUrl + course['url'])
            #self.navigateByLinks(course)
        except Exception, e:
            print "method MoodleLogin->" + func + " is not implemented or threw an exception...exiting..\n"
            #print e
            raise e
    
    # unluckily sloppy course_contents ws call seems to have 
    # problem with activity oublog as it sees it as hidden even when it's not
    # so we have to manually build the resource
    def oublogConfigure(self, course, res):
        # /mod/oublog/view.php?id=22
        print "configuring oublog"
        res['res_type'] = 'oublog'
        res['url'] = self.baseUrl + "mod/oublog/view.php?id=" + str(res['id'])
        res['res_link'] = '//a[@href="' + res['url'] + '"]'
        res['res_link_comment'] = "Add your comment"
        return res

    def oublog(self, course, res):
        driver = self.driver
        if self.rollDice(1,6) + self.bonus <= course['threeshold'][self.group]:
            return "dice said no to visiting blog for user " + self.username

        print self.username + " is visiting oublog " + res['res_title']
        elem = getattr(driver, 'find_element_by_xpath')(res['res_link'])
        elem.click() 
        time.sleep(3)
        try:
            elem = driver.find_element(By.PARTIAL_LINK_TEXT, "comment")
            elem.click()
        except Exception, e:
            elem = getattr(driver, 'find_element_by_link_text')(res['res_link_comment'])
            elem.click()
        time.sleep(1)
        driver.get(self.baseUrl + res['edit_link'])
        time.sleep(1)
        body = self.randomText(100)
        text = driver.find_element_by_id('id_messagecommenteditable') 
        driver.execute_script("arguments[0].scrollIntoView();", text)
        text.send_keys(body)
        btnSubmit = driver.find_element_by_name('submitbutton')
        driver.execute_script("arguments[0].scrollIntoView();", btnSubmit)
        btnSubmit.click()
        time.sleep(3)
        return self.username + " dropped a comment on oublog " + res['res_title']
    # ends stupid shit

    def forum(self, course, res):
        driver = self.driver
        print self.username + " entered forum " + res['res_title'] + " in course " + course['title'] 
        elem = getattr(driver, 'find_element_by_xpath')(res['res_link'])
        elem.click() 
        time.sleep(3)
        startedNewThread = False
        leaveComment = False
        # try to start a new thread
        if "button_enter" in res:
            elem = driver.find_element_by_xpath(res['button_enter'])
            elem.click()
            # rollDice here
            if self.rollDice(1,6) + self.bonus > course['threeshold'][self.group]:
                startedNewThread = self.writeSomeText(res)
                leaveComment = True
            else:
                print "dice said no to starting new thread for user " + self.username
                leaveComment = True
                
            if startedNewThread == True:
                print self.username + " started a new thread"
            # if dice says no put startedNewThread to True coz we want to try reply some threads
        
        if leaveComment == True and self.rollDice(1,6) + self.bonus > course['threeshold'][self.group]: # we have to go back
            print " re-entered forum " + res['res_title']
            elem = driver.get(res['url'])
            time.sleep(2)  
            # now try to reply some thread
            # rollDice here
            threads = driver.find_elements(By.CSS_SELECTOR,'td.replies > a')
            
            if len(threads) > 0:
                dice = self.rollDice(0, len(threads)-1)
                print dice
                elem = threads[dice]
                elem.click()
                time.sleep(2)
                elem = driver.find_element(By.LINK_TEXT, 'Reply')
                elem.click()
                time.sleep(2)
                if self.writeSomeText(res) == True:
                    return self.username + " dropped a comment on forum " + res['res_title']
            else:
                print "dice said no to comment someone else forum post for " + self.username


        
        return self.username + " exits forum " + res['res_title'] + " in course " + course['title'] 
    
    '''TODO: set parameters for everythin, oppure usare questo come wrapper'''
    def writeSomeText(self, res):
        driver = self.driver
        title = self.randomText()
        body = self.randomText(100)    
        time.sleep(3)
        subject = driver.find_element_by_name('subject')
        subject.send_keys(title)
        text = driver.find_element_by_id('id_messageeditable')
        driver.execute_script("arguments[0].scrollIntoView();", text)
        text.send_keys(body)
        btnSubmit = driver.find_element_by_name('submitbutton')
        driver.execute_script("arguments[0].scrollIntoView();", btnSubmit)
        btnSubmit.click() # <<<UNCOMMENT --temporarily commented not to clutter the forum
        time.sleep(3)
        # we are now to the current thread page and have to go back to forum threads list
        return True
    
    ''' really a hard task, we go by trial, step by step '''
    def quiz(self, course, res):
        print self.username + " entered quiz " + res['res_title'] + " in course " + course['title'] 
        driver = self.driver
        elem = getattr(driver, 'find_element_by_xpath')(res['res_link'])
        elem.click()
        time.sleep(3)

        buttonEnter = None
        try:
            buttonEnter = driver.find_element(By.XPATH, "//input[@value='Attempt quiz now']")
            ActionChains(driver).move_to_element(buttonEnter).click().perform()
        except:
            buttonEnter = None

        if buttonEnter == None:
            try:
                buttonEnter = driver.find_element(By.XPATH, "//input[@value='Continue the last attempt']")
                ActionChains(driver).move_to_element(buttonEnter).click().perform()
            except:
                buttonEnter = None
        if buttonEnter == None:
            buttonEnter = driver.find_element(By.XPATH, "//input[@value='Re-attempt quiz']")
            ActionChains(driver).move_to_element(buttonEnter).click().perform()

        answers = None
        time.sleep(3)
        isBusy = True
        while isBusy:
            try:
                answers = driver.find_elements(By.CSS_SELECTOR,'div.answer')
                isBusy = False
            except StaleElementReferenceException:
                isBusy = True
        
        print len(answers)
        i =0
        for answer in answers:
            div = answer
            div2 = div.find_element(By.CLASS_NAME, "r0")
            ActionChains(driver).move_to_element(div2).perform()
            i+=1
            print self.username + " is answering question " + str(i)
            regex = 'name="q(.+?):' + str(i) + '_answer"'
            qNum = re.search(regex, div2.get_attribute("innerHTML"))
            radio = driver.find_element(By.NAME, "q"+ str(qNum.group(1)) + ":" + str(i) +"_answer")
            if self.rollDice(1, 6) + self.retry > 3:
                radio.click()
            else:
                print "dice said no to answering question "+str(i)
                
            time.sleep(1)
        
        buttonFinish = driver.find_element(By.XPATH, "//input[@value='Finish attempt ...']")
        ActionChains(driver).move_to_element(buttonFinish).click().perform()
        time.sleep(3)
        print self.username + " is trying to submit quiz " + res['res_title'] + " in course " + course['title'] 
        buttonConfirm = driver.find_element(By.XPATH, "//input[@value='Submit all and finish']")
        ActionChains(driver).move_to_element(buttonConfirm).click().perform()
        time.sleep(3)
        xpr = "//*[@class='confirmation-buttons form-inline justify-content-around']/input[@value='Submit all and finish']"
        buttonConfirm2 = driver.find_element(By.XPATH, xpr) 
        buttonConfirm2.click()
        time.sleep(3)      
        
        
        return self.username + " submitted quiz " + res['res_title'] + " in course " + course['title'] 
    
    def resource(self, course, res):
        return self.reading(course, res)

    def reading(self,course, res):
        driver = self.driver
        #func = "find_element_" + res['res_link_type'] #<< raise error, why?
        #elem = getattr(driver, func)(res['res_link']) #<< raise error, why?
        elem = getattr(driver, 'find_element_by_xpath')(res['res_link'])
        elem.click()    
        self.takePicture("entered_" + course['title'] + "_" + res['res_title'] + ".png")
        return self.username + " has entered resource " + res['res_title']+"\n"

    def scorm(self, course, res):
        driver = self.driver
        #func = "find_element_" + res['res_link_type'] #<< raise error, why?
        #elem = getattr(driver, func)(res['res_link']) #<< raise error, why?
        print self.username + " has entered scorm " + res['res_title']+"\n"
        elem = getattr(driver, 'find_element_by_xpath')(res['res_link'])
        elem.click()    
        self.takePicture("entered_" + course['title'] + "_" + res['res_title'] + ".png")
        buttonEnter = moodle_config['courses']['scorm']['button_enter']
        buttonAdvance =res['button_advance']
        elem = driver.find_element_by_xpath(buttonEnter)
        elem.click()
        self.takePicture("started_" + course['title'] + "_" + res['res_title'] + ".png")
        #seleziona o meno il frame giusto a seconda di dove sono collocati i pulsanti dello scorm
        if 'ignore_iframe' in res:
            pass
        else:
            driver.switch_to_frame("scorm_object")
        #loop sulle slides
        slides = res['slides'] + 1
        delay = self.defaultDelay # not really used unless i clear existing configs
        #print "SONO ARRIVATO QUI<<<<"
        if self.debug:
            print " delay is: " + str(delay)
        #myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.next > .component_base')))
        elem = driver.find_element_by_xpath(buttonAdvance)
        driver.execute_script("arguments[0].scrollIntoView();", elem)
        for i in range(1, slides):
            try:
                driver.implicitly_wait(1)
                elem.click()
                print self.username + " is watching slide " + str(i) + "\n"
                self.takePicture(course['title'] + "_" + res['res_title'] + "_slide" + str(i) +".png")
            except TimeoutException, e:
                print "non trovato pulsante " + buttonAdvance + " per " + course['title'] + "_" + res['res_title'] + "\n"
                raise e


        self.takePicture("completed_" + course['title'] + "_" + res['res_title'] + ".png")

        return self.username + " has exited scorm " + res['res_title']+"\n"
    
    def randomText(self, size=20, chars=string.ascii_uppercase + string.ascii_lowercase):
        return ''.join(random.choice(chars) for _ in range(size))

    def rollDice(self, start=1, end=6):
        return random.randint(start,end)
    
    def takePicture(self, picture_name):
        if self.debug:
            self.driver.save_screenshot(self.userdirectory +"/" + picture_name)
        return self.userdirectory +"/" + picture_name

    def tearDown(self):
        #https://sqa.stackexchange.com/questions/1941/how-do-i-close-the-browser-window-at-the-end-of-a-selenium-test
        #self.driver.close()
        try:
            print "session exit for " + self.username
        except Exception:
            print "fatal error"

        self.driver.quit()

if __name__ == "__main__":
    unittest.main()