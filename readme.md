# TeamTree  
TeamTree is a simple application for displaying and navigating a hierarchy of names such as an employee list.  It receives input from teamtree.csv and teamupdates.csv.  If either file is missing, the app won't run.  
  
# Installation Instructions for Windows  
  
## Install Python  
Downloand and isntall Python from https://www.python.org/downloads/  
Select "Custom Install"  
Uncheck the boxes for "Documentation", "Tcl/tk", "Py launcher"  
Check the boxes for "Install for all users", "Precompile standard library"  
Change the install location to `c:\python`  

## Add Python path to Windows  
Click Start and type "Edit the system environment variables" <enter>  
  In System Properties, click "Environment Variables" near the bottom.  
    In System Variables, scroll unti you find "Path".  Highlight it then click "Edit"  
      In Edit Environment Variable, click "New".  Add "c:\python" as the new path variable  
      In Edit Environment Variable, click "New".  Add "c:\python\scripts" as the new path variable  
      Click "OK", "OK"  
Confirm that Python is installed correctly by typing `python --version` at the command prompt  
Check if PIP is installed by typing `pip help` at the command prompt  
  If PIP is installed, skip the next step
    
## Install PIP to Windows
Download and save this file to `c:\python`: https://bootstrap.pypa.io/get-pip.py  
Open the Windows Command prompt as Administrator  
  `cd c:\python`  
  `python get-pip.py`  
Confirm that PIP is installed by typing `pip help` at the command prompt  
  
## Install Pandas, Django
Open the windows Command prompt as Administrator  
  `pip install pandas`  
  `pip install django`  
  
## Install TeamTree  
From Chrome, go to: https://github.com/daveisnt/teamtree/  
  Click "Code"  
    Click "Download ZIP"  
    Right-click on the ZIP file  
    Click "Extract All"  
    Type `c:\python_web` for the destination folder  
    Click "Extract"  
  
If you have team lists already to go, save them to... 
  `c:\python_web\teamtree-master\teamtree.csv`  
  `c:\python_web\teamtree-master\teamupdates.csv`  
  
From Command prompt, type:
  `cd c:\python_web\teamtree-master`  
  `python manage.py runserver`  
    
Open Chrome and go to https://localhost:8000/tree/  
