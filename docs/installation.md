# Installation
 LearnProgrammingBot requires scikit-learn, praw and sqlalchemy. Due to this, the installation instructions are slightly different depending on which platform you are using. It should work with both Python 2 and Python 3 (unit tests are coming soon).
 
 To install, first download the source from either [the master ZIP](https://github.com/Aurora0001/LearnProgrammingBot/archive/master.zip) or the [releases](https://github.com/Aurora0001/LearnProgrammingBot/releases) tab, and extract the zip file into any directory. Alternatively, you can clone the source using git by running:
 
     git clone https://github.com/Aurora0001/LearnProgrammingBot.git
     
 Then, follow the instructions for your platform to install the dependencies:
 
## Windows
 As an administrator, in the command prompt, run:

    pip install -r requirements.txt

If pip is not recognised, you may need to install it using [these instructions](http://stackoverflow.com/questions/4750806/how-do-i-install-pip-on-windows#12476379). If you want to download a pre-compiled version of Python with SciPy, try [Python(x,y)](https://python-xy.github.io/downloads.html).

## Mac

    sudo pip install -r requirements.txt
    
## Debian/Ubuntu/Mint

    sudo apt-get install python-scipy python-pip
    sudo pip install sqlalchemy scikit-learn praw
     
## Other Linux Distributions
 Check if your distribution has a package such as `python-scipy`, which will save time and avoid the need for you to compile NumPy from source (which is slow and quite difficult). If you **can** use a package, just run this afterwards: 
 
    sudo pip install sqlalchemy scikit-learn praw

Make sure that you've installed the package for `pip` too, if you haven't already.

If your distribution does not have a SciPy package, just run this (and prepare for a long wait!): 

    sudo pip install -r requirements.txt
    
