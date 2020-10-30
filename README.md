# TCP Text Service
 In this consol app, the client sends 2 files to the server in one of the two modes (change_text/encode_decode). In respond, the server processes files according to the modes and sends new processed file to the client.
 ## Scenario
 *Modes*:
  - **change_text:** In this mode, the client sends a text file and a json file to the server. The server
reads the json file and replaces the words from the text file according to the json file. After, newly processed file will be sent to the client.
  - **encode_decode:** In this mode, the client sends 2 text files,  first and second file contains text and key, respectively. The server apply **XOR** operation to the first file by using the key inside the second file. **NOTE**: if the first file contains a plain text,then this file will be encoded, but if the first file contains encoded text, then it will be decoded by the server. After successful operations, newly processed file will be sent to the client.


**NOTE**:  In the first mode, *Processed_client_file.txt* will be created. In the second mode, *XOR.txt* file will be created. *XOR.txt* file will contain encoded or decoded file, according to the content of the first file (if it was plain text or encoded text). Both files will be sent to the client and saved inside the same directory where original files are located.

## Installation
Clone this repository into your directory
``` bash
git clone https://github.com/Shakar-Gadirli/TCP_Text_Service.git
```
Install requirements for this application.
```bash
pip3 install -r requirements.txt
```

## Usage
For server and client, open 2 terminal tabs. 
In the first tab, run the following command to create server.
```bash
python3 text_service.py server ""
```
Here, **""** represents the interface for server to accept incoming data. By default the port 1060 will be used. If you want to specify port, then add *-p port_number* at the end. (like -p 5555).

In the second tab, run the following command to create client.
```bash
python3 text_service.py hostname --mode change_text file1.txt file2.json
```
OR
``` bash
python3 text_service.py hostname --mode encode_decode file.txt key.txt
```
Here instead of "hostname", hostname of your local machine should be written. By default, the client will send to the port 1060, but you can add the port number (one that you specified in the server) after the *hostname*. (like  -p 5555)

**NOTE:** 
After, sending *plain_text.txt* and *key.txt* to the server, the server will send you **XOR.txt** which will be **encoded text**, You can send **XOR.txt** with the same *key.txt* file to the server, again. The server will decode **XOR.txt** and send it back to you. So, you will see that, **XOR.txt** is **decrypted and has the same content with plain_text.txt**

