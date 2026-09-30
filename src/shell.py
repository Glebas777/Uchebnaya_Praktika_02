import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kernel import Kernel
from db import init_db


BANNER = '''
========================================
  my_os — учебная операционная система
  Python + SQLite
========================================
Введите "help" для списка команд.
'''


def print_help():
    print('''
Доступные команды:
  help                       — показать эту справку
  echo <сообщение>           — вывести сообщение через sys_echo
  users                      — список пользователей через sys_get_users
  login <логин> <пароль>     — вход в систему
  whoami                     — текущий пользователь
  clear                      — очистить экран
  exit                       — выход
''')


def main():
    init_db()
    kernel = Kernel()

    print(BANNER)

    while True:
        try:
            user = kernel.whoami()
            line = input(f'{user}@my_os> ').strip()
        except (EOFError, KeyboardInterrupt):
            print('\n[shell] Завершение работы.')
            break

        if not line:
            continue

        parts = line.split()
        cmd = parts[0].lower()
        args = parts[1:]

        if cmd == 'exit':
            print('[shell] Выход из системы.')
            break
        elif cmd == 'help':
            print_help()
        elif cmd == 'clear':
            os.system('clear')
        elif cmd == 'echo':
            message = ' '.join(args)
            result = kernel.call('sys_echo', message)
            print(result)
        elif cmd == 'users':
            users = kernel.call('sys_get_users')
            if not users:
                print('[shell] Нет пользователей.')
            else:
                print(f'{"ID":<5}{"ЛОГИН":<15}{"РОЛЬ":<20}')
                print('-' * 40)
                for u in users:
                    print(f'{u["id"]:<5}{u["login"]:<15}{u["role"]:<20}')
        elif cmd == 'login':
            if len(args) < 2:
                print('[shell] Использование: login <логин> <пароль>')
                continue
            result = kernel.call('sys_login', args[0], args[1])
            if result:
                print(f'[shell] Добро пожаловать, {result["login"]} ({result["role"]})')
            else:
                print('[shell] Ошибка входа: неверный логин или пароль.')
        elif cmd == 'whoami':
            print(kernel.whoami())
        else:
            print(f'[shell] Неизвестная команда: {cmd}. Введите "help".')


if __name__ == '__main__':
    main()