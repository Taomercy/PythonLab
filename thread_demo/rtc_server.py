import queue
import socket
import threading
import time
from queue import Queue


class RemoteControl(threading.Thread):
    def __init__(self, rtc_data, udp_port=9999):
        threading.Thread.__init__(self)
        self.__id = "REMOTE_CONTROL"
        self.__rtc_data = rtc_data

        self.__udp_socket = None
        self.__udp_port = udp_port
        self.__running = False
        self.__force_exit = False
        self.answers = Queue(maxsize=0)

    @property
    def id(self):
        return self.__id

    @property
    def rtc_data(self):
        return self.__rtc_data

    @property
    def force_exit(self):
        return self.__force_exit

    def clean_subscriptions(self):
        self.__subscriptions = {}

    def subscribe(self, cmd, queue):
        try:
            self.__subscriptions[cmd] += [queue]
        except KeyError:
            self.__subscriptions.update({cmd:[queue]})

    def find_subscription(self, cmd):
        try:
            return self.__subscriptions[cmd]
        except KeyError:
            return []

    def start_udp_server(self):
        print("udp server start")
        self.__udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__udp_socket.settimeout(5.0)
        self.__udp_socket.bind(('0.0.0.0', self.__udp_port))
        self.__running = True

    def shutdown(self):
        print('remote control shutdown')
        if self.__running:
            self.__force_exit = True
            if self.is_alive:
                self.join(5.0)
            self.__udp_socket.close()
            self.__udp_socket = None
            self.__running = False

    def read_udp_cmd(self):
        try:
            data, client = self.__udp_socket.recvfrom(4096)
        except KeyboardInterrupt as e:
            print(e)
            return
        except socket.timeout:
            return

        data = data.strip()
        print("receive data:", data.decode("utf-8"))
        try:
            cmd = data.split()[0]
            print("cmd:", cmd)
        except IndexError:
            answer = 'HSS_rtc command NOT VALID'
            sent = self.__udp_socket.sendto(answer, client)
            return

        if cmd == "who_are_you":
            answer = 'HSS_rtc'
            sent = self.__udp_socket.sendto(answer, client)
        elif cmd == 'quit':
            answer = 'ORDERED'
            sent = self.__udp_socket.sendto(answer, client)
            rtc.paused = False
            self.rtc_data.exit_rtc = True
        else:
            sent = self.__udp_socket.sendto("Done", client)

    def run(self):
        print("read_udp_cmd is running")
        while self.__running:
            if self.force_exit:
                print("read_udp_cmd is done")
                return
            self.read_udp_cmd()
        print('%s end of thread execution' % self.id)


class RTCData(object):
    def __init__(self):
        self.__remote_control = RemoteControl(self)
        self.__exit_rtc = False

    @property
    def remote_control(self):
        return self.__remote_control

    def start_remote_control(self):
        self.remote_control.start_udp_server()
        self.remote_control.start()

    def stop_remote_control(self):
        self.remote_control.shutdown()

    def finish(self):
        print("finish")


class RTCController(object):
    def __init__(self, rtc_data):
        self.__rtc_data = rtc_data
        self.__paused = False

    @property
    def rtc_data(self):
        return self.__rtc_data

    def release(self):
        self.rtc_data.remote_control.shutdown()
        self.rtc_data.finish()

    def run(self):
        self.rtc_data.start_remote_control()
        print('RTC execution start')
        while True:
            while self.__paused:
                print('RTC in paused state')
                time.sleep(5.0)

            try:
                send_data = input("==>")
                print(send_data)
            except KeyboardInterrupt:
                self.rtc_data.exit_rtc = True
                break

        self.rtc_data.stop_remote_control()


if __name__ == '__main__':
    rtc_data = RTCData()
    rtc = RTCController(rtc_data)
    rtc.run()

