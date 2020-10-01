from oscpy.server import OSCThreadServer
from oscpy.client import OSCClient
from time import sleep

CLIENT = OSCClient('localhost', 3002)


def send_data(i):
    CLIENT.send_message(
        b'/activation',
        ['Etkin'.encode("UTF-8"), ],
    )
    CLIENT.send_message(
        b'/activation',
        [str(i).encode("UTF-8"), ],
    )


i = 0
if __name__ == '__main__':
    SERVER = OSCThreadServer()
    SERVER.listen('localhost', port=3000, default=True)
    while True:
        i += 1
        sleep(0.3)
        send_data(i)