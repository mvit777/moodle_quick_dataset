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

This [collection of scripts](https://github.com/mvit777/moodle_quick_dataset) is what I came out with and here a screencast of what they do
