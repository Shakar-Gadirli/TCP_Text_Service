import argparse, socket, sys, os, json
from itertools import cycle

class Server:
    MAX_BYTES = 65535
    def __init__(self,host,port):
        self.host=host
        self.port=port
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    
    def change_text(self,file1,file2):
        content_to_process=file1
        json_content=file2
        js = json.loads(json_content)
        
        for k in js:
            content_to_process = content_to_process.replace(k,js[k])
        return content_to_process

    def encrypt_decrypt(self,file1,file2):
        content_to_process = file1
        key = file2        
        xored = [chr(ord(a) ^ ord(b)) for a,b in zip(content_to_process, cycle(key))]
        return "".join(xored)

    def start(self):
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)
        print("\nThe server is listening at:", self.sock.getsockname())

        while True:
            sc, sockname = self.sock.accept()
            print('[+] We have accepted a connection from', sockname)

            print("\n[+] Receiving files from: ",sc.getpeername())
            mode, file1, file2 = sc.recv(self.MAX_BYTES).decode().split("ə")
            print("\n[+] Processing files...")
            if mode == "change_text":
                changed_text = self.change_text(file1,file2)
                print("\n[+] Sending processed file to: ",sc.getpeername())
                sc.send(changed_text.encode())
            elif mode == "encode_decode":
                changed_text = self.encrypt_decrypt(file1,file2)
                print("\n[+] Sending processed file to: ",sc.getpeername())
                sc.sendall(changed_text.encode())
            sc.close()
            print("="*60)


class Client:
    MAX_BYTES=65535
    def __init__(self,host,port,mode):
        self.host=host
        self.port=port
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.mode= mode


    def case_1(self,file1,file2):
        main_file = open(file1,"r")
        file_1_content = main_file.read()
        main_file_name=main_file.name.split(".txt")[0]
        main_file.close()
        
        jsonFile=open(file2,"r")
        file_2_content=jsonFile.read()
        jsonFile.close()

        print("\n[+] Sending files...")
        self.sock.sendall(str.encode("%".join([self.mode,file_1_content,file_2_content])))
        
        #receive modified content
        print("\n[+] Receiving processed file...")
        modified_content = self.sock.recv(self.MAX_BYTES)
        modified_file = open("Processed_" + main_file_name + ".txt","wb")
        modified_file.write(modified_content)
        modified_file.close()

    def case_2(self,file1,file2):
        plaintext_file = open(file1,"r")
        file_1_content = plaintext_file.read()
        #plaintext_file_name = plaintext_file.name.split(".txt")[0]
        plaintext_file.close()
        key_file = open(file2,"r")
        file_2_content = key_file.read()
        key_file.close()

        print("\n[+] Sending files...")
        self.sock.sendall(str.encode("ə".join([self.mode,file_1_content,file_2_content])))

        #receive encrypted/decrypted file
        print("\n[+] Receiving processed file...")
        modified_content = self.sock.recv(self.MAX_BYTES)
        modified_file = open("XOR"+".txt","wb")
        modified_file.write(modified_content)
        modified_file.close()



    def start(self,file1,file2):
        self.sock.connect((self.host,self.port))
        print('Client has been assigned socket name', self.sock.getsockname())
        if self.mode == "change_text":
            self.case_1(file1,file2)
        elif self.mode == "encode_decode":
            self.case_2(file1,file2)


if __name__=="__main__":
    parser = argparse.ArgumentParser(description = "TCP file transfer")
    choices = {"server": Server, "client": Client}
    parser.add_argument('role', choices = choices, help = "server or client")
    parser.add_argument("host", help="interface server listens at; hostname client sends to")
    parser.add_argument("-p", metavar="PORT", type=int, default=1060, help="Port (default 1060)")
    
    if sys.argv[1] == "client":
        parser.add_argument('--mode', type = str,help="mode (change_text or encode_decode)")
        parser.add_argument('file1', type = str, help = "1st filename")
        parser.add_argument('file2', type = str, help = "2nd filename")
    
    args = parser.parse_args()
    Class = choices[args.role]

    if args.role == "client":
        cl_obj = Class(args.host, args.p,args.mode)
        cl_obj.start(args.file1, args.file2)
    elif args.role == "server":
        s_obj = Class(args.host,args.p)
        s_obj.start()

