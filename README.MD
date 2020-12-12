## Moodle Quick DataSet

### Prequel
Back in 2018 I wanted to give a try to the [Students at risk of dropping out](https://docs.moodle.org/310/en/Students_at_risk_of_dropping_out)  model which is part of [Moodle's Learning Analytics](https://docs.moodle.org/310/en/Analytics).
As per their definition:

>This model predicts students who are at risk of non-completion (dropping out) of a Moodle course, based on low student engagement.

>In this model, the definition of "dropping out" is "no student activity in the last quarter of the course." 
>This prediction model uses the Community of Inquiry model of student engagement, consisting of three parts:
>
> - Cognitive presence
> - Social presence
> - Teacher presence

The expected output is something like this

![Insights](https://github.com/mvit777/moodle_quick_dataset/raw/master/docs/pics/list.png)

and this

![Insights](https://github.com/mvit777/moodle_quick_dataset/raw/master/docs/pics/detail.png)


I also had a plan (now totally de-railed mainly due to lack of time) to code a plugin which would cross-check the model's output against the output of one or more [gamification plugin](https://docs.moodle.org/310/en/Using_restrict_access#Gamification), ideally through the use of [Jupyter Notebooks](https://jupyter.org/).

The first thing I needed was a lot of data. At the time I had access to a moodle platform but the courses there where already started or their structure did not meet the model's criteria (ex. no due date etc etc).
So armed with a list of users, a couple of courses and the [selenium webdriver](https://www.selenium.dev/about/), I decided to simulate an entire semester in a matter of a week.
The idea was to feed a script with the list of users and let selenium, a bit of system date/time tampering and a guided random do the rest.

This [collection of scripts](https://github.com/mvit777/moodle_quick_dataset/tree/master/py3) is what I came out with and here a screencast of what they do

[![screencast](https://github.com/mvit777/moodle_quick_dataset/raw/master/video/screencast.png)](https://www.youtube.com/watch?v=sj6mydLKPbk)

## ...some more details...
The main folder should reside in moodle's root directory.
I previously divided students in three coohorts inside moodle (A, B, C) and give all the same password

All the scripts are in the [py3 folder](https://github.com/mvit777/moodle_quick_dataset/tree/master/py3)

The [screenshot folder](https://github.com/mvit777/moodle_quick_dataset/tree/master/py3/screenshot) should have write permission for the user launching the [main.py](https://github.com/mvit777/moodle_quick_dataset/tree/master/py3/main.py) script.

To start `python3 main.py` from inside the py3 folder. You can specify the list-of-users file and the mapping-of-course(s) file as arguments.

Site level configurations are made in the [general.json](https://github.com/mvit777/moodle_quick_dataset/tree/master/py3/configs/general.json) file.
Here you can assign, for instance, the random for participating at the course on site level

The mapping of the resources of the course is done in the [fullcourse.json](https://github.com/mvit777/moodle_quick_dataset/tree/master/py3/configs/fullcourse.json) in case you call main.py without arguments or a single course.
The mapping of the resources of the course is a bit of a pain in the neck a script in the scripts folder may assist (see below). 
To make things a little bit easier I also made some assumptions like the theme is the default one, the language is English and quizzes' first answer is the correct one (a funny moodle's configuration which only I usee I see is this).

The [scripts folder](https://github.com/mvit777/moodle_quick_dataset/tree/master/py3/scripts/) contains some php scripts which are called by the main.py file and perform api calls to moodle. In some cases that was much easier than scripting with webdriver. Here you have to configure the url, user and token for moodle's webservice.

## End of the story
As said before this stuff is a bit messy but in case someone wants to pick up where I left here you go...happy coding



