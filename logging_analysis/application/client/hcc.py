#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import argparse
import getpass
import os
import re
import shutil
import socket
import subprocess
import sys
import tarfile
import time
from cmd import Cmd

def run_command(cmd, visible=True):
    (status, output) = subprocess.getstatusoutput(cmd)
    if visible:
        if status:
            print(output)
        else:
            if output:
                print(output)
            else:
                print("success")


def un_tar(file_name, target_dir):
    tar = tarfile.open(file_name)
    names = tar.getnames()

    if not os.path.isdir(target_dir):
        os.mkdir(target_dir)

    for name in names:
        tar.extract(name, target_dir)
    tar.close()
    return target_dir


def commandline():
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--ip", action='store', default="10.120.115.52",
                        help="server ip (default:10.120.115.52)", dest="ip")
    parser.add_argument("-p", "--port", action='store', default=8888, type=int,
                        help="server port (default:8888)", dest="port")
    parser.add_argument("-l", "--log", action="store", dest="log")
    parser.add_argument("-stb", "--stability", action="store_const", const="stability", dest="type")
    parser.add_argument("-acc", "--accuracy", action="store_const", const="accuracy", dest="type")
    parser.add_argument("-rob", "--robustness", action="store_const", const="robustness", dest="type")
    parser.add_argument("-sum", "--summary", action="store", dest="summary")
    parser.add_argument("-user", "--user", action="store", default=None, dest="user", help=argparse.SUPPRESS)
    parser.add_argument("-c", "--command", action='store', default=None,
                        help="exec command", dest="command")
    parser.add_argument("-u", "--upload", action='store', default=None,
                        help="upload case path", dest="upload_path")

    args = parser.parse_args()
    return args


class Client(Cmd):
    ip = None
    port = None
    bufsize = 1024*50
    address = None
    client_socket = None
    intro = "Welcome to hss check client. Type help or ? to list commands.\n"
    prompt = "hcc> "
    commands = []
    case_storage_path = None

    def __init__(self, ip, port, stdin=sys.stdin, user=None):
        super().__init__(stdin=stdin)
        self.ip = ip
        self.port = port
        self.address = (ip, port)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(7200.0)
        if user:
            self.user = user
        else:
            self.user = getpass.getuser()
        self.user_message = "user:"+self.user
        self.client_socket.connect(self.address)

        # receive client port
        self.client_socket.sendto(self.user.encode('utf-8'), self.address)
        response, address = self.client_socket.recvfrom(self.bufsize)
        self.client_port = response.decode('utf-8')

        # receive storage path
        self.client_socket.sendto("storage".encode('utf-8'), self.address)
        response, address = self.client_socket.recvfrom(self.bufsize)
        self.case_storage_path = response.decode('utf-8')

        self.prompt = "%s@hcc(%s)[%s]> " % (self.user, self.client_port, os.getcwd())

    def default(self, line):
        line = line.strip()
        for begin in ['#', '//']:
            if line.startswith(begin):
                return
        print('Unknown command: %s. Type help or ? to list allowed commands' % line)
        return

    def emptyline(self):
        pass

    def send_msg(self, line, visible=True):
        self.save_command(line)
        self.client_socket.sendto(line.encode('utf-8'), self.address)
        response = self.receive_msg(visible=visible)
        return response

    def receive_msg(self, visible=True):
        try:
            response, address = self.client_socket.recvfrom(self.bufsize)
        except socket.timeout:
            return None

        if response:
            if visible:
                print(response.decode('utf-8'))
            return response.decode('utf-8')

    def save_command(self, c):
        if len(self.commands) < 10:
            self.commands.append(c)
        else:
            del self.commands[0]
            self.commands.append(c)

    def upload(self, log):
        if "/" not in log:
            case_path = os.path.join(os.getcwd(), log)
        else:
            case_path = log
        cmd = "cp -r %s %s" % (case_path, self.case_storage_path)
        print("Uploading...")
        run_command(cmd, visible=False)

        log_basename = os.path.basename(log)
        storage_log = os.path.join(self.case_storage_path, log_basename)
        if not os.path.exists(storage_log):
            print("Upload Failed.")

        if ".tar" in log:
            un_tar(log, self.case_storage_path)
            os.remove(os.path.join(self.case_storage_path, log_basename))
            storage_log = storage_log.split(".tar")[0]

        cmd = "chmod -R 777 %s" % storage_log
        run_command(cmd, visible=False)

    def do_EOF(self, arg):
        self.do_exit(arg)

    def do_shutdown(self, arg):
        self.do_exit(arg)

    def do_exit(self, arg):
        self.client_socket.close()
        sys.exit(0)

    # def do_help(self, arg):
    #     self.send_msg("help")

    def do_history(self, arg):
        for c in self.commands:
            print(c)

    def do_who(self, arg):
        self.send_msg("who")

    def do_cd(self, arg):
        try:
            os.chdir(arg)
            self.prompt = "%s@hcc(%s)[%s]> " % (self.user, self.client_port, os.getcwd())
        except Exception as e:
            print(e)

    def do_clear(self, arg):
        os.system("clear")

    def do_ls(self, arg):
        os.system("ls")

    def do_pwd(self, arg):
        os.system("pwd")

    def do_cat(self, arg):
        try:
            cmd = "cat %s" % arg
            run_command(cmd)
        except:
            self.send_msg("cat " + arg)

    # def do_check_result_save_latest(self, arg):
    #     output_path = os.path.join(self.case_storage_path, "output")
    #     paths = os.listdir(output_path)
    #     my_check = []
    #     for path in paths:
    #         if self.user in path and os.listdir(os.path.join(output_path, path)):
    #             my_check.append(path)
    #     my_check.sort(key=lambda i: int(i.split("-")[-1]))
    #     my_latest_check = my_check[-1]
    #     my_latest_path = os.path.join(output_path, my_latest_check)
    #     self.send_msg("chmod -R 777 " + my_latest_path, False)
    #     if arg:
    #         cmd = "cp -r %s %s" % (my_latest_path, arg)
    #     else:
    #         cmd = "cp -r %s %s" % (my_latest_path, os.path.join(os.getcwd(), my_latest_check))
    #     run_command(cmd)

    def do_check_result_list(self, arg):
        self.send_msg("check_result_list")

    def do_check_result_clean(self, arg):
        if arg:
            self.send_msg("check_result_clean " + arg)
        else:
            self.send_msg("check_result_clean")

    def do_case_path_list(self, arg):
        self.send_msg("case_path_list")

    def do_case_path_upload(self, arg):
        if not arg:
            print("Please input case path")
            return
        if "TC-" not in arg:
            print("It's not start with 'TC', maybe not a case path.")
            return
        case_path_list = self.send_msg("case_path_list", False).split("\n")
        if os.path.basename(arg) in case_path_list:
            print("The case path is existed")
            return
        if arg.endswith("/"):
            arg = arg[:-1]
        self.upload(arg)

    def do_case_path_remove(self, arg):
        if "TC-" not in arg:
            print("The directory is not a case path")
        else:
            case_path = os.path.join(self.case_storage_path, arg)
            cmd = "rm -rf %s" % case_path
            run_command(cmd)

    def do_summary(self, arg):
        self.send_msg("summary")

    def do_properties_list(self, arg):
        self.send_msg("properties_list")

    def do_properties_show(self, arg):
        if arg:
            self.send_msg("properties_show " + arg)
        else:
            self.send_msg("properties_show")

    def help_properties_show(self):
        print("properties_show: display your current properties")
        print("properties_show ${filename}: display target properties")

    def do_properties_save(self, arg):
        self.send_msg("properties_save")

    def do_properties_remove(self, arg):
        self.send_msg("properties_remove " + arg)

    def do_properties_copy(self, arg):
        self.send_msg("properties_copy " + arg)

    def do_properties_delete(self, arg):
        self.send_msg("properties_delete " + arg)

    def do_properties_update(self, arg):
        self.send_msg("properties_update " + arg)

    def help_properties_update(self):
        print("properties_update ${key1}=${value1},${key2}=${value2}")

    def do_hwwuex_check(self, arg):
        self.send_msg("hwwuex_check " + arg)

    def do_stability_check(self, arg):
        self.send_msg("stability_check " + arg)

    def help_stability_check(self):
        print('''\nRUN_STABILITY_CHECK
                \nstability_check log_path options[default all:alarm.error rate,load,memory].''')

    def do_upgrade_check(self, arg):
        self.send_msg("upgrade_check " + arg)

    def help_upgrade_check(self):
        print('''\nRUN_UPGRADE_CHECK
                \nupgrade_check log_path options[default all:ca,upgrade time].''')

    def do_robustness_check(self, arg):
        self.send_msg("robustness_check " + arg)

    def help_robustness_check(self):
        print('''\nRUN_ROBUSTNESS_CHECK
                \nrobustness_check log_path options[default all:alarm,applogs,process].''')

    def do_accuracy_check(self, arg):
        self.send_msg("accuracy_check " + arg)

    def help_accuracy_check(self):
        print('''\nRUN_ACCURACY_CHECK
                \naccuracy_check log_path options[default all:alarm,applogs].''')


if __name__ == '__main__':
    args = commandline()
    ip = args.ip
    port = args.port
    upload_path = args.upload_path
    command = args.command

    client = Client(ip, port, stdin=sys.stdin, user=args.user)

    if args.type and not args.log:
        print("Please input log path: [-l LOG]")
        client.client_socket.close()
        sys.exit()

    if args.log:
        log = args.log
        if log.endswith("/"):
            log = log[:-1]

        log_basename = os.path.basename(log)
        case_storage_path = os.path.join(client.case_storage_path, log_basename)
        if os.path.exists(case_storage_path):
            print("Log (%s) had been existed." % log_basename)
        else:
            client.upload(log)

        case_path = os.path.join(os.getcwd(), log)
        if args.type:
            cmd = "{}_check {}".format(args.type, log_basename)
        else:
            cmd = "hwwuex_check {}".format(log_basename)

        # request to server
        print("Checking...")
        response = client.send_msg(cmd, visible=False)

        # copy result
        try:
            pattern = re.compile(r"//*.*/[0-9]{14}")
            res = re.findall(pattern, response)
            if res:
                result_path = res[0]
                local_path = os.path.join(case_path, "result")
                if os.path.exists(local_path):
                    shutil.rmtree(local_path)
                os.makedirs(local_path)

                # display response
                response = response.replace(result_path, local_path)
                print(response)

                # save result into local
                cmd = "cp -rf {}/* {}".format(result_path, local_path)
                print("Saving result into {}".format(local_path))
                # wait for the result to be fully written
                time.sleep(30)
                run_command(cmd, visible=False)

                # summary log
                if args.summary:
                    with open(os.path.join(local_path, "summary.log"), "r+") as f:
                        context = f.read()
                        context = context.replace(result_path, local_path)
                        f.seek(0)
                        f.write(context)

                    with open(os.path.join(os.getcwd(), args.summary), "a") as fw:
                        fw.write(context)
                        fw.write("\n\n\n")
        except Exception as e:
            print(e)

        # remove log
        # cmd = "rm -rf %s" % case_storage_path
        # run_command(cmd, visible=False)
        print("Complete.")
        client.client_socket.close()
        sys.exit()

    if upload_path:
        client.upload(upload_path)
        client.client_socket.close()
        sys.exit()

    if command:
        client.send_msg(command)
        client.client_socket.close()
        sys.exit()
    else:
        try:
            client.cmdloop()
        except KeyboardInterrupt as e:
            client.client_socket.close()
            print("")
            sys.exit()
