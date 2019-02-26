from __future__ import print_function

import sleekxmpp
import ConfigParser
import os, socket
import json
import systemd.daemon


class XmppBot(sleekxmpp.ClientXMPP):

    def __init__(self, jid, password):
        super(XmppBot, self).__init__(jid, password)
        self.auto_authorize = True
        self.add_event_handler('connected', self.connected_event)

    def connected_event(self, event=None):
        self._reset_connection_state(event)
        self.send_presence()

    def send_jsonmsg(self, jsonmsg):
        msg = json.loads(jsonmsg)
        self.send_message(mto=msg['to'], mbody=msg['body'])


def main():

    systemd.daemon.notify("STATUS=starting\n")

    config = ConfigParser.ConfigParser()
    config.read('xmppbot.conf')

    bot = XmppBot(
        config.get('main', 'jid'),
        config.get('main', 'password'))

    systemd.daemon.notify("STATUS=opening command socket\n")
    print("Opening command socket")

    cmdsock_path = config.get('main', 'socket')
    if os.path.exists(cmdsock_path):
        os.unlink(cmdsock_path)

    cmdsock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    cmdsock.bind(cmdsock_path)
    cmdsock.listen(128)

    print("Connecting server")
    systemd.daemon.notify("STATUS=connecting jabber server\n")

    if not bot.connect(address=(config.get('main', 'server'), 5222)):
        raise IOError("connection to server failed")

    bot.process()

    systemd.daemon.notify("STATUS=running\nREADY=1\n")
    print("Entering main loop")

    try:
        while True:
            connection, client_address = cmdsock.accept()
            print("Received connection")
            data = connection.recv(4096)
            print("Message: {}".format(data))
            bot.send_jsonmsg(data)

    except KeyboardInterrupt:
        print("Interrupt")

    finally:
        systemd.daemon.notify("STATUS=shutting down\nSTOPPING=1\n")
        print("Stopping bot")
        bot.disconnect()
        bot.stop.set()


if __name__ == "__main__":
    main()
