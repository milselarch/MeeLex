#!/usr/bin/env python

import sys, os, socket
import threading

from socketserver import ThreadingMixIn
from http.server import BaseHTTPRequestHandler, HTTPServer

class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    pass

# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
    # GET
    def do_GET(self):
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Send message back to client
        message = "Hello world!"
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        return

def run(threaded=False):
    print('starting server...')

    # Server settings
    # Choose port 8080, for port 80, which is normally used for a http server, you need root access
    server_address = ('127.0.0.1', 30000)
    httpd = ThreadingHTTPServer(server_address, testHTTPServer_RequestHandler)
    print('running server...')

    if threaded == False:
        httpd.serve_forever()
    else:
        threading.Thread(target=httpd.serve_forever).start()


if __name__ == "__main__":
    run()
