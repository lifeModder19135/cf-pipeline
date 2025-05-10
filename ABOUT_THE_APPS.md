# About the Apps

## Introduction

Following is a list, in alphabetical order, of descriptions for all of the apps included with this package. These are all command line tools for competitive programmers. To use any of these apps, just type it's name on the command line, 
followed by any needed options or arguments. For a list of options and/or arguments
associated with an app, type 

'{app name} --help' 

on the command line. All of the apps have this help option which outputs a short description for the app, followed by a list of available options and arguments.

## Apps List

***NOTE:*** In the synopsis section, [] surrounds required args or options, and <> 
surrounds the optional ones. Also, | means *or*.

### cf-fetchproblem

  **Synopsis**
    cf-fetchproblem <--rating [INTEGER]> | <--min-rating [INTEGER]> <--max-rating [INTEGER]>

  **Description**
    Fetch a random Codeforces problem by exact rating or within a rating range.

### cf-getproblem

  ***Synopsis***
    cf-getproblem [CONTEST-ID] [LETTER-INDEX] | <--help>

  ***Description***
    This is a simple command-line program created as an example of how to use 
    this framework. You identify the problem you want by its contest id and its
    letter index. It returns the available info on that problem. For example,
    running the command 'cf-getproblem 2093 A' will return the details for
    problem A from contest 2093, which happens to be named "Ideal Generator".

### cf-makefilefmt1

  ***Synopsis:***
    cf-makefilefmt1 <-d | --dest [STRING]> [-t | --type [STRING]] [-c | --cases [INTEGER]] [-l | --lines [INTEGER]] [-v | --values [INTEGER]] <--help>

  ***Description:***
    This command is used for building templates for cfp format 1 files (.cfpin,
    .cfpout, and .cfpexp files, the kind used with cf-testproblem). To use, just
    execute the command giving values for all of the  options. The options
    describe how you want the file laid out. 

### cf-pipeline

  ***Synopsis:***
    cf-pipeline <-v | -V | --version> | <-c | -C | --contribute> | <-u | -U | --usage> | <--help>

  ***Description:***
    This command is meant for new users to cf-pipeline. using the various
    options, you can get useful info on the version, usage info, and even info
    on contributing to the project.

### cf-testproblem 

  ***Synopsis:***
    cf-testproblem [SOLUTIONFILE] [INPUTFILE] [OUTPUTFILE] | <--help>

  ***Description:***
    This will test a codeforces solution against input provided in the format of
    a cfpin file. For more details about cfpin files, see cfp_context.py.
