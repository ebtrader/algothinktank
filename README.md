# Table of Contents  
  
[How to Get Setup](#setup)  
[How to Fire Off Individual Trades](#firetrades)  
[How to Receive Data](#receivedata)  
  
## How to Get Setup  
  
To get setup with the IBKR API, follow the steps listed below.  

1. Visit the url: https://interactivebrokers.github.io/  
2. Click on "I Agree". A new frame slides into view.  
3. The first row lists stables API, for Windows on the Left, and for Linux/Mac on the right.  
4. Select your OS and download the API.  
5. For Linux/Mac open a command terminal and navigate to the download location where you've downloaded the API.  
6. Type in the command `sudo unzip twsapi_macunix.n.m.zip -d $HOME/`. The n.m.zip part will actually have your version number.  
7. After unzip'ing the files, navigatge to the API location, type in: ` cd ~/IBJts`.  
8. Navigate into source/pythonclient folder and type in the following commands.
`python setup.py build`  
`python setup.py install`  
