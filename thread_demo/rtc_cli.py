import cmd
import socket
import sys
import time

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
address = ('127.0.0.1', 9999)
udp_socket.bind(address)


def recv_msg():
    while True:
        msg, addr = udp_socket.recvfrom(1024)
        print(f'收到来自{str(addr)}的信息:{msg.decode("utf-8")}')


class RTCShell(cmd.Cmd):
    intro = 'Welcome to RTC shell. Type help or ? to list commands.\n'
    prompt = 'rtc_cli> '
    answer_received = False
    dbus_handler = None

    def default(self, line):
        line = line.strip()
        for begin in ['#', '//']:
            if line.startswith(begin):
                return
        print('Unknown command: %s. Type help or ? to list allowed commands' % line)
        return

    def emptyline(self):
        pass

    def do_EOF(self, line):
        self.do_exit(line)

    def do_shutdown(self, line):
        self.do_exit(line)

    def do_exit(self, line):
        self.stop()
        print(line)
        sys.exit(0)

    def stop(self):
        if self.dbus_handler is not None:
            self.dbus_handler.stop()

    def do_hello(self, arg):
        print('hello', arg)

    def do_who_are_you(self, arg):
        try:
            udp_socket.sendto("who_are_you".encode('utf-8'), address)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    try:
        shell = RTCShell(stdin=sys.stdin)
        shell.cmdloop()
    except:
        exit()
        udp_socket.close()
