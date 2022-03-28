# TeamTree
TeamTree is a simple application for displaying and navigating a hierarchy of names such as an employee list.  It receives input from teamtree.csv and teamupdates.csv.  If either file is missing, the app won't run.

# Installation Instructions for Windows

## Install Python
Downloand and isntall Python from https://www.python.org/downloads/ 

## Install Pandas, Django, Git
Open the windows Command prompt as Administrator.
  pip install pandas
  pip install django
  pip install git
  
## Install TeamTree
From Command prompt
  mkdir c:\python_web
  cd c:\python_web
  git clone https://github.com/daveisnt/teamtree.git
  cd teamtree
  python manage.py runserver
  
Open Chrome and go to https://localhost:8000/tree/
