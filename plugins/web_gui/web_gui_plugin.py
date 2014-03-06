#:coding=utf-8:
import os
import string
import random
import json
from datetime import datetime
from base_plugin import BasePlugin
from plugins.core.player_manager import PlayerManager
from packets import chat_sent, client_connect
from . import web_gui
import tornado.ioloop
from tornado.platform.twisted import TwistedIOLoop
TwistedIOLoop().install()


class WebGuiPlugin(BasePlugin, PlayerManager):
    name = "web_gui"
    depends = ['player_manager']

    def __init__(self):
        super(WebGuiPlugin, self).__init__()
        try:
            self.port = int(self.config.plugin_config['port'])
        except (AttributeError, ValueError):
            self.port = 8083
        self.ownerpassword = self.config.plugin_config['ownerpassword']
        self.restart_script = self.config.plugin_config['restart_script']
        if self.config.plugin_config['cookie_token'] == "" or not self.config.plugin_config['remember_cookie_token']:
            self.cookie_token = self.config.plugin_config['cookie_token'] = self.generate_cookie_token()
        else:
            self.cookie_token = self.config.plugin_config['cookie_token']
        self.serverurl = self.config.plugin_config['serverurl']
        self.messages = set()
        self.messages_log = set()

    def activate(self):
        super(WebGuiPlugin, self).activate()
        self.player_manager = self.plugins['player_manager'].player_manager
        self.web_gui_app = web_gui.WebGuiApp(port=self.port, ownerpassword=self.ownerpassword,
                                             playermanager=self.player_manager, factory=self.factory,
                                             cookie_secret=self.cookie_token, serverurl=self.serverurl,
                                             messages=self.messages, messages_log=self.messages_log,
                                             restart_script=self.restart_script)
        self.logger.info("WebGUI listening on port {p}".format(p=self.port))
        self.gui_instance = tornado.ioloop.IOLoop.instance()

    def deactivate(self):
        super(WebGuiPlugin, self).deactivate()
        self.gui_instance.stop()

    def generate_cookie_token(self):
        chars = string.ascii_letters + string.digits
        random.seed(os.urandom(1024))
        return "".join(random.choice(chars) for i in range(64))

    def on_chat_sent(self, data):
        parsed = chat_sent().parse(data.data)
        msgdate = datetime.now().strftime("[%H:%M:%S]")
        message = json.dumps({"msgdate": msgdate, "author": self.protocol.player.name, "message": parsed.message.decode("utf-8")})
        self.messages.add(message)
        self.messages_log.add(message)

        return True

    def on_client_connect(self, data):
        parsed = client_connect().parse(data.data)
        msgdate = datetime.now().strftime("[%H:%M:%S]")
        connect_player = self.player_manager.get_by_name(parsed.name.decode("utf-8"))
        if self.player_manager.check_bans(connect_player.ip):
            msgtxt = "Banned Player {p} tried to join the server.".format(p=connect_player.name)
        else:
            msgtxt = "Player {p} has joined the server.".format(p=connect_player.name)
        message = json.dumps({"msgdate": msgdate, "author": "SERVER", "message": msgtxt})
        self.messages.add(message)
        self.messages_log.add(message)

        return True

    def on_client_disconnect(self, data):
        if self.protocol.player is not None:
            msgdate = datetime.now().strftime("[%H:%M:%S]")
            msgtxt = "Player {p} has left the server.".format(p=self.protocol.player.name.encode("utf-8"))
            message = json.dumps({"msgdate": msgdate, "author": "SERVER", "message": msgtxt})
            self.messages.add(message)
            self.messages_log.add(message)
