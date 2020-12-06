# Table of Contents  
  
[How to Get Setup](#setup)  
[How to Fire Off Individual Trades](#firetrades)  
[How to Receive Data](#receivedata)  
  
## How to Get Setup  
  
To get setup with the IBKR API, follow the steps listed below.  

1. Visit the url: https://interactivebrokers.github.io/  
2. Click on "I Agree". A new frame slides into view.  
3. The first row lists stable API, for Windows on the Left, and for Linux/Mac on the right.  
4. Select your OS and download the API.  
5. For Linux/Mac open a command terminal and navigate to the download location where you've downloaded the API.  
6. Type in the command `sudo unzip twsapi_macunix.n.m.zip -d $HOME/`. The n.m.zip part will actually have your version number.  
7. After unzip'ing the files, navigatge to the API location for python. Use the command: ` cd ~/IBJts/source/pythonclient`.  
8. Then type in the following commands.  
`python setup.py build`  
`python setup.py install`  
> Note: for Ubuntu and derivates you'll need to use `python3` instead of `python`. For Ubuntu `python` refers to python 2.x version, and `python3` refers to python 3.x version.  
9. Launch your TWS client and enable API connectivity by following the instructions at: https://interactivebrokers.github.io/tws-api/initial_setup.html  
10. Open a new file using your favorite IDE and type in the following code:  
```python  
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import *
from threading import Timer

class IBapi(EWrapper, EClient):
  def __init__(self):
    EClient.__init__(self, self)
    
app = IBapi()
app.connect('127.0.0.1', 7497, 123)
app.run()

time.sleep(2)
app.disconnect
```

Download Python here:
https://www.python.org/downloads/
