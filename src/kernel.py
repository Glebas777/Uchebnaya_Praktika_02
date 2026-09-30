import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from syscalls import sys_echo, sys_get_users, sys_login


class Kernel:
    def __init__(self):
        self.current_user = None

    def call(self, name, *args):
        if name == 'sys_echo':
            return sys_echo(*args, user=self.current_user or 'guest')
        elif name == 'sys_get_users':
            return sys_get_users(user=self.current_user or 'guest')
        elif name == 'sys_login':
            result = sys_login(*args, user=self.current_user or 'guest')
            if result:
                self.current_user = result['login']
            return result
        else:
            return f'[kernel] Неизвестный системный вызов: {name}'

    def whoami(self):
        return self.current_user or 'guest'