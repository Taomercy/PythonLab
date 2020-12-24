import queue
import socket
import sys
import threading
import time
from queue import Queue
rtc = None
hello_count = 0


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
        self.__udp_socket.settimeout(3.0)
        self.__udp_socket.bind(('100.98.218.151', self.__udp_port))
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

    def send_msg(self, context, client):
        #print(context)
        try:
            self.__udp_socket.sendto(context.encode("utf-8"), client)
        except Exception as e:
            print(e)

    def read_udp_cmd(self):
        try:
            data, client = self.__udp_socket.recvfrom(4096)
        except KeyboardInterrupt as e:
            print(e)
            return
        except socket.timeout:
            return

        data = data.strip().decode("utf-8")
        try:
            cmd = data.split()[0]
            print("cmd:", cmd)
        except IndexError:
            answer = 'HSS_rtc command NOT VALID'
            self.send_msg(answer, client)
            return

        if cmd == "who_are_you":
            answer = 'HSS RTC'
            self.send_msg(answer, client)
        elif cmd == 'stop_server':
            answer = 'STOPED'
            self.send_msg(answer, client)
            self.rtc_data.exit_rtc = True
            rtc.set_exit()
        elif cmd == 'hello':
            global hello_count
            hello_count += 1
            answer = 'Hello Commander! ({}/5)'.format(hello_count)
            if hello_count == 5:
                hello_count = 0
                answer += "\nMission accomplished"
            self.send_msg(answer, client)
        else:
            return

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
        self.__exit = False

    @property
    def rtc_data(self):
        return self.__rtc_data

    def set_exit(self):
        self.__exit = True

    def release(self):
        self.rtc_data.remote_control.shutdown()
        self.rtc_data.finish()

    def run(self):
        self.rtc_data.start_remote_control()
        print('RTC execution start')
        while True:
            if self.__exit:
                print('RTC will close after 5s')
                time.sleep(5.0)
                self.rtc_data.exit_rtc = True
                break

            try:
                send_data = input("rtc_server> ")
                print(send_data)
            except KeyboardInterrupt:
                self.rtc_data.exit_rtc = True
                break

        self.rtc_data.stop_remote_control()


if __name__ == '__main__':
    rtc_data = RTCData()
    rtc = RTCController(rtc_data)
    rtc.run()

