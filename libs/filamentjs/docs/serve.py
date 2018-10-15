#!/usr/bin/env python3

import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CURRENT_DIR = os.getcwd()
ROOT_DIR = '../../../'
SERVE_DIR = ROOT_DIR + 'docs'
FILAMENT_DIR = ROOT_DIR + 'out/cmake-webgl-release/libs/filamentjs'
EXEC_NAME = os.path.basename(sys.argv[0])
SCRIPT_NAME = os.path.basename(__file__)
PORT = 8000

# The pipenv command in the shebang needs a certain working directory.
if EXEC_NAME == SCRIPT_NAME and SCRIPT_DIR != CURRENT_DIR:
    relative_script_path = os.path.dirname(__file__)
    quit(f"Please run script from {relative_script_path}")

import http.server
import socketserver

os.system(f"ls -l {SERVE_DIR}")
os.system(f"lsof -nP -i4TCP:{PORT}")

# Crucially, associate wasm files with the correct MIME type.
Handler = http.server.SimpleHTTPRequestHandler
Handler.extensions_map.update({
    '.wasm': 'application/wasm',
})

# Serve all files in the script folder.
Handler.directory = SERVE_DIR
os.chdir(SERVE_DIR)
socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    httpd.allow_reuse_address = True
    print("serving at port", PORT)
    httpd.serve_forever()
