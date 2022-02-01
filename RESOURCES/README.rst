# CF PIPELINE

8< ------------------------------------------------------------------------------------------------------------------------------------------------ >8

## INFORMATION FOR USERS

### Installation

At first, the project will probably just need an installer program for windows users, a homebrew package for mac users, and a gzipped tar archive with 
a Makefile for Linux. Later, I would like to add archives for at least deb and rpm so that it can be deployed to repos for various package mgrs such 
as Apt.

Additionally, it will need to be run through the setuptools process so it can be added to ``PyPi/pip``.

At this point, since there are no finished modules to install or run, there is nothing else to add here, and this document (and indeed, this package) 
will only be useful to contributors. If you are an end user reading this, try back occasionally. When this section changes, you will know that it is 
ready for at least one or two basic uses.

### Getting started

**NOTE: Until the program is at least runnable with at least one useful command, this section is purely for reference.**

CF Pipeline is a cli program for automating all of your routines. The goal is to build a program that wikk eventually be versatile enough that you can 
automate any codeforces "workflow". The term workflow has a special meaning within the context of this application. For the context-dependent 
definition of the term, see the subsection below with the same name.   

Currently, only Linux is supported, but there are plans to support Windows and Mac in future versions.

To run, simply type in the appropriate command into a shell style tty/pty command prompt of your choosing. the full synopsis is included in the 
``Synopsis`` subsection below. The command always starts with ``cfp`` followed by a command. All commands are divided into two groups: low-level task 
commands and higher-level workflow commands. The latter is a convenience which runs a group of the former. More accurately, the former were created to 
support development of the latter in an efficient, reusable, and extensible way.

The last of these is what I believe seperates CF-Pipeline from other Codeforces cli programs. In addition to the provided workflow commands, CF-P 
provides (will provide) a framework for building workflow commands that let you interact with the codeforces api in just about any way that it 
supports. The goal for the final implementation of CF-P is to provide a package that contains 

  - a small task-level command for every task available via the codeforces.com api
  - a set of workflow commands representing the most common workflows
  - a framework for combining tasks to make your own workflows



8< ------------------------------------------------------------------------------------------------------------------------------------------------ >8

## INFORMATION FOR DEVELOPERS

*NOTE: Be sure to read the user info above before moving to this section, as it will give you a good idea of the general goals for the project.*

### CONTRIBUTING

Not much to 

### TODO

At this point, focus should be on building tasks. The next section, titled ``TASKLIST``, is a list of all tasks that have been implemented so far. If 
you want to 

### Git Conventions

#### Branching Strategy

#### Remotes

If you are reading this, you've found the only remote, fr now at least. Later the binaries will have multiple deployment endpoints.

Just for posterity:

https://github.com/lifeModder19135/cf-pipeline

#### Commits

Commits will follow these conventions. The message will have a title of the format of ``_datestring_--_scope_--_title_`` on the first line. The second 
will be blank. 

All remaining lines will be either change-items or change-subitems. Both types will follow the format of a bulleted list item preceded by whitespaces. 

A change-item describes a change that is included in the commit. These will each follow exactly 2 blank spaces at the beginning of a new line. 

Change-subitem(s) go on the line(s) immediately below the change-item to which they refer. They are meant for describing the aspects of, or else the 
steps involved in the implementation of, a change-item in greater detail. The format for change-subitems is the same as it is for change-items, but the
former also includes an

For examples, run ``git log`` from inside the main project directory to see the previous commits. 

8< ------------------------------------------------------------------------------------------------------------------------------------------------ >8

## ABOUT CF-P

### General Info

### Workflows, Tasks, and more junk

A workflow, in this context, is any set(workflow) of interactions(tasks) with the site(context) that you would commonly carry out together to 
accomplish some goal(s) (tasks). The most commonly used example of a workflow in CF Pipeline is probably competing in a Codeforces.com competition. In 
this example, the end goal, a.k.a the workflow is to take part in a codeforces competition, with the id of the competition being specified by the user 
and passed to the cfp command as an argument. This workflow will be composed of tasks. One such task would be to retrieve the contest problems and 
display them to the user in some way. The method of display will likely be configurable by the user via config file or an option argument added to 
the command.

So in this example, the following (made-up) workflow command would be used...

    example@example/~$_    *cfp compete [ --options ] <CONTEST-ID>*

Some of the tasks involved in this workflow, along with the associated (again, imaginary at this point) commands would be:

  - If user not logged in, do so  
    example@example/~$_    *cfp login -u <USERNAME> -p stdin*      # or maybe a hashed cmd-line version, we'll see...
    
  - get problems
    example@example/~$_    *cfp grab-problem 1625_A; cfp grab-problem 1625_B; ... cfp grab-problem 1625_F *
    
  - more stuff...
      
...and you get the idea. The point is that the bigger commands, with which users will likely be the most familiar, will be made up of smaller 
do-one-job-well commands, and that there will be a framework for users to combine these in any way they need to make their own bigger commands.

### A note about the (future!!) workflow for competing in contests 

The command(s) above mentioned using the contest id as a parameter. This value will likely be used many times over in the specification of cfp 
commands.  The contest id is the (often 3-or-4-digit) number that you see in the URL when you are on the web pages for a contest or it's problems. At 
the time of writing, most of the recent contest IDs have been in the 16xx range. Obviously, since there is no late registration (aside from the 
extremely small forgiveness window), to compete in a contest, the user must be logged in and pre-registered. That said, eventually, there may be a 
workflow to register early and then recieve some sort of notification/triggered tasks when the contest is starting.


### AUTHORS

______NAME_____| ______CF_USERNAME________| _________EMAIL_____________|

 - - ntolb - - - - - lifeModder19135 - - - - - ntolbertu85@gmail.com
