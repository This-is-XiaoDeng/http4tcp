#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rich.console import Console
import socket
import sys
import json
import requests
import urllib.parse
import threading

console = Console()
config  = json.load(open("./config.json"))

def get_header(recv):
    for k in list(recv.keys()):
        if k[:8] == "Request-" or k == "Content-Lines":
            recv.pop(k)
    return recv

def handle(sock, addr):
    recv_data = json.loads(sock.recv(1024).decode("utf-8"))
    console.log(f"[I] {addr[0]} - {recv_data['Request-Method']} {recv_data['Request-URI']} {recv_data['Request-HttpType']}")
    header = get_header(recv_data.copy())

    if recv_data["Request-Method"] == "GET":
        req = requests.get(config["url"] + recv_data["Request-URI"], headers = header)
        resp_data = req.content
    else:
        req = requests.post(config["url"] + recv_data["Request-URI"], urllib.parse.parse_qs(recv_data["Content-Lines"][0]), headers = header)
        resp_data = req.content
    
    get_headers = req.headers
    sock.send(f"{recv_data['Request-HttpType']} {req.status_code} OK\r\nContent-Type: {get_headers['Content-Type']}\r\n\r\n".encode("utf-8") + resp_data)
    sock.close()

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        sock.bind(("", config["port"]))
    except OSError:
        console.print_exception()
        console.log(f"[E] 无法监听 {config['port']} 端口，该端口已被占用")
        sys.exit()
    except TypeError:
        console.print_exception()
        console.log(f"[E] 端口 {config['port']} (Type: {type(config['port'])}) 不是一个有效的端口")
        sys.exit()
    
    sock.listen(1024)

    console.log(f"[I] 服务器已在 0.0.0.0:{config['port']} 开放")
    while True:
        new_sock, addr = sock.accept()
    
        threading.Thread(target= handle, args = (new_sock, addr)).start()
