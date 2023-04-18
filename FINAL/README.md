# App 0 Manager - Client App {N} System using ZeroMQ library

## Description
Two separate applications are developed for this system, one which is the App 0 Manager and the other a Client App program

This is an example of how ZeroMQ messaging library can be used to exchange files between two connected system(s). Three important specifications to be aware of are:

* "App 0 Manager”– should be able to send and receive messages with any client App (“Client App 1”, “Client App2”, ...., “Client App {N}” )
* “Client App 1” – can send and receive messages from “App 0 Manager”
* “Client App 2” – can send and receive messages from “App 0 Manager”
* “Client App {N}” – can send and receive messages from “App 0 Manager”

### How to get started:
Files needed:
  * AppManager.py
  * ClientApp.py
  * ClientApp.py


#### How to run applications
```python 
python AppManager.py 
python ClientApp.py
python ClientApp.py
```


