#!/usr/bin/env python
# -*- coding:utf-8 -*-
import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
import time
import gobject

MSG_OBJ_PATH = "/com/example/msg"
MSG_INTERFACE_URI = "com.example.msg"

TIMEFORMAT = "%H:%M:%S"


class Msg(dbus.service.Object):
    def __init__(self,bus,object_path):
        dbus.service.Object.__init__(self,bus,object_path)

    @dbus.service.method(dbus_interface=MSG_INTERFACE_URI,
                         in_signature='', out_signature='s')
    def say_hello(self):
        return "hello, exported method"

    @dbus.service.signal(dbus_interface=MSG_INTERFACE_URI,
                         signature='as')
    def msg_signal(self,msg_list):
        print("exported signal: ",msg_list)

    def construct_msg(self):
        timeStamp = time.strftime(TIMEFORMAT)
        self.msg_signal(["1111",timeStamp,"This is the content","1 2 3"])
        return True


if __name__ == "__main__":
    DBusGMainLoop(set_as_default=True)
    bus = dbus.SessionBus()
    aMsg = Msg(bus, MSG_OBJ_PATH)

    gobject.timeout_add(1000, aMsg.construct_msg)
    loop = gobject.MainLoop()
    loop.run()