import cmd
import os
import platform
import socket
import sys

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.settimeout(3.0)
address = ('127.0.0.1', 9999)
udp_socket.connect(address)


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
        # self.stop()
        sys.exit(0)

    def stop(self):
        if self.dbus_handler is not None:
            self.dbus_handler.stop()

    def send_msg(self, context):
        try:
            udp_socket.sendto(context.encode('utf-8'), address)
        except Exception as e:
            print(e)
        self.receive_msg()

    @staticmethod
    def receive_msg():
        try:
            msg, addr = udp_socket.recvfrom(1024)
            print("message from server:", msg.decode('utf-8'))
        except Exception as e:
            print(e)

    def do_hello(self, arg):
        self.send_msg('hello')

    def do_send(self, arg):
        self.send_msg(arg)

    def do_stop_server(self, arg):
        self.send_msg("stop_server")

    def do_who_are_you(self, arg):
        self.send_msg("who_are_you")

    def do_add(self, arg):
        print(sum([int(i) for i in arg.split(" ")]))

    def do_clear(self, arg):
        system_version = platform.system()
        if system_version == "Windows":
            os.system("cls")
        elif system_version == "Linux":
            os.system("clear")
        else:
            print("cannot recognise system:", system_version)


if __name__ == '__main__':
    shell = RTCShell(stdin=sys.stdin)
    try:
        shell.cmdloop()
    except KeyboardInterrupt as e:
        udp_socket.close()
        shell.stop()
        sys.exit()
    except:
        udp_socket.close()
        sys.exit()

