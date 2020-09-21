import hashlib
import sys


def show_hash(user, password, salt=None):
    secret = user + password
    if salt:
        secret = secret + salt
    print(hashlib.md5(secret.encode()).hexdigest())


def main():
    args = sys.argv
    if 3 <= len(args) <= 4:
        show_hash(args[1], args[2], args[3 if len(args) == 4 else None])
    else:
        print('Usage: app user password [salt]')


if __name__ == '__main__':
    main()
    # show_hash('zeus', 'zeus', 'mblog')  # 167b208b5899df2a16a8c0b1d19a4c24
