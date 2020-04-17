# Salesforce Incremental Package Builder

A simple python script and gui to build incremental packages. Uses filecmp and lxml to compare two directories and build the package.xml for metadata components that are different between the two. 

GUI in PySimpleGui.

To run the GUI use ```app.py```.

To run the script directly, set the REMOTE and LOCAL inside ```script.py```.  

## Screenshots

![ss1](https://user-images.githubusercontent.com/31303415/79558439-c592d800-80c1-11ea-9a69-9e39b800116a.png)

![ss2](https://user-images.githubusercontent.com/31303415/79558495-de02f280-80c1-11ea-8621-388b3d4e62bf.png)


## Requirements

1. PySimpleGUI - Only for GUI 
2. lxml - For both GUI and script

```pip install -r requirements.txt```
