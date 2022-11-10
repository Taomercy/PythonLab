#!/usr/bin/env python
# -*- coding:utf-8 -*-
import argparse
import socketserver
from socketserver import BaseRequestHandler
from controller import answer
from scheduler import CleanCheckResultScheduler, CleanCaseScheduler
from application.server.object import ServerLogger, Properties, Configuration
from hwwuex_check.utils.utils import remove_dir
DEBUG = None
config = Configuration()


def commandline():
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--ip", action='store', default="0.0.0.0",
                        help="server ip (default:0.0.0.0)", dest="ip")
    parser.add_argument("-p", "--port", action='store', default=8888, type=int,
                        help="server port (default:8888)", dest="port")
    parser.add_argument("-d", "--debug", action="store_true", default=False, dest="debug")

    args = parser.parse_args()
    return args


class Server(BaseRequestHandler):
    handle_space = None
    properties = None
    user = None
    client_name = None
    bufsize = 1024*50
    encoding = "utf-8"

    def setup(self):
        logger.info('Got a new connection from %s' % str(self.client_address))
        client_port = str(self.client_address[1])
        # receive user
        self.user = self.request.recv(1024).decode(self.encoding)
        # send client information
        self.client_name = "%s-%s" % (self.user, client_port)
        config.set_client(self.client_name)
        self.request.send(client_port.encode(self.encoding))
        # send storage path
        self.request.recv(1024).decode(self.encoding)
        self.request.send(config.case_root.encode(self.encoding))
        logger.debug("Send case path %s" % config.case_root)
        # create properties and workspace
        self.properties = Properties(self.user, client_port)
        self.handle_space = self.properties.workspace
        logger.debug("Create properties %s" % self.properties.file)

    def handle(self):
        Properties().add_or_update(log_level=log_level)
        while True:
            message = self.request.recv(self.bufsize).decode(self.encoding)
            if not message:
                break
            logger.info('receive message:{} from {}'.format(message, self.client_address))
            if DEBUG:
                response = answer(message)
                if not response:
                    self.request.send("None".encode(self.encoding))
                else:
                    self.request.send(response.encode(self.encoding))
            else:
                try:
                    response = answer(message)
                    if not response:
                        self.request.send("None".encode(self.encoding))
                    else:
                        self.request.send(response.encode(self.encoding))
                except Exception as e:
                    self.request.send(str(e).encode(self.encoding))
                    logger.error(e)
                    continue

    def finish(self):
        logger.info('Connection closed %s' % str(self.client_address))
        remove_dir(self.handle_space)
        logger.info("remove handler space %s" % self.handle_space)
        config.remove_client(self.client_name)


if __name__ == '__main__':
    args = commandline()
    ip = args.ip
    port = args.port
    config.add_or_update(ip=ip, port=port)
    DEBUG = args.debug
    if DEBUG:
        log_level = "debug"
    else:
        log_level = "info"

    logger = ServerLogger(file="server.log", level=log_level).logger
    server = socketserver.ThreadingTCPServer((ip, port), Server)
    logger.debug("server start.")

    ccrs = CleanCheckResultScheduler(level=log_level)
    ccrs.scheduler_start()
    ccs = CleanCaseScheduler(level=log_level)
    ccs.scheduler_start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.debug("server done.")
        ccrs.scheduler_shutdown()
        ccs.scheduler_shutdown()
        server.shutdown()
