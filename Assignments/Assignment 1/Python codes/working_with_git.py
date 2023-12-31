# -*- coding: utf-8 -*-
"""working with git.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/11GZgVSDVj0G9psbNMMvuUExPWuW_Zg-A
"""

!pip install gitpython

from git import Repo

help(Repo.clone_from)

help(Repo.__init__)

coursefolder = '/Users/Jay/tmpdir/'

import os
os.path.abspath(coursefolder)

repodir = os.path.join(os.path.abspath(coursefolder), 'mth271content')
repodir # full path name of the subfolder

os.path.isdir(repodir)

if os.path.isdir(repodir): # if repo exists, pull newest data
  repo = Repo(repodir)
  repo.remotes.origin.pull()
else: # otherwise, clone from remote
  repo = Repo.clone_from('https://github.com/jayggg/mth271content', repodir)

repo.working_dir