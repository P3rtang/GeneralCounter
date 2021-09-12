import sys
from time import sleep


def main(args):
    with open('C:\\Users\\tom-v\\Documents\\GitHub\\GeneralCounter\\bin\\dump.txt', 'w') as dump_file:
        dump_file.write(str(args))


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
