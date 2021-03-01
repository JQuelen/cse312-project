#from flask import Flask, send_from_directory, render_template
import socketserver
import sys

#app = Flask(__name__)

class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        received_data = self.request.recv(1024).strip()
        print(self.client_address[0] + " is sending data:")
        print(received_data.decode())
        print("\n\n")
        sys.stdout.flush()
        #if requestType == "GET" & requestPath == "/":
            #self.request.sendall("HTTP/1.1 200 ok\r\nContent-Length: s\r\n\r\nhello".encode())
        #else:
            #self.request.sendall("HTTP/1.1 404 Not Found\r\nContent-Length: s\r\n\r\n404 Error".encode())

        self.request.sendall("HTTP/1.1 200 ok\r\nContent-Length: s\r\n\r\nhello".encode())





if __name__ == '__main__':
    host = "0.0.0.0"
    port = 8000

    server = socketserver.ThreadingTCPServer((host, port), MyTCPHandler)
    server.serve_forever()

