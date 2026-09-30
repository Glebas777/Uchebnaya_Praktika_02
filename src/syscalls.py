import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from db import log_syscall, get_all_users, hash_password, find_user


def sys_echo(message, user='user'):
    log_syscall('sys_echo', message, user, 'ok')
    return message


def sys_get_users(user='user'):
    users = get_all_users()
    log_syscall('sys_get_users', '', user, 'ok')
    return users


def sys_login(login, password, user='guest'):
    found = find_user(login)
    if not found:
        log_syscall('sys_login', login, user, 'user_not_found')
        return None

    if found['password_hash'] != hash_password(password):
        log_syscall('sys_login', login, user, 'wrong_password')
        return None

    log_syscall('sys_login', login, user, 'ok')
    return {'login': found['login'], 'role': found['role']}