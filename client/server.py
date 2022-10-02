#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rich.console import Console
from io import BytesIO
import socket
import json
import formats

console = Console()
config  = None

def init(conf: dict) -> socket.SocketIO | None:
    global config
    config = conf
    sock   = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        sock.bind(tuple(conf["host"]["local"]))
    except OSError:
        console.log(f"[red][E] 无法在 {config['host']['local']} 开启服务器：地址被占用")
        return None
    except TypeError:
        console.print_exception()
        console.log(f"[red][E] 无法识别的地址：{config['host']['local']}")
        return None
    
    sock.listen(1024)
    
    console.log(f"[I] 服务器已在 {config['host']['local']} 开放")

    return sock

def to_remote(recv_data: dict) -> tuple:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        sock.connect(tuple(config["host"]["remote"]))
        sock.send(json.dumps(recv_data).encode("utf-8"))
        recv = sock.recv(1024)
    except Exception as e:
        console.print_exception()
        return recv_data["Request-HttpType"].encode("utf-8") + b" " + formats.formatResponse("text/html", "520 Time Out", str(e))
    
    return recv




def handle(sock, addr):
    recv_data = formats.formatRequest(BytesIO(sock.recv(1024)))
    console.log(f"[I] {addr[0]} - {recv_data['Request-Method']} {recv_data['Request-URI']} {recv_data['Request-HttpType']}")
    console.log(recv_data)

    resp_data = to_remote(recv_data)

    sock.send(resp_data)
    sock.close()

