import socket
import json
import sys
import ConfigParser
import email
import logging

# postfix config example
#
# main.cf:
# transport_maps = hash:/etc/postfix/transport
#
# transport:
# jabber.tld jabber:
#
# master.cf:
# jabber unix - n n - - pipe user=jabberbot directory=/path/to/xmppbot argv=/path/to/python sendmail.py ${recipient}


logger = logging.getLogger('xmppbot')
logger.setLevel(logging.DEBUG)

logger_fh = logging.FileHandler('/var/log/xmppbot/sendmail.log')
logger_fh.setLevel(logging.DEBUG)

logger_fmt = logging.Formatter('%(asctime)-15s | %(levelname)-10s | %(message)s')
logger_fh.setFormatter(logger_fmt)

logger.addHandler(logger_fh)

def main():

    try:
        config = ConfigParser.ConfigParser()
        config.read('xmppbot.conf')

        msg = email.message_from_file(sys.stdin)

        jsonmsg = dict()
        jsonmsg['body'] = msg['Subject'] + "\n\n" if 'Subject' in msg else ''
        jsonmsg['body'] += msg.get_payload(decode=True)
        jsonmsg['to'] = sys.argv[1]

        cmdsock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        cmdsock.connect(config.get('main', 'socket'))
        cmdsock.send(json.dumps(jsonmsg))
        cmdsock.close()

    except:
        logger.exception("Something went wrong")
        sys.exit(75) # bounce

if __name__ == "__main__":
    main()

