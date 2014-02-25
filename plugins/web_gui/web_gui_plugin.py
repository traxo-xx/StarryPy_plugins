#:coding=utf-8:
import os
import string
import random
from base_plugin import BasePlugin
from plugins.core.player_manager import permissions, PlayerManager, UserLevels
import web_gui
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
        if self.config.plugin_config['cookie_token'] == "" or not self.config.plugin_config['remember_cookie_token']:
            self.cookie_token = self.config.plugin_config['cookie_token'] = self.generate_cookie_token()
        else:
            self.cookie_token = self.config.plugin_config['cookie_token']
        self.websocket = web_gui.WebSocketChatHandler
        self.chatmessages = set()

    def activate(self):
        super(WebGuiPlugin, self).activate()
        self.player_manager = self.plugins['player_manager'].player_manager
        self.web_gui_app = web_gui.WebGuiApp(port=self.port, ownerpassword=self.ownerpassword,
                                             playermanager=self.player_manager, factory=self.factory,
                                             messages=self.chatmessages, cookie_secret=self.cookie_token)
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
        message = parsed.message.decode("utf-8")
        self.chatmessages.add(message)

