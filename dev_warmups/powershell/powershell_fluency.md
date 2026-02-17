## Use these for moving around
pwd
ls
cd folder
cd ..

## Creat a file or folder: do not like skip 
New-Item -Name file.txt -ItemType File
New-Item -Name folder -ItemType Directory
Get-ChildItem -Filter file.py 

this is better : use these
mkdir → create directory

ni → PowerShell alias for New-Item
example: 
# mkdir src\delay_risk\validation
# ni src\delay_risk\__init__.py

rmdir .\src -Recurse -Force  : delete everything inside (meaning of -Recurse), -Force ( don ask for confirmation)
also ls sames as dir same as Get-ChildItem for poweshell.

also  tree folder to see tree of relations for subfolders. 