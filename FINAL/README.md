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

  This solution is Terminal-based and the following steps can be followed for execution.
    * Have python3 installed on your machine
              * Nested bullet
                  * Sub-nested bullet etc
    * Create a virtual environment for the program to be executed
      * Link to creating a virtual environment on Windows: [CLICK HERE] <https://linuxhint.com/python-requirements-txt-file/>
      * Link to creating a virtual environment on Linux: [CLICK HERE] <https://mothergeo-py.readthedocs.io/en/latest/development/how-to/venv.html>
              


#### How to run applications
```python 
python AppManager.py 
python ClientApp.py
python ClientApp.py
```


### Features
- [x] Client App {N} is able to send and receive messages **asynchronously**
- [x] App 0 Manager is able to send and receive messages __asynchronously__
- [x] App 0 Manager is able to receive messages from any clients prior to the establiishment of connections
- [ ] UI/UX for exchanging messages instead of using a Linux or Windows terminal


