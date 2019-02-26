import socket
import json
import sys
import ConfigParser


def main():
    config = ConfigParser.ConfigParser()
    config.read('xmppbot.conf')

    jsonmsg = dict()

    jsonmsg['body'] = "\n\n".join(sys.argv[2:])
    jsonmsg['to'] = sys.argv[1]

    cmdsock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    cmdsock.connect(config.get('main', 'socket'))
    cmdsock.send(json.dumps(jsonmsg))
    cmdsock.close()


if __name__ == "__main__":
    main()
