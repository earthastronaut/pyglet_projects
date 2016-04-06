# Pyglet Projects

[Pyglet](https://bitbucket.org/pyglet/pyglet/wiki/Home) is a fun python interface for creating iteractive games. The purpose of pyglet_projects is to provide pyglet game examples for teaching and fun.


## Getting Started

To get started you'll need python and pyglet. Probably the easiest way to get these requirements is to:

1. [install python](https://wiki.python.org/moin/BeginnersGuide/Download)
1. [install pip](https://pip.pypa.io/en/stable/installing/)
1. (optional) you may want to install [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/) and install these within a virtual environment. Make sure you use python 3
1. download this repo using either `git clone` or the download zip button above
1. install `pyglet`
    1. [how to install pyglet for python3](http://stackoverflow.com/questions/21298834/how-to-get-pyglet-working-for-python-3)
    1. [pyglet home](https://bitbucket.org/pyglet/pyglet/wiki/Home)
    1. [pyglet install docs](http://pyglet.readthedocs.org/en/latest/programming_guide/installation.html)

Now you're ready to dive in. 

_Note: python3 is suggested but not necessarily required. Some of the projects may work with python2._ 


## Pyglet Project Organization

This repo is organizes into directories for each example nested within the `projects` folder.

    |- pyglet_projects/
        |- README.md
        |- spinoff_projects.md
        |- projects/
            |- mind_sweeper_basic/
                |- README.md
                |- run.py
                |- ... 
            |- snake_with_basic/
                |- README.md
                |- run.py
                |- ... 
            |- ... 


You should be able to go to any directory (sub-project) and run `python3 run.py` to start the game. 

I created a single repo for all these projects so it'd be easy for someone to download and try out a bunch of pyglet games. 

Each project could concevable be it's on repo. I encourage you to start your own git repo, copy the project code over as a starting point, and modify to your hearts content. If you do, please add a link to `spinoff_projects.md` and make a pull request. Share the fun!


## Explorative Learning

One goal of `pyglet_projects` is to be a learning tool for beginning developers. The projects have varying levels entry (e.g. some require knowledge of object oriented programming others do not). Because of this some projects have repeated implementations. 

Courses often start teaching programming from the ground up with variables, control statements, and so on. I fully endorse this method. However, I know when I began programming some of the most valuable learning was from exploring existing projects. 

Here are some general steps:

1. start up a project and see how it works (these projects start with `python3 run.py`)
1. get a text editor (like [Sublime Text](https://www.sublimetext.com/)) and open up the source code for the projects.
1. modify the source code and run it again. 
1. go crazy, make modifications, and re-run it 
    1. some good modifications are things like changing colors, object shapes, and control keys/buttons


## Contributing

Open source rocks! If you have an project idea to add to `pyglet_projects`
 create a pull request! Projects must: 

1. run with `python3 run.py`
1. follow [pep8](http://pep8.org/)
 