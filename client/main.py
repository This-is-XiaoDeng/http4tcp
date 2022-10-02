#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rich.console import Console
import json
import server
import sys
import threading

console = Console()
config  = json.load(open("./config.json"))
sock    = server.init(config)

if __name__ == "__main__" and sock:
    while True:
        new_sock, addr = sock.accept()
        threading.Thread(target = server.handle, args = (new_sock, addr)).start()

