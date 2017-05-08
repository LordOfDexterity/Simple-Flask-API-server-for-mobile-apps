#!mobserv/bin/python
import socket
import fcntl
import struct

from app import app


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,
        struct.pack('256s', ifname[:15])
    )[20:24])

HOST_IP_ADDRESS = get_ip_address('enp0s3')
app.run(debug=True, host=HOST_IP_ADDRESS)
