import pexpect


class Connection(object):
    def __init__(self, user, host, password):
        self.__user = user
        self. __host = host
        self.__password = password
        self.prompt = ['#', '>>>', '>', '\$']
        self.child = self.connect

    @property
    def user(self):
        return self.__user

    @property
    def host(self):
        return self.__host

    @property
    def password(self):
        return self.__password

    @property
    def connect(self):
        ssh_newkey = 'Are you sure you want to continue connecting'
        connStr = 'ssh ' + self.user + '@' + self.host

        # generate a object of spawn class for ssh command
        child = pexpect.spawn(connStr)

        # expect ssh_newkey prompt，or timeout
        ret = child.expect([pexpect.TIMEOUT, ssh_newkey, '[P|p]assword: '])

        # TIMEOUT
        if ret == 0:
            print('[-] Error Connecting')
            return None

        # ssh_newkey
        if ret == 1:
            child.sendline('yes')
            ret = child.expect([pexpect.TIMEOUT, '[P|p]assword: '])

        # TIMEOUT
        if ret == 0:
            print('[-] Error Connecting')
            return None

        # send password
        child.sendline(self.password)
        child.expect(self.prompt)
        return child

    def send_command(self, cmd):
        result = None
        if self.child:
            # send command
            self.child.sendline(cmd)
            # expected prompt
            self.child.expect(self.prompt)

            result = self.child.before
            self.child.close()
        return result