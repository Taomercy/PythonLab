import cmd
import socket
import sys
import threading
import time

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.settimeout(2.0)
address = ('127.0.0.1', 9999)
server_socket.connect(address)

recv_running = False


def recv_msg():
    global recv_running
    recv_running = True
    print("receive start")
    while True:
        if recv_running is False:
            server_socket.close()
            return
        try:
            msg, addr = server_socket.recvfrom(1024)
        except socket.timeout:
            continue
        print("receive from server:", msg.decode('utf-8'))


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
        global recv_running
        recv_running = False
        sys.exit(0)

    def stop(self):
        if self.dbus_handler is not None:
            self.dbus_handler.stop()

    def send_msg(self, context):
        try:
            server_socket.sendto(context.encode('utf-8'), address)
        except Exception as e:
            print(e)

    def do_hello(self, arg):
        print('hello', arg)

    def do_send(self, arg):
        self.send_msg(arg)

    def do_stop_server(self, arg):
        print("send")
        self.send_msg("stop_server")

    def do_who_are_you(self, arg):
        self.send_msg("who_are_you")


if __name__ == '__main__':
    thread_recv = threading.Thread(target=recv_msg)
    thread_recv.start()

    shell = RTCShell(stdin=sys.stdin)
    try:
        shell.cmdloop()
    except KeyboardInterrupt as e:
        recv_running = False
        thread_recv.join()
        server_socket.close()
        shell.stop()
        sys.exit()
    except:
        thread_recv.join()
        server_socket.close()
        sys.exit()

